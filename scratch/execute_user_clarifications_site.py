import requests
import json
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

# 1. Update Product 3662 (KST Kettle and Teapot)
print("=== 1. UPDATING PRODUCT 3662 (KST KETTLE & TEAPOT) ===")
r_get = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product/3662?context=edit', auth=auth, headers=headers, timeout=30)
if r_get.status_code == 200:
    data = r_get.json()
    content = data.get('content', {}).get('raw', '')
    excerpt = data.get('excerpt', {}).get('raw', '')
    
    new_title = 'کتری و قوری روگازی هرمی ۵ لیتری کی اس تی مدل 604 استیل طلا'
    new_slug = 'kst-604-pyramid-gold-kettle-teapot'
    
    # Replace brand references in content
    content = content.replace('متفرقه (Golden)', 'کی اس تی (KST)')
    content = content.replace('متفرقه', 'کی اس تی (KST)')
    content = content.replace('برند نام‌آشنای <strong>کی اس تی (KST)</strong>', 'برند باکیفیت <strong>کی اس تی (KST)</strong>')
    content = content.replace('کتری و قوری روگازی هرمی ۵ لیتری استیل طلا مدل 604', new_title)
    excerpt = excerpt.replace('کتری و قوری روگازی هرمی ۵ لیتری استیل طلا مدل 604', new_title)
    
    payload = {
        'title': new_title,
        'slug': new_slug,
        'content': content,
        'excerpt': excerpt
    }
    r_post = requests.post('https://hosseinykala.ir/wp-json/wp/v2/product/3662', auth=auth, headers=headers, json=payload, timeout=30)
    if r_post.status_code in [200, 201]:
        print(f"SUCCESS 3662: {new_title} (slug: {new_slug})")
    else:
        print(f"ERROR 3662: {r_post.text[:150]}")

# 2. Update Product 3354 (Dasti Luxe Cookware)
print("\n=== 2. UPDATING PRODUCT 3354 (DASTI LUXE COOKWARE) ===")
r_get = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product/3354?context=edit', auth=auth, headers=headers, timeout=30)
if r_get.status_code == 200:
    data = r_get.json()
    content = data.get('content', {}).get('raw', '')
    excerpt = data.get('excerpt', {}).get('raw', '')
    
    new_title_3354 = 'سرویس پخت و پز ۱۰ پارچه تمام استیل دستی لوکس اینداکشن'
    
    payload = {
        'title': new_title_3354
    }
    r_post = requests.post('https://hosseinykala.ir/wp-json/wp/v2/product/3354', auth=auth, headers=headers, json=payload, timeout=30)
    if r_post.status_code in [200, 201]:
        print(f"SUCCESS 3354: {new_title_3354}")
    else:
        print(f"ERROR 3354: {r_post.text[:150]}")

# 3. Delete Duplicate Product 4101
print("\n=== 3. DELETING DUPLICATE PRODUCT 4101 ===")
r_del = requests.delete('https://hosseinykala.ir/wp-json/wp/v2/product/4101?force=true', auth=auth, headers=headers, timeout=30)
print(f"DELETE 4101 Status: {r_del.status_code}")
if r_del.status_code in [200, 204]:
    print("SUCCESS: Product 4101 deleted permanently.")
else:
    print(f"DELETE Response: {r_del.text[:150]}")

# 4. Delete Draft Product 3840
print("\n=== 4. DELETING DRAFT PRODUCT 3840 ===")
r_del2 = requests.delete('https://hosseinykala.ir/wp-json/wp/v2/product/3840?force=true', auth=auth, headers=headers, timeout=30)
print(f"DELETE 3840 Status: {r_del2.status_code}")
if r_del2.status_code in [200, 204]:
    print("SUCCESS: Product 3840 deleted permanently.")
else:
    print(f"DELETE Response: {r_del2.text[:150]}")
