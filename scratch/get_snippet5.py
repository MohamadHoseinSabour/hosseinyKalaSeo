import urllib.request
import base64
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

creds = base64.b64encode(b'agent:Mlwg pHHX NQ64 drrz 7ca2 IVto').decode('utf-8')
req = urllib.request.Request('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/5', headers={
    'Authorization': 'Basic ' + creds,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        with open('scratch/snippet5_code.php', 'w', encoding='utf-8') as f:
            f.write(data.get('code', ''))
        print("Success! Lines:", len(data.get('code', '').splitlines()))
except Exception as e:
    print("Error:", e)
