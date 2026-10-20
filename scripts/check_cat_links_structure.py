import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# Let's inspect cat 153 (clover-refrigerators, parent: 92) and cat 93 (washing machine, parent: 0)
r1 = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product_cat/153', auth=AUTH, headers=headers)
r2 = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product_cat/93', auth=AUTH, headers=headers)

if r1.status_code == 200:
    c1 = r1.json()
    print("Cat 153 (child of 92):")
    print("  Link:", c1.get('link'))
    print("  Slug:", c1.get('slug'))

if r2.status_code == 200:
    c2 = r2.json()
    print("Cat 93 (root):")
    print("  Link:", c2.get('link'))
    print("  Slug:", c2.get('slug'))
