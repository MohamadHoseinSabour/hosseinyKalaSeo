import requests
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

with open('data/all_link_replacements.json', encoding='utf-8') as f:
    replacements = json.load(f)

# Sort replacements by length of old_url descending so more specific URLs are replaced first
sorted_replacements = sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True)

r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/posts?per_page=100&status=any', auth=AUTH, headers=HEADERS)
posts = r.json()
print(f"Total posts fetched: {len(posts)}\n", flush=True)

success_count = 0
skip_count = 0
fail_count = 0

for p in posts:
    pid = p['id']
    title = p['title'].get('rendered', '')
    content = p.get('content', {}).get('raw') or p.get('content', {}).get('rendered', '')
    
    new_content = content
    replaced_items = []
    
    for old_url, new_url in sorted_replacements:
        if old_url in new_content:
            count = new_content.count(old_url)
            new_content = new_content.replace(old_url, new_url)
            replaced_items.append((old_url, new_url, count))
            
    # Fix post 3217 typo if present
    if pid == 3217 and "دسته‌بندی سرخ کن" in new_content:
        old_bad = "https://hosseinykala.ir/product-category/%d9%85%d8%ae%d9%84%d9%88%d8%b7-%da%a9%d9%86/"
        fryer_url = "https://hosseinykala.ir/product-category/%d8%b3%d8%b1%d8%ae-%da%a9%d9%86/"
        if old_bad in new_content:
            new_content = new_content.replace(old_bad, fryer_url)
            replaced_items.append((old_bad, fryer_url, 1))

    if replaced_items:
        total_sub = sum(x[2] for x in replaced_items)
        print(f"Updating Post [{pid}] {title[:35]}... ({total_sub} links)", flush=True)
        update_url = f"https://hosseinykala.ir/wp-json/wp/v2/posts/{pid}"
        payload = {'content': new_content}
        
        try:
            up_res = requests.post(update_url, auth=AUTH, headers=HEADERS, json=payload, timeout=25)
            if up_res.status_code == 200:
                print(f"  -> [SUCCESS] Post {pid} updated successfully.", flush=True)
                success_count += 1
            else:
                print(f"  -> [FAIL] Post {pid}: HTTP {up_res.status_code} - {up_res.text[:100]}", flush=True)
                fail_count += 1
        except Exception as e:
            print(f"  -> [ERROR] Post {pid}: {e}", flush=True)
            fail_count += 1
        
        time.sleep(0.5)
    else:
        skip_count += 1

print(f"\n==========================================", flush=True)
print(f"Update Summary: {success_count} posts updated, {skip_count} skipped, {fail_count} failed.", flush=True)
