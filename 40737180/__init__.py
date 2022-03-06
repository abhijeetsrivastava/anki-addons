# Picmonic Anki Add-On
#
# Copyright (C) 2020 Picmonic <https://www.picmonic.com/>
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

# import the main window object (mw) from aqt
from aqt import mw
# import all of the Qt GUI library
from aqt.qt import *
from aqt.reviewer import Reviewer
import decorator
from .settings import SettingsDialog
from .onboarding import OnboardingDialog

# get the config from config.json
config = mw.addonManager.getConfig(__name__)

# order is important here because of the "typing" library
ADDON_DIR_NAME = __name__.split(".")[0]
ADDON_PATH = os.path.join(mw.pm.addonFolder(), ADDON_DIR_NAME)
sys.path.insert(0, os.path.join(ADDON_PATH, "_vendor"))
from flashtext import KeywordProcessor
import json

# the typing library is not included in older version of python
from ._vendor.dotenv import load_dotenv
from typing import Any, Callable, Tuple

"""
    LOAD ENV VARS
"""
if os.path.isfile(os.path.join(ADDON_PATH, ".env")):
    load_dotenv(dotenv_path=os.path.join(ADDON_PATH, ".env"))

apiBaseUrl = os.environ.get("API_BASE_URL") or "https://www.picmonic.com/"

"""
    SETTINGS DIALOG
"""
settingsDialog = SettingsDialog(config, mw)
mw.addonManager.setConfigAction(ADDON_DIR_NAME, settingsDialog.show)

"""
    ONBOARDING DIALOG
"""
onboardingDialog = OnboardingDialog(config, mw)

"""
    HANDLE INJECTING JS/CSS
"""
# Bypasses Anki's security policy to enable loading of our web elements.
mw.addonManager.setWebExports(__name__, r"web(\\|/).*")
baseFolder = f"/_addons/{ADDON_DIR_NAME}/web"
dictionaryFilesFolder = os.path.join(mw.pm.addonFolder(), ADDON_DIR_NAME, 'dictionary')

def _getScriptsAndStyles():
    stylesAndScripts = "\n"

    js = [
        "tracking.js",
        "mark.min.js",
        "popper.min.js",
        "tippy.umd.min.js",
    ]
    css = [
        "fonts.css",
        "tippy.css",
        "tippy-theme-light-picmonic.css",
        "app.css",
    ]

    stylesAndScripts += f"""<script>window.api_base_url = "{apiBaseUrl}";</script>"""

    for f in js:
        stylesAndScripts += f"""<script src="{baseFolder}/js/{f}"></script>\n"""
    for f in css:
        stylesAndScripts += f"""<link rel="stylesheet" href="{baseFolder}/css/{f}">\n"""

    return stylesAndScripts


# Anki 2.1.22+ Hook
def _onWebviewWillSetContent(web_content: "WebContent", context: Reviewer):
    if not isinstance(context, Reviewer):
        return

    web_content.body += _getScriptsAndStyles()


# Anki Legacy Hook
def _onRevHtml(reviewer: Reviewer, _old: Callable):
    return _old(reviewer) + _getScriptsAndStyles()


def wrap(old: Callable, new: Callable):
    """Override an existing method."""

    def decorator_wrapper(f: Callable, *args, **kwargs):
        return new(_old=old, *args, **kwargs)

    return decorator.decorator(decorator_wrapper)(old)


try:  # Anki 2.1.22+
    # register web content hook to update reviewer HTML content
    from aqt.gui_hooks import webview_will_set_content

    webview_will_set_content.append(_onWebviewWillSetContent)
except (ImportError, ModuleNotFoundError):
    # Legacy: monkey-patch original Reviewer.revHtml method to add
    # our own web elements.
    Reviewer.revHtml = wrap(
        Reviewer.revHtml, _onRevHtml
    )

"""
    HANDLE CLICKING A LINK
"""
PICMONIC_LINK_PREFIX = "picmonic"


def _callLinkHandler(message: str):
    _, cmd, payload = message.split(":", 2)

    if cmd == "link":
        return QDesktopServices.openUrl(QUrl(payload))


def _onReviewerLinkHandler(reviewer: Reviewer, link: str, _old: Callable):
    # TODO: delegate to ReviewerLinkHandler completely, ideally
    if not link.startswith(PICMONIC_LINK_PREFIX):
        return _old(reviewer, link)
    return _callLinkHandler(link)


