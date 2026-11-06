import requests

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# Check options or permissions
r = requests.get('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/4', auth=auth, headers=headers, timeout=10)
print("Snippet 4 GET status:", r.status_code)
