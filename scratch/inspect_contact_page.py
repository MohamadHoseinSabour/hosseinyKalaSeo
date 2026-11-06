import urllib.request
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request('https://hosseinykala.ir/contact/', headers={'User-Agent': 'Mozilla/5.0 (iPhone)'})
with urllib.request.urlopen(req) as r:
    html = r.read().decode('utf-8', errors='ignore')

# Check titles / headings
headings = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', html, re.DOTALL)
print("Headings on /contact/:")
for h in headings[:10]:
    clean = re.sub(r'<[^>]+>', '', h).strip()
    if clean:
        print(" ", clean)

# Check widgets
widgets = re.findall(r'class=[\'"][^\'"]*elementor-widget-([^\'"]+)[\'"]', html)
print(f"\nElementor widgets on /contact/: {len(widgets)}")
for w in set(widgets):
    print(" ", w)
