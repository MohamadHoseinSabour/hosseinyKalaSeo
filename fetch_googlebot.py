import urllib.request
import re
import json

url = 'https://divar.ir/pro/xTlfvkBc'
req = urllib.request.Request(
    url,
    headers={
        'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'fa-IR,fa;q=0.9,en;q=0.8',
    }
)

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8')
        print("Success! Length:", len(html))
        with open("divar_googlebot.html", "w", encoding="utf-8") as f:
            f.write(html)
            
        m = re.search(r'window\.__PRELOADED_STATE__\s*=\s*(\{.*?\});?\s*</script>', html, re.DOTALL)
        if m:
            state = json.loads(m.group(1))
            print("Googlebot Preloaded State keys:", list(state.keys()))
            with open("divar_googlebot_state.json", "w", encoding="utf-8") as out:
                json.dump(state, out, ensure_ascii=False, indent=2)
            
            # Check premiumPanel or nb in googlebot state
            pp = state.get('premiumPanel', {})
            landing = pp.get('landing', {})
            print("Landing pageTitle:", landing.get('pageTitle'))
            print("Header widgets:", len(landing.get('headerWidgets', [])))
            print("Post row widgets:", len(landing.get('postRowWidgets', [])))
            
            nb = state.get('nb', {})
            print("nb listWidgets:", len(nb.get('listWidgets', [])))
        else:
            print("No PRELOADED_STATE in googlebot html")
except Exception as e:
    print("Error:", e)
