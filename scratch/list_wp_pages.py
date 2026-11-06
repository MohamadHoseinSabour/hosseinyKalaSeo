import urllib.request
import base64
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

creds = base64.b64encode(b'agent:Mlwg pHHX NQ64 drrz 7ca2 IVto').decode('utf-8')
req = urllib.request.Request('https://hosseinykala.ir/wp-json/wp/v2/pages?per_page=50', headers={'Authorization': 'Basic ' + creds})
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        pages = json.loads(r.read().decode('utf-8'))
        print(f"Total pages: {len(pages)}")
        for p in pages:
            print(f"ID: {p.get('id'):<5} | Slug: {p.get('slug'):<25} | Title: {p.get('title', {}).get('rendered')}")
except Exception as e:
    print("Error:", e)
