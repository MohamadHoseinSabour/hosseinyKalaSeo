import requests
import json

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0'}

r = requests.get('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/5', auth=auth, headers=headers, timeout=10)
s5 = r.json()
with open('scratch/snippet5_current.php', 'w', encoding='utf-8') as f:
    f.write(s5.get('code', ''))

print("Saved current snippet 5. Length:", len(s5.get('code', '')))
