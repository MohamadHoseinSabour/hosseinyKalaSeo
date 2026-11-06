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
url = 'https://hosseinykala.ir/wp-json/wp/v2/product/2885'
req = urllib.request.Request(url, headers={'Authorization': f'Basic {creds}', 'User-Agent': 'Mozilla/5.0'})
try:
    p = json.loads(urllib.request.urlopen(req, context=ctx, timeout=8).read().decode('utf-8'))
    fm_id = p.get('featured_media')
    print('Featured media ID:', fm_id)
    if fm_id:
        media_url = f'https://hosseinykala.ir/wp-json/wp/v2/media/{fm_id}'
        req_m = urllib.request.Request(media_url, headers={'Authorization': f'Basic {creds}', 'User-Agent': 'Mozilla/5.0'})
        m = json.loads(urllib.request.urlopen(req_m, context=ctx, timeout=8).read().decode('utf-8'))
        print('Image source url:', m.get('source_url'))
except Exception as e:
    print('Err:', e)
