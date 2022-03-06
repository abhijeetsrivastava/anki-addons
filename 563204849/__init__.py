# AGPLv3
# Copyright (c) 2013 Steve AW
#           (c) 2016-2017 Glutanimate
#           (c) 2019- ijgnd
#           (c) 2020 jamesnicolas


import datetime
from pprint import pprint as pp

from anki.hooks import wrap
import aqt
from aqt import gui_hooks

from aqt.deckbrowser import DeckBrowser
from aqt.overview import Overview
from aqt.theme import theme_manager


def gc(arg, fail=False):
    conf = aqt.mw.addonManager.getConfig(__name__)
    if conf:
        return conf.get(arg, fail)
    else:
        return fail


def whenIsNextLrnDue(sqlstring, append_relative):
    all_learning = aqt.mw.col.db.all(sqlstring)
    if not all_learning:
        return
    all_learning = dict(all_learning)  # dict consists of  card_id: due_in_epoch_time
    now = datetime.datetime.now()
    # dayOffset - next day starts at
    # in 2.1.14 values can be between 0 and 23, no negative values
    if aqt.mw.col.schedVer() == 2:
        dayOffset = aqt.mw.col.conf.get("rollover", 4)
    else:
        # https://github.com/ankidroid/Anki-Android/wiki/Database-Structure
        #   crt = timestamp of the creation date. It's correct up to the day. For V1 scheduler,
        #   the hour corresponds to starting a new day. By default, new day is 4.
        dayOffset = datetime.datetime.fromtimestamp(aqt.mw.col.crt).hour

    now = datetime.datetime.today()  # returns the current local date, same as date.fromtimestamp(time.time())
    if now.hour < dayOffset:
        now = now - datetime.timedelta(days=1)
    todaystart = datetime.datetime(
        year=now.year, month=now.month, day=now.day, hour=dayOffset, second=0
    )
    todaystartepoch = int(todaystart.timestamp())
    relevant_cid = None
    for this_due_val in sorted(list(all_learning.values())):
        if this_due_val < todaystartepoch:
            continue
        for cid, due_val in all_learning.items():
            if due_val == this_due_val:
                relevant_cid = cid
                break
    if not relevant_cid:
        return
    cdo = datetime.datetime.fromtimestamp(this_due_val)
    seconds = ":%S" if gc("time_with_seconds", True) else ""
    if gc("time_24hour_clock", True):
        f = f"%H:%M{seconds}"
    else:
        f = f"%I:%M{seconds} %p"
    color = "white" if theme_manager.night_mode else "black"
    linktext = cdo.strftime(f)
    if append_relative:
        linktext += f" ({timeInAgo(cdo)})"
    tstr = f"""<a href=# style="text-decoration: none; color:{color};"
    onclick="return pycmd('BrowserSearch#{str(relevant_cid)}')">{linktext}</a>"""
    msg = gc("sentence_beginning", "The next learning card due today is due at ") + tstr
    return "<div>" + msg + "</div>"


def timeInAgo(t):
    zero = datetime.timedelta(0)
    now = datetime.datetime.now()
    td = t - now
    due_later = True
    if td < zero:
        due_later = False
        td = now - t
    if int(td.total_seconds()) == 0:
        return "now"
    hours = int(td.total_seconds() / 3600)
    minutes = int(td.total_seconds() / 60 % 60)
    seconds = int(td.total_seconds() % 60)
    msg = ""
    if hours:
        msg += "%dh" % (hours)
    if minutes:
        msg += "%dm" % (minutes)
    msg += "%ds" % (seconds)
    if due_later:
        msg = "in " + msg
    else:
        msg += " ago"
    return msg


def deckbrowserMessage(self, _old):
    sql_string_all = """select id, due from cards where queue = 1 order by due"""
    add_this = whenIsNextLrnDue(sql_string_all, False)
    if add_this:
        return _old(self) + add_this
    else:
        return _old(self)
# TODO newstyle hooks -  maybe gui_hooks.deck_browser_will_render_content
DeckBrowser._renderStats = wrap(DeckBrowser._renderStats, deckbrowserMessage, "around")


def addRemainingTimeToDesc(overview, content):
    did = str(aqt.mw.col.decks.current()["id"])
    sql = f"select id, due from cards where queue = 1 and did = {did} order by due"
    add_this = whenIsNextLrnDue(sql, True)
    if add_this:
        content.desc += add_this
gui_hooks.overview_will_render_content.append(addRemainingTimeToDesc)


def openBrowser(searchterm):
    browser = aqt.dialogs.open("Browser", aqt.mw)
    browser.form.searchEdit.lineEdit().setText(searchterm)
    browser.onSearchActivated()
    if "noteCrt" in browser.model.activeCols:
        col_index = browser.model.activeCols.index("noteCrt")
        browser.onSortChanged(col_index, True)
    browser.form.tableView.selectRow(0)


def myLinkHandler(self, url, _old):
    if url.startswith("BrowserSearch#"):
        out = url.replace("BrowserSearch#", "").split("#", 1)[0]
        openBrowser("cid:" + out)
    else:
        return _old(self, url)
Overview._linkHandler = wrap(Overview._linkHandler, myLinkHandler, "around")
DeckBrowser._linkHandler = wrap(DeckBrowser._linkHandler, myLinkHandler, "around")
