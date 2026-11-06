import urllib.request
import re

url = "https://s100.divarcdn.com/web-assets/2026/11/services-671.a9cd9b37.desktop.js"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
content = urllib.request.urlopen(req).read().decode('utf-8')

# Search for endpoints or /pro/ or premium
matches = set(re.findall(r'["\'](/v\d+/[^"\']+)["\']', content))
print(f"Found {len(matches)} API paths in services:")
for m in sorted(matches):
    if any(x in m for x in ['pro', 'premium', 'store', 'dealer', 'place', 'post', 'business', 'shop']):
        print(" ->", m)
