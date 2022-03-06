# AMBOSS Anki Add-on
#
# Copyright (C) 2019-2020 AMBOSS MD Inc. <https://www.amboss.com/us>
# Copyright (C) 2020 Ankitects Pty Ltd and contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import time
from typing import TYPE_CHECKING, Any, Callable, NamedTuple, Optional

from aqt.utils import openLink
from aqt.webview import AnkiWebPage, AnkiWebView
from PyQt5.QtCore import QDateTime, QObject, QUrl, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtNetwork import QNetworkCookie

# TODO: Drop ignore once we are ready to move to Qt 5.15.x
# (cf. sidepanel_web comment)
from PyQt5.QtWebEngineWidgets import (  # type: ignore
    QWebEnginePage,
    QWebEngineProfile,
)
from PyQt5.QtWidgets import QWidget

from .hooks import amboss_did_login, amboss_did_logout, profile_will_close
from .profile import ProfileAdapter
from .shared import safe_print
from .theme import ThemeManager

URI_BLANK = "about:blank"

if TYPE_CHECKING:
    from aqt.mediasrv import MediaServer


class Cookie(NamedTuple):
    """
    Custom data exchange format for cookies
    Fully typed and easier to handle than QNetworkCookie
    """

    name: str
    value: str
    domain: str
    path: str
    expires: Optional[int]
    secure: bool
    http_only: bool


class _CookieTranslator:
    @staticmethod
    def cookie_from_qcookie(qcookie: QNetworkCookie) -> Cookie:
        # TODO: bytearray typing below should be fixable (decode arr directly to str?)
        return Cookie(
            name=bytearray(qcookie.name()).decode(),  # type: ignore[call-overload]
            value=bytearray(qcookie.value()).decode(),  # type: ignore[call-overload]
            domain=qcookie.domain(),
            path=qcookie.path(),
            expires=qcookie.expirationDate().toSecsSinceEpoch()
            if qcookie.expirationDate()
            else None,
            secure=qcookie.isSecure(),
            http_only=qcookie.isHttpOnly(),
        )

    @staticmethod
    def qcookie_from_cookie(cookie: Cookie) -> QNetworkCookie:
        qcookie = QNetworkCookie(
            name=cookie.name.encode("utf-8"), value=cookie.value.encode("utf-8")
        )
        qcookie.setDomain(cookie.domain)
        qcookie.setPath(cookie.path)
        qcookie.setHttpOnly(True)
        qcookie.setSecure(cookie.secure)
        if cookie.expires:
            qcookie.setExpirationDate(QDateTime.fromSecsSinceEpoch(cookie.expires))
        return qcookie


class WebProfile(QWebEngineProfile):
    """
    Custom web engine profile, currently solely used for the side panel

    Allows us to keep persistent web data separate from Anki's regular web views,
    implement convenience methods for setting/getting cookies, and customizing
    web engine settings such as HTTP cache use
    """

    def __init__(
        self,
        storage_name: str,
        user_agent: Optional[str] = None,
        parent: QObject = None,
    ):
        super().__init__(storage_name, parent=parent)  # type: ignore
        if user_agent:
            self.setHttpUserAgent(f"{self.httpUserAgent()} {user_agent}")

    def set_cookie(self, cookie: Cookie):
        self.cookieStore().setCookie(_CookieTranslator.qcookie_from_cookie(cookie))

    def delete_all_cookies(self):
        self.cookieStore().deleteAllCookies()


class WebPage(AnkiWebPage):

    """
    Basic QWebEnginepage, extending AnkiWebPage with a number of convenience features
    that we need:

    - more advanced domDone handling
    - handling of external link opening
    - ability to set up a custom bridge, bypassing the webview_did_receive_js_message
      hook

    """

    _custom_bridge_cmd: Optional[Callable[[str], Any]]

    def __init__(self, on_bridge_cmd: Optional[Callable] = None):
        self._custom_bridge_cmd: Optional[Callable[[str], Any]] = on_bridge_cmd
        super().__init__(self._wrapped_bridge_command)

    def _wrapped_bridge_command(self, message: str) -> Any:
        view: WebView = self.view()  # type: ignore[assignment]

        handled = view.handle_js_message(message)

        if handled:
            return

        if self._custom_bridge_cmd:
            return_value_for_js = self._custom_bridge_cmd(message)
            return return_value_for_js
        elif message.lower().startswith("http"):
            openLink(message)

        return

    def setBridgeCommand(self, bridge_command: Optional[Callable[[str], Any]]) -> None:
        self._custom_bridge_cmd = bridge_command


class LocalWebPage(WebPage):
    """
    Only opens local links inside the view, delegating all other links to
    the default system handler

    Inherits from AnkiWebPage rather than WebPage to reduce error surface
    """

    def acceptNavigationRequest(self, url: QUrl, nav_type, is_main_frame) -> bool:
        if url.host() == "localhost":
            return True
        openLink(url)
        return False


