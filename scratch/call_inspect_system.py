import urllib.request
import base64
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

creds = base64.b64encode(b'agent:Mlwg pHHX NQ64 drrz 7ca2 IVto').decode('utf-8')
req = urllib.request.Request('https://hosseinykala.ir/wp-json/hk-perf/v1/inspect-system', headers={
    'Authorization': 'Basic ' + creds,
    'User-Agent': 'Mozilla/5.0'
})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print(json.dumps(data, indent=2))
except Exception as e:
    print("Error calling inspect-system:", e)
