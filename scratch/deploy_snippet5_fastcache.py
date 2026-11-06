import urllib.request
import base64
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

creds = base64.b64encode(b'agent:Mlwg pHHX NQ64 drrz 7ca2 IVto').decode('utf-8')

with open('scratch/test_snippet5_code.php', 'r', encoding='utf-8') as f:
    code = f.read()

# Strip <?php from start if present because Code Snippets doesn't use <?php
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

print("Deploying updated Snippet 5...")
with urllib.request.urlopen(req, timeout=20) as resp:
    res = json.loads(resp.read().decode('utf-8'))
    print("Snippet 5 updated successfully! ID:", res.get('id'), "Active:", res.get('active'))

# Purge old cache
purge_req = urllib.request.Request(
    'https://hosseinykala.ir/wp-json/hk-perf/v1/purge-all',
    headers={'Authorization': 'Basic ' + creds},
    data=b'{}'
)
with urllib.request.urlopen(purge_req, timeout=20) as resp:
    print("Purge response:", resp.read().decode('utf-8'))