class WebView(AnkiWebView):
    def __init__(
        self,
        theme_manager: ThemeManager,
        history_filter: Optional[Callable[[str], bool]] = None,
        parent: Optional[QWidget] = None,
        object_name: Optional[str] = None,
    ):
        self._theme_manager = theme_manager
        self._history_filter = history_filter
        super().__init__(parent)
        if object_name:
            self.setObjectName(object_name)

    def load(self, url: QUrl):  # type: ignore[override]
        # Allows using Anki's domDone JS eval queueing system when loading directly
        # from a URL: (support for this is native on Anki 2.1.28+)
        self._domDone = False
        super().load(url)

    def setPage(self, page: WebPage):  # type: ignore[override]
        # re-apply window bg color to reduce flicker

        try:  # < 2.1.45
            bg_color = self._getWindowColor()
        except AttributeError:  # >= 2.1.45
            bg_color = self.get_window_bg_color(self._theme_manager.night_mode)
        except Exception:  # fallback
            safe_print("AMBOSS: Could not determine window bg color")
            bg_color = QColor("#ececec")  # Anki default for macOS

        page.setBackgroundColor(bg_color)
        super().setPage(page)

    def navigate_forward(self):
        if self.can_navigate_forward():
            self.triggerPageAction(QWebEnginePage.Forward)

    def navigate_back(self):
        if self.can_navigate_back():
            self.triggerPageAction(QWebEnginePage.Back)

    def can_navigate_forward(self) -> bool:
        history = self.page().history()
        url = history.forwardItem().url().toString()
        history_available = history.canGoForward() and bool(url)

        if history_available is False or not self._history_filter:
            return history_available

        return self._history_filter(url)

    def can_navigate_back(self) -> bool:
        history = self.page().history()
        url = history.backItem().url().toString()
        history_available = history.canGoBack() and bool(url)

        if history_available is False or not self._history_filter:
            return history_available

        return self._history_filter(url)

    def handle_js_message(self, cmd: str) -> bool:
        """Handles JS messages coming in from WebPage instance via pycmd bridge
        while skipping the webview_did_receive_js_message hook that AnkiWebView
        normally pipes JS messages through if not handled in AnkiWebView._onBridgeCmd
        directly.

        :param cmd: JS message
        :return: Whether the message was handled at this level or not. Messages
                 not handled here will be handled by the custom bridge command
                 specified in the originating WebPage instance
        """
        # NOTE: based on AnkiWebView._onBridgeCmd, should be kept in sync with it
        # FIXME: Depends on AnkiWebView implementation details, thus is prone to
        # breaking if the private API changes (though that goes for a lot of the
        # code in this module)
        if self._shouldIgnoreWebEvent():
            safe_print("ignored late bridge cmd", cmd)
            return True

        if not self._filterSet:
            self.focusProxy().installEventFilter(self)
            self._filterSet = True

        if cmd == "domDone":
            self._domDone = True
            self._maybeRunActions()
            return True

        return False


class WebProfileAuthHandler(QObject):

    """
    Subscribes to login hooks, syncing auth cookies with general add-on login state
    """

    logged_in = pyqtSignal()
    logged_out = pyqtSignal()
    error = pyqtSignal(Exception)

    def __init__(
        self,
        web_profile: WebProfile,
        profile_adapter: ProfileAdapter,
        auth_token_cookie_name: str,
        auth_token_cookie_domain: str,
    ):
        super().__init__(parent=web_profile)
        self._web_profile = web_profile
        self._profile_adapter = profile_adapter
        self._auth_token_cookie_name = auth_token_cookie_name
        self._auth_token_cookie_domain = auth_token_cookie_domain

    def subscribe_to_auth_events(self):
        # NOTE: login hook is called on each startup, not just initial log in
        amboss_did_login.append(self._on_amboss_did_login)
        amboss_did_logout.append(self._on_amboss_did_logout)
        profile_will_close.append(self._on_profile_will_close)

    def _on_amboss_did_login(self):
        try:
            cookie = self._auth_cookie()
        except ValueError as e:
            self.error.emit(e)
            return
        self._web_profile.set_cookie(cookie)
        self.logged_in.emit()

    def _on_amboss_did_logout(self):
        self._web_profile.delete_all_cookies()
        self.logged_out.emit()

    def _on_profile_will_close(self):
        self._web_profile.delete_all_cookies()

    def _auth_cookie(self) -> Cookie:
        if not self._profile_adapter.token:
            raise ValueError("AMBOSS auth token not set. Could not generate cookie.")
        return Cookie(
            name=self._auth_token_cookie_name,
            domain=self._auth_token_cookie_domain,
            value=self._profile_adapter.token,
            path="/",
            expires=int(time.time()) + 365 * 86400,
            secure=True,
            http_only=True,
        )


class LocalURLResolver:

    _local_server_host = "localhost"

    def __init__(self, package_name: str, media_server: "MediaServer"):
        self._package_name = package_name
        self._media_server = media_server

    def resolve(self, relative_file_path: str) -> str:
        return (
            f"""http://{self._local_server_host}:{self._media_server.getPort()}"""
            f"""/_addons/{self._package_name}/{relative_file_path}"""
        )
