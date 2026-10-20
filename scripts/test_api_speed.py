import sys
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

print("Testing tags fetch...", flush=True)
r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/tags?per_page=100', auth=AUTH, headers=HEADERS, timeout=15)
print(f"Status: {r.status_code}, tags count: {len(r.json())}", flush=True)

print("Testing post search...", flush=True)
r2 = requests.get('https://hosseinykala.ir/wp-json/wp/v2/posts?slug=home-appliances-installment-buying-guide&status=any', auth=AUTH, headers=HEADERS, timeout=15)
print(f"Status: {r2.status_code}, posts found: {len(r2.json())}", flush=True)
