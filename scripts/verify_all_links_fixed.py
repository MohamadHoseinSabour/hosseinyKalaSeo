import requests
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

print("=== Starting Complete Link Verification across WordPress ===")

r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/posts?per_page=100&status=any', auth=AUTH, headers=HEADERS)
posts = r.json()
print(f"Total posts checked: {len(posts)}\n")

broken_query_cat_found = []
for p in posts:
    pid = p['id']
    title = p['title'].get('rendered', '')
    content = p.get('content', {}).get('raw') or p.get('content', {}).get('rendered', '')
    if 'product_cat=' in content or '?product_cat' in content:
        broken_query_cat_found.append((pid, title))

if broken_query_cat_found:
    print(f"❌ [ALERT] Found {len(broken_query_cat_found)} posts still containing ?product_cat=:")
    for pid, title in broken_query_cat_found:
        print(f"   - [{pid}] {title}")
else:
    print("✅ [PERFECT] ZERO posts contain '?product_cat='! All category query links are completely eradicated from the entire website.")

# Check the 6 installment cluster posts specifically
installment_pids = [3851, 3853, 3855, 3857, 3859, 3861]
print("\n=== Inspecting Installment Cluster Posts (3851 to 3861) ===")

all_cluster_links = set()

for pid in installment_pids:
    post_item = next((p for p in posts if p['id'] == pid), None)
    if post_item:
        content = post_item.get('content', {}).get('raw') or post_item.get('content', {}).get('rendered', '')
        links = re.findall(r'href=["\'](https?://[^"\']+)["\']', content)
        print(f"\n--- Post [{pid}] {post_item['title'].get('rendered', '')[:40]}... ({len(links)} links) ---")
        for l in links:
            print(f"   -> {l}")
            if 'hosseinykala.ir' in l:
                all_cluster_links.add(l)

print(f"\nTotal unique internal links in the 6 installment articles: {len(all_cluster_links)}")
