import requests
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

with open('data/all_link_replacements.json', encoding='utf-8') as f:
    replacements = json.load(f)

r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/posts?per_page=100&status=any', auth=AUTH, headers=HEADERS)
posts = r.json()

print(f"Total posts fetched: {len(posts)}\n")

total_changes = 0
posts_to_update = {}

for p in posts:
    pid = p['id']
    title = p['title'].get('rendered', '')
    content = p.get('content', {}).get('raw') or p.get('content', {}).get('rendered', '')
    
    new_content = content
    post_changes = []
    
    for old_url, new_url in replacements.items():
        if old_url in new_content:
            count = new_content.count(old_url)
            post_changes.append((old_url, new_url, count))
            new_content = new_content.replace(old_url, new_url)
    
    # Special fix for post 3217 where ?product_cat=123 was used for "دسته‌بندی سرخ کن"
    # 123 is actually مخلوط کن, and 121 is سرخ کن
    if pid == 3217 and "دسته‌بندی سرخ کن" in new_content:
        old_bad = "https://hosseinykala.ir/product-category/%d9%85%d8%ae%d9%84%d9%88%d8%b7-%da%a9%d9%86/"
        fryer_url = "https://hosseinykala.ir/product-category/%d8%b3%d8%b1%d8%ae-%da%a9%d9%86/"
        if old_bad in new_content:
            new_content = new_content.replace(old_bad, fryer_url)
            post_changes.append((old_bad, fryer_url, 1))

    if post_changes:
        posts_to_update[pid] = {
            'title': title,
            'changes': post_changes,
            'new_content': new_content
        }
        total_changes += sum(c[2] for c in post_changes)
        print(f"Post [{pid}] {title[:40]}... -> {len(post_changes)} link rules matched:")
        for old, new, count in post_changes:
            print(f"   ({count}x) {old}  ===>  {new}")

print(f"\n==========================================")
print(f"Summary: {len(posts_to_update)} posts will be updated with {total_changes} total link replacements.")
