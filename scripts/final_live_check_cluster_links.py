import requests
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

installment_ids = [3851, 3853, 3855, 3857, 3859, 3861]

unique_urls = set()

for pid in installment_ids:
    r = requests.get(f'https://hosseinykala.ir/wp-json/wp/v2/posts/{pid}', auth=AUTH, headers=HEADERS)
    if r.status_code == 200:
        data = r.json()
        content = data.get('content', {}).get('raw') or data.get('content', {}).get('rendered', '')
        links = re.findall(r'href=["\'](https?://[^"\']+)["\']', content)
        for l in links:
            unique_urls.add(l)

print(f"Total unique URLs in the 6 installment articles: {len(unique_urls)}")
print("Testing each URL live (with 25s timeout)...\n")

results = []
for url in sorted(unique_urls):
    try:
        # For scheduled posts, anonymous visitors will get 404 until published date, 
        # so let's check whether it's a post slug or category or product
        res = requests.get(url, headers=HEADERS, timeout=25, allow_redirects=True)
        status = res.status_code
        print(f"[{status}] {url} -> (Final: {res.url})", flush=True)
        results.append({'url': url, 'status': status, 'final': res.url})
    except Exception as e:
        print(f"[ERR] {url} -> {e}", flush=True)
        results.append({'url': url, 'status': 'ERR', 'error': str(e)})

with open('data/final_live_check_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
