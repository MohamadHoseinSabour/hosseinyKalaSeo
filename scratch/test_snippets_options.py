import requests

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# Test GET schema or OPTIONS on /wp-json/code-snippets/v1/snippets
r = requests.options('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/4', auth=auth, headers=headers, timeout=10)
print("OPTIONS status:", r.status_code, "Allow:", r.headers.get('Allow'))
