import urllib.request
import re
import json

req = urllib.request.Request('https://pagespeed.web.dev/analysis/https-hosseinykala-ir/p31vkp5f3e?form_factor=mobile', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode('utf-8')

# Look for embedded json data in the page
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
print("Found scripts:", len(scripts))

for s in scripts:
    if 'lighthouseResult' in s or 'categories' in s:
        print("Found lighthouseResult in script!")
        # Try to extract json
        m = re.search(r'(\{\"lighthouseResult\".*?\})\s*;', s)
        if m:
            print("Extracted JSON data!")
            data = json.loads(m.group(1))
            cats = data.get('lighthouseResult', {}).get('categories', {})
            for c, v in cats.items():
                print(f"  {c}: {v.get('score')}")
