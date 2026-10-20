import requests
from requests.auth import HTTPBasicAuth

resp = requests.get('https://hosseinykala.ir/wp-json/wc/v3/products/3546', auth=HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto'), timeout=30)
print("Status:", resp.status_code)
if resp.status_code == 200:
    data = resp.json()
    print("Name:", data.get('name'))
    print("Slug:", data.get('slug'))
    print("Permalink:", data.get('permalink'))
    print("Categories:", data.get('categories'))
    print("Attributes:", data.get('attributes'))
    print("Description:", data.get('description'))
else:
    print("Error:", resp.text[:200])
