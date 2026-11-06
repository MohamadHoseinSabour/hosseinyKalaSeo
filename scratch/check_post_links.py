import urllib.request
import base64
import json
import ssl
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://hosseinykala.ir/wp-json/wp/v2/posts/3857'
creds = base64.b64encode(b'agent:Mlwg pHHX NQ64 drrz 7ca2 IVto').decode('utf-8')
req = urllib.request.Request(url, headers={'Authorization': f'Basic {creds}', 'User-Agent': 'Mozilla/5.0'})
post = json.loads(urllib.request.urlopen(req, context=ctx, timeout=10).read().decode('utf-8'))

soup = BeautifulSoup(post['content']['rendered'], 'html.parser')
links = soup.find_all('a')
print(f'Total links in post: {len(links)}')
for a in links:
    print(f'Anchor: "{a.get_text(strip=True)}" -> URL: {a.get("href")}')
