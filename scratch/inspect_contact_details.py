import urllib.request
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request('https://hosseinykala.ir/contact/', headers={'User-Agent': 'Mozilla/5.0 (iPhone)'})
with urllib.request.urlopen(req, timeout=15) as r:
    html = r.read().decode('utf-8', errors='ignore')

# Check if there is an iframe (e.g. Google Maps or Neshan)
iframes = re.findall(r'<iframe[^>]+>', html)
print(f"Iframes on /contact/: {len(iframes)}")
for ifr in iframes:
    print("  ", ifr[:200])

# Check forms
forms = re.findall(r'<form[^>]+>', html)
print(f"Forms on /contact/: {len(forms)}")
for f in forms:
    print("  ", f[:150])

# Check large assets or base64
base64_matches = re.findall(r'data:[^;]+;base64,[A-Za-z0-9+/=]{100,}', html)
print(f"Large base64 strings on /contact/: {len(base64_matches)}")
if base64_matches:
    print("  Total base64 bytes:", sum(len(b) for b in base64_matches))
