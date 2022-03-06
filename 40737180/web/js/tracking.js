function atlasEvent(e, o, n, t, r, i, u) {
    var c = u || '',
        a = '',
        p = new XMLHttpRequest;
        actionPrefix = 'picmonic-anki-';
    p.open("POST", window.api_base_url + "api/v3/anki/analytics", !0), p.setRequestHeader("Content-type", "application/x-www-form-urlencoded"), p.send("action=" + actionPrefix + e + "&source=script&url=" + c + "&referrer=" + a + "&description=" + o + "&flow=" + n + "&step=" + t + "&timelimit=" + r + "&onlynewvisitors=" + i + "&analyticsid=" + window.picmonicAnalyticsId), console.info("Action: " + e + " | URL: " + c + " | Description: " + o)
}