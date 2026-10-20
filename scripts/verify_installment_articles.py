import sys
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

article_ids = [3851, 3853, 3855, 3857, 3859, 3861]

print("=== Verification of All 6 Installment Articles ===")
for pid in article_ids:
    url = f"https://hosseinykala.ir/wp-json/wp/v2/posts/{pid}"
    r = requests.get(url, auth=AUTH, headers=HEADERS, timeout=20)
    if r.status_code == 200:
        p = r.json()
        print(f"ID: {p['id']} | Status: {p['status']} | Date: {p['date']} | Featured Media: {p['featured_media']} | Slug: {p['slug']}")
        print(f"  Title: {p['title']['rendered']}")
        print(f"  Link: {p['link']}")
        print(f"  Categories: {p['categories']}")
        print(f"  Tags: {len(p['tags'])} tags")
        print("-" * 60)
    else:
        print(f"Error fetching ID {pid}: HTTP {r.status_code}")
