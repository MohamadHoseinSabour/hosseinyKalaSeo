import urllib.request
import base64
import json
import ssl
import sys

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

creds = base64.b64encode(b'agent:Mlwg pHHX NQ64 drrz 7ca2 IVto').decode('utf-8')
url = 'https://hosseinykala.ir/wp-json/wp/v2/posts?status=publish,future,draft&per_page=6'
req = urllib.request.Request(url, headers={'Authorization': f'Basic {creds}', 'User-Agent': 'Mozilla/5.0'})
try:
    posts = json.loads(urllib.request.urlopen(req, context=ctx, timeout=8).read().decode('utf-8'))
    print(f'Total retrieved: {len(posts)}')
    for p in posts:
        print(f"ID: {p['id']} | Status: {p['status']} | Date: {p['date']} | Title: {p['title']['rendered']}")
except Exception as e:
    print('Err:', e)
