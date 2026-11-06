import requests
import json

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
# Read options via WP REST API or let's check options endpoint
r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/settings', auth=auth, timeout=15)
print("Settings status:", r.status_code)
