import requests

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0'}

# Let's inspect options through Snippet 4 or register a route in Snippet 4 to inspect options
# Notice in Snippet 4, register_rest_route is used. Let's see what routes exist or read options
r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/settings', auth=auth, headers=headers, timeout=10)
print("Settings status:", r.status_code)
