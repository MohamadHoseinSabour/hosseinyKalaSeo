import urllib.request
import base64
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

creds = base64.b64encode(b'agent:Mlwg pHHX NQ64 drrz 7ca2 IVto').decode('utf-8')

with open('scratch/snippet5_complete_engine.php', 'r', encoding='utf-8') as f:
    code = f.read()

if code.startswith('<?php'):
    code = code[5:].lstrip()

update_payload = json.dumps({'code': code}).encode('utf-8')
req = urllib.request.Request(
    'https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/5',
    headers={
        'Authorization': 'Basic ' + creds,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    },
    data=update_payload,
    method='POST'
)

print("Deploying Master Snippet 5 Engine (timeout=50)...")
try:
    with urllib.request.urlopen(req, timeout=50) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print("Master Snippet 5 updated successfully! ID:", res.get('id'), "Active:", res.get('active'))
except Exception as e:
    print("Update error:", e)
