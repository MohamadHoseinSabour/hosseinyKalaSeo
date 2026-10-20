import requests
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Let's inspect products around 4080-4100
for pid in [4080, 4081, 4082, 4083, 4084, 4085, 4086, 4087, 4088, 4089, 4090, 4091, 4092, 4093, 4094, 4095, 4096, 4097, 4098, 4099, 4100]:
    try:
        res = requests.get(f'https://hosseinykala.ir/wp-json/wc/v3/products/{pid}', auth=AUTH, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            p = res.json()
            print(f"ID {pid}: {p.get('name')} | slug={p.get('slug')}")
    except Exception as e:
        pass
