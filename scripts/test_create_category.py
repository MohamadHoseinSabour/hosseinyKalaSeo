import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Content-Type': 'application/json'
}

# Try to create a test category
test_payload = {
    'name': 'تست موقت',
    'slug': 'test-temporary-category'
}

r = requests.post('https://hosseinykala.ir/wp-json/wp/v2/product_cat', auth=AUTH, headers=headers, json=test_payload, timeout=15)
print(f"POST status: {r.status_code}")
if r.status_code in [200, 201]:
    cat = r.json()
    cat_id = cat['id']
    print(f"Created category ID: {cat_id}")
    
    # Try to delete it
    r_del = requests.delete(f"https://hosseinykala.ir/wp-json/wp/v2/product_cat/{cat_id}?force=true", auth=AUTH, headers=headers, timeout=15)
    print(f"DELETE status: {r_del.status_code}")
else:
    print(f"Failed to create: {r.text[:200]}")
