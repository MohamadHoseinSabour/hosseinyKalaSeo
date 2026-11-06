import urllib.request
import re

url = "https://s100.divarcdn.com/web-assets/2026/11/store-962.9307be70.desktop.js"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
content = urllib.request.urlopen(req).read().decode('utf-8')

print("store chunk length:", len(content))

# Look for url strings or api paths
paths = re.findall(r'["\'](https?://[^"\']+|/[a-zA-Z0-9_\-\/]+)["\']', content)
print("Found paths:", len(paths))
for p in set(paths):
    if any(k in p.lower() for k in ['v8', 'pro', 'panel', 'store', 'dealer', 'business', 'post', 'api']):
        print("  ", p)
