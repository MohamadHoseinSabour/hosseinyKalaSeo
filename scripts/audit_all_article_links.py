import re
import requests

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

article_ids = [3851, 3853, 3855, 3857, 3859, 3861]
all_links = set()

for pid in article_ids:
    r = requests.get(f'https://hosseinykala.ir/wp-json/wp/v2/posts/{pid}', auth=AUTH, headers=HEADERS)
    if r.status_code == 200:
        content = r.json()['content']['raw'] if 'raw' in r.json()['content'] else r.json()['content']['rendered']
        links = re.findall(r'href=["\'](https?://[^"\']+)["\']', content)
        print(f"Post {pid} has {len(links)} links.")
        for l in links:
            all_links.add(l)

print(f"\nUnique links to test: {len(all_links)}")
for link in sorted(all_links):
    try:
        r = requests.get(link, headers=HEADERS, timeout=10, allow_redirects=True)
        status = r.status_code
        print(f"[{status}] {link} -> (Final: {r.url})")
    except Exception as e:
        print(f"[ERR] {link} -> {e}")
