import sys
import requests
from requests.auth import HTTPBasicAuth

sys.stdout.reconfigure(encoding='utf-8')

auth = HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
base_url = 'https://hosseinykala.ir/wp-json/wc/v3/products/'

pids = [4085, 4402, 4127, 4442]
for pid in pids:
    res = requests.get(base_url + str(pid), auth=auth, timeout=15)
    if res.status_code == 200:
        d = res.json()
        print(f"PID {pid}: status={d.get('status')}, stock={d.get('stock_status')}, price={d.get('price')}, name={d.get('name')[:30]}")
    else:
        print(f"PID {pid}: HTTP {res.status_code}")
