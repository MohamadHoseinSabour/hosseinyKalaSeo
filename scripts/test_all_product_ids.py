import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

product_ids = [
    2745, 2972, 2871, 2766, 2538, 2559, 3065, 3056, 3016, 3013, 
    3026, 2594, 2585, 2445, 2579, 2885, 2505, 2497, 2704, 2691, 
    2431, 2510, 2637, 2680
]

# Also load data/id_mappings.json to compare
with open('data/id_mappings.json', encoding='utf-8') as f:
    mappings = json.load(f)

results = []

for pid in product_ids:
    spid = str(pid)
    mapping_info = mappings.get(spid)
    shortlink = f"https://hosseinykala.ir/?p={pid}"
    try:
        r = requests.get(shortlink, headers=HEADERS, timeout=15, allow_redirects=False)
        status = r.status_code
        loc = r.headers.get('Location', '')
        print(f"Product {pid}: Status={status} -> Location={loc}")
        results.append({
            'id': pid,
            'status': status,
            'location': loc,
            'mapping': mapping_info
        })
    except Exception as e:
        print(f"Product {pid}: ERROR -> {e}")

with open('data/product_link_test_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
