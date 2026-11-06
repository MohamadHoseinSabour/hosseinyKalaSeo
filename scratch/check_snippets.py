import requests
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0'}

r = requests.get('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets', auth=auth, headers=headers)
print('Code snippets status:', r.status_code)
if r.status_code == 200:
    snippets = r.json()
    print(f'Total snippets: {len(snippets)}')
    for s in snippets:
        print(f"ID: {s.get('id')} | Name: {s.get('name')} | Active: {s.get('active')} | Scope: {s.get('scope')}")
        code = s.get('code', '')
        if 'session' in code.lower():
            print(f"  >>> ALERT: session found in snippet {s.get('id')} ({s.get('name')}):")
            print(code[:200])
else:
    print('Snippet response:', r.text[:200])