def _onWebviewDidReceiveJSMessage(
    handled: Tuple[bool, Any], message: str, context: Reviewer
) -> Tuple[bool, Any]:
    """JS <-> PY bridge handling on Anki >= 2.1.22"""
    if not isinstance(context, Reviewer):
        # TODO?: Extend support to other web views
        return handled

    if not message.startswith(PICMONIC_LINK_PREFIX):
        return handled

    return (True, _callLinkHandler(message))

try:  # Anki >= 2.1.22
    # Subscribe to bridge call hook
    from aqt.gui_hooks import webview_did_receive_js_message

    webview_did_receive_js_message.append(_onWebviewDidReceiveJSMessage)
except (ImportError, ModuleNotFoundError):
    # Legacy: Monkey-patch original Reviewer._linkHandler method to do our own
    # link handling
    Reviewer._linkHandler = wrap(
        Reviewer._linkHandler, _onReviewerLinkHandler
    )

"""
    HANDLE MARKING WORDS 
"""
timeout = 60
retries = 1
__version__ = 1
ankiVersion = 1

def prepare(html, card, context):
    note = card.note()
    text = " ".join(tuple(field.strip() for field in note.fields if field.strip()))
    results = []

    # Case insensitive
    with open(dictionaryFilesFolder + '/case-insensitive.json') as f:
        data = json.load(f)

    keyword_processor = KeywordProcessor()
    keyword_processor.add_keywords_from_dict(data)

    insensitive = keyword_processor.extract_keywords(text)

    # Remove duplciates
    insensitive = list(dict.fromkeys(insensitive))

    # Case sensitive
    with open(dictionaryFilesFolder + '/case-sensitive.json') as f:
        data = json.load(f)

    keyword_processor = KeywordProcessor(case_sensitive=True)
    keyword_processor.add_keywords_from_dict(data)

    sensitive = results + keyword_processor.extract_keywords(text)

    # remove duplicates
    sensitive = list(dict.fromkeys(sensitive))

    # Set the color of the underline
    html = html + "<style>.picmonic-marker { border-bottom: 2px solid "+config['underlineColor']+";}</style>"

    # Set the variable for showing the picmonic eye when the popup system conflicts with AMBOSS
    html = html + "<script>whenPopupConflictsShowLogo = "+str(config['whenPopupConflictsShowLogo']).lower()+";</script>"

    html = html + "<style>.picmonic-inline-anchor { opacity: "+str(config['logoOpacity'])+";}</style>"

    # Generate an analytics id if not already created
    if config['analyticsId'] == "":
        import binascii
        config['analyticsId'] = binascii.hexlify(os.urandom(9)).decode()
        mw.addonManager.writeConfig(__name__, config)

    html = html + "<script>picmonicAnalyticsId = '" + config['analyticsId'] + "';</script>"
    html = html + "<script>picmonicMarketId = '" + str(config['marketId']) + "';</script>"

    # Add our search results to the HTML
    html = html + "<script>picmonic_results = {}; picmonic_results.insensitive = JSON.parse('" + json.dumps(insensitive).replace("'", "\\'") + "'); picmonic_results.sensitive = JSON.parse('" + json.dumps(sensitive).replace("'", "\\'") + "');</script>"

    # add our results to the html
    return html + """
<script>
_onLinkClick = function(e) {
    e.preventDefault();

    if (typeof atlasEvent === 'function') {
        element = e.currentTarget;
        atlasEvent('click', element.getAttribute('track') + ' ' + element.getAttribute('track-description'));
    }

    if (typeof pycmd === 'function') {
        pycmd("picmonic:link:"+e.currentTarget.href)
    }
}

registerOnLinkClickEvents = function() {
    embed = document.getElementById("picmonic-anki-embed");
    
    if (!embed) {
        return;
    }

    links = embed.querySelectorAll('a');

    for (i = 0; i < links.length; i++) {
        links[i].addEventListener("click", _onLinkClick);
    }
}

onUpdateHook.push(function () {
    if (typeof Mark !== 'function') {
        return;
    }

    instance = new Mark(document.getElementById('qa')); 

    if (!picmonic_results) {
        return;
    }

    for(searchType in picmonic_results) {
        if (!picmonic_results[searchType].length) {
            continue;
        }
    
        for(result of picmonic_results[searchType]) {
            pieces = result.split("|||");
            term = pieces[0];
            picmonics = pieces[1].split('||');
            inMarketPicmonics = [];
            
            // only highlight picmonics which are in the selected market
            for (i = 0; i < picmonics.length; i++) {
              if (picmonics[i].split('|')[1].split(',').indexOf(picmonicMarketId) !== -1) {
                inMarketPicmonics.push(picmonics[i]);
              }
            }

            // no in market picmonics return early
            if (!inMarketPicmonics.length) {
                return;
            }
            
            // Find synonyms with multiple matching picmonics and select ONLY ONE picmonic with the shortest slug
            // This occurs for topics that are split into multiple picmoncis such as:
            // - benign-prostatic-hyperplasia-bph-disease_1402
            // - benign-prostatic-hyperplasia-bph-diagnosis-and-treatment_1403
            // - benign-prostatic-hyperplasia-bph-assessment_1481
            // - benign-prostatic-hyperplasia-bph-interventions_1675
            slug = inMarketPicmonics[0].split("|")[0];
            for (i = 0; i < inMarketPicmonics.length; i++) {
              currentSlug = inMarketPicmonics[i].split("|")[0];
              if (currentSlug.length < slug.length) {
                slug = currentSlug;
              }
            }
        
            instance.mark(term, {
                separateWordSearch: false,
                className: "picmonic-marker",
                caseSensitive: searchType === 'sensitive',
                ignorePunctuation: "?:;.,-–—‒_(){}[]!'\\"+=".split(""),
                accuracy: {
                    "value": "exactly",
                    "limiters": [",", ".", "?", "/", ")", "("]
                },
                each: function(node, range){
                    // Play nice with AMBOSS plugin by appending a new element to use as the hover trigger
                    if ((typeof tippy === 'function' || typeof ambossAddon === 'object') && whenPopupConflictsShowLogo) {
                        picImage = new Image();
                        picImage.src =  '""" + baseFolder + """/img/logo.svg';
                        picImage.className = "picmonic-inline-anchor";
                        elem = node.appendChild(picImage);
                    } else {
                        elem = node;
                    }
                
                    // Manually modified tippy.min.js to change tippy -> tippyp so we can play nicely with the AMBOSS plugin
                    tippyp(elem, {
                        appendTo: function() {
                            return document.body
                        },
                        onCreate(instance) {
                            instance._isFetching = false;
                            instance.slug = slug;
                            instance.term = term;
                        },
                        onShow(instance) {
                          tippyp.hideAll({ duration: 0 });  
                        
                          if (typeof atlasEvent === 'function') {
                            atlasEvent('show', instance.term, undefined, undefined, undefined, undefined, '/anki/embed/' + instance.slug);
                          }
                        
                          if (instance._isFetching) {
                            return;
                          }
                          
                          instance._isFetching = true;
                          
                          fetch('""" + apiBaseUrl + """api/v3/anki/embed/' + instance.slug + '?platform=anki&market_id=' + picmonicMarketId)
                          .then((response) => response.text())
                          .then((text) => {
                            instance.setContent('<div class="picmonic-embed-container">'+text+'</div>');
                            registerOnLinkClickEvents();
                          })
                          .catch((error) => {
                            instance._error = error;
                            instance.setContent(`Request failed. ${error}`);
                            instance._isFetching = false;
                          });
                        },
                        content: '<div class="pls-loading-icon"><img src=\"""" + baseFolder + """/img/loading.svg" alt="Loading"></div>',
                        allowHTML: true,
                        animateFill: false,
                        animation: 'shift-away',
                        theme: "picmonic",
                        arrow: true,
                        interactive: true,
                        interactiveDebounce: 100,
                        flipOnUpdate: true,
                        maxWidth: "900px",
                        boundary: "window",
                        multiple: true,
                        placement: "bottom",
                        duration: 100,
                    });
                }}
            );
        };
   };
});
</script>"""

try:  # Anki >= 2.1.20
    from aqt import gui_hooks

    gui_hooks.card_will_show.append(prepare)
except (ImportError, ModuleNotFoundError):
    from anki.hooks import addHook
    addHook('prepareQA', prepare)


try:  # Anki >= 2.1.20
    from aqt import gui_hooks

    if config['onboardingSeen'] == 0:
        gui_hooks.main_window_did_init.append(onboardingDialog.show)
except (ImportError, ModuleNotFoundError):
    pass  # do nothing
