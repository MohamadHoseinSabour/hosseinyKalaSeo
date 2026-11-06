import requests
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0'}

try:
    r = requests.get('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/4', auth=auth, headers=headers, timeout=10)
    print("Snippet 4 status:", r.status_code)
    if r.status_code == 200:
        print("Snippet 4 code:\n", r.json().get('code', ''))
    else:
        print("Snippet 4 resp:", r.text[:200])
except Exception as e:
    print("Snippet 4 error:", e)

try:
    r5 = requests.get('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/5', auth=auth, headers=headers, timeout=10)
    print("\nSnippet 5 status:", r5.status_code)
    if r5.status_code == 200:
        print("Snippet 5 code:\n", r5.json().get('code', ''))
    else:
        print("Snippet 5 resp:", r5.text[:200])
except Exception as e:
    print("Snippet 5 error:", e)
