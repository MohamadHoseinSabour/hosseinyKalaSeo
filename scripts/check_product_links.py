import requests
import json

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

products_to_check = [2972, 3707, 2745, 2766, 2871]
for pid in products_to_check:
    url = f"https://hosseinykala.ir/?p={pid}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        print(f"Product ?p={pid} -> HTTP {r.status_code} | Final: {r.url}")
    except Exception as e:
        print(f"Product ?p={pid} -> Error: {e}")

# Check real direct URLs from products.json and id_mappings.json
with open('data/id_mappings.json', encoding='utf-8') as f:
    id_map = json.load(f)

for pid in products_to_check:
    str_pid = str(pid)
    if str_pid in id_map:
        info = id_map[str_pid]
        direct_url = f"https://hosseinykala.ir/product/{info['slug']}/"
        try:
            r = requests.get(direct_url, headers=HEADERS, timeout=10)
            print(f"Direct Product {pid} ({info['slug']}) -> HTTP {r.status_code} | Final: {r.url}")
        except Exception as e:
            print(f"Direct Product {pid} -> Error: {e}")
    else:
        print(f"ID {pid} NOT in id_mappings.json!")
