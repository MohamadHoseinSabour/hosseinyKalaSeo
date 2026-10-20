import requests
import json
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

# 1. Update Haversen TVs (IDs 3531, 3523, 3520)
tv_updates = [
    {
        'id': 3531,
        'title': 'تلویزیون ال ای دی ۷۵ اینچ هوشمند 4K هاورسن مدل Cinema HDR',
        'slug': 'haverson-75-inch-4k-smart-tv'
    },
    {
        'id': 3523,
        'title': 'تلویزیون ال ای دی ۶۵ اینچ هوشمند 4K هاورسن مدل Frameless IPS',
        'slug': 'haverson-65-inch-4k-smart-tv'
    },
    {
        'id': 3520,
        'title': 'تلویزیون ال ای دی ۵۵ اینچ هوشمند 4K هاورسن مدل Smart Android',
        'slug': 'haverson-55-inch-4k-smart-tv'
    }
]

print("=== UPDATING HAVERSEN TVS ON SITE ===")
for item in tv_updates:
    pid = item['id']
    # Fetch existing content to replace 'هاورسون' with 'هاورسن'
    r_get = requests.get(f'https://hosseinykala.ir/wp-json/wp/v2/product/{pid}?context=edit', auth=auth, headers=headers, timeout=30)
    if r_get.status_code == 200:
        data = r_get.json()
        content = data.get('content', {}).get('raw', '')
        excerpt = data.get('excerpt', {}).get('raw', '')
        
        # Replace هاورسون with هاورسن
        content = content.replace('هاورسون', 'هاورسن')
        excerpt = excerpt.replace('هاورسون', 'هاورسن')
        
        payload = {
            'title': item['title'],
            'slug': item['slug'],
            'content': content,
            'excerpt': excerpt
        }
        r_post = requests.post(f'https://hosseinykala.ir/wp-json/wp/v2/product/{pid}', auth=auth, headers=headers, json=payload, timeout=30)
        if r_post.status_code in [200, 201]:
            print(f"SUCCESS {pid}: {item['title']}")
        else:
            print(f"ERROR {pid}: {r_post.text[:150]}")
    else:
        print(f"GET ERROR {pid}: {r_get.status_code}")

# 2. Update Kenra Vegetable Chopper (ID 4099)
print("\n=== UPDATING KENRA VEGETABLE CHOPPER ON SITE (ID 4099) ===")
r_get = requests.get('https://hosseinykala.ir/wp-json/wp/v2/product/4099?context=edit', auth=auth, headers=headers, timeout=30)
if r_get.status_code == 200:
    data = r_get.json()
    content = data.get('content', {}).get('raw', '')
    excerpt = data.get('excerpt', {}).get('raw', '')
    
    # Replace 'متفرقه' brand in table with 'کنرا (KENRA)'
    content = content.replace('<td>متفرقه</td>', '<td>کنرا (KENRA)</td>')
    content = content.replace('برند <strong>متفرقه</strong>', 'برند <strong>کنرا (KENRA)</strong>')
    content = content.replace('سبزی خردکن KENRA', 'سبزی خردکن خانگی کنرا مدل KENRA')
    excerpt = excerpt.replace('سبزی خردکن KENRA', 'سبزی خردکن خانگی کنرا مدل KENRA')
    
    payload = {
        'title': 'سبزی خردکن خانگی کنرا مدل KENRA',
        'slug': 'kenra-vegetable-chopper',
        'content': content,
        'excerpt': excerpt
    }
    r_post = requests.post('https://hosseinykala.ir/wp-json/wp/v2/product/4099', auth=auth, headers=headers, json=payload, timeout=30)
    if r_post.status_code in [200, 201]:
        print("SUCCESS 4099: سبزی خردکن خانگی کنرا مدل KENRA")
    else:
        print(f"ERROR 4099: {r_post.text[:150]}")
