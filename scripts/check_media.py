import requests

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}
r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/media?per_page=10', auth=AUTH, headers=HEADERS, timeout=20)
if r.status_code == 200:
    for m in r.json():
        print(f"ID: {m['id']} | Slug: {m['slug']} | Title: {m['title']['rendered']}")
else:
    print(f"HTTP {r.status_code}: {r.text[:200]}")
