import requests
import json
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/json'
}

BASE_API = 'https://hosseinykala.ir/wp-json/wp/v2'

def safe_req(method, endpoint, **kwargs):
    kwargs.setdefault('auth', AUTH)
    kwargs.setdefault('headers', HEADERS)
    kwargs.setdefault('timeout', 45)
    url = f"{BASE_API}/{endpoint}" if not endpoint.startswith('http') else endpoint
    for attempt in range(3):
        try:
            if method.lower() == 'get':
                return requests.get(url, **kwargs)
            elif method.lower() == 'post':
                return requests.post(url, **kwargs)
        except Exception as e:
            print(f"  [Attempt {attempt+1}/3 failed]: {e}")
            time.sleep(2)
    return None

def main():
    print("=== Step 1: Create 'صوتی و تصویری' and 'تلویزیون' Categories ===")
    
    # Check if 'صوتی و تصویری' exists
    r_cats = safe_req('get', 'product_cat?per_page=100')
    existing_cats = r_cats.json() if r_cats and r_cats.status_code == 200 else []
    
    av_cat = next((c for c in existing_cats if c['name'] == 'صوتی و تصویری' or c['slug'] == 'audio-video'), None)
    if av_cat:
        av_id = av_cat['id']
        print(f"[EXISTS] Category 'صوتی و تصویری' exists with ID: {av_id}")
    else:
        payload = {'name': 'صوتی و تصویری', 'slug': 'audio-video', 'parent': 0}
        r = safe_req('post', 'product_cat', json=payload)
        av_data = r.json()
        av_id = av_data['id']
        print(f"[CREATED] Category 'صوتی و تصویری' created with ID: {av_id}")

    # Check if 'تلویزیون' exists
    tv_cat = next((c for c in existing_cats if c['name'] == 'تلویزیون' or c['slug'] == 'television'), None)
    if tv_cat:
        tv_id = tv_cat['id']
        print(f"[EXISTS] Category 'تلویزیون' exists with ID: {tv_id}")
        # Ensure parent is av_id
        if tv_cat.get('parent') != av_id:
            safe_req('post', f'product_cat/{tv_id}', json={'parent': av_id})
            print(f"  [UPDATED] 'تلویزیون' parent set to {av_id}")
    else:
        payload = {'name': 'تلویزیون', 'slug': 'television', 'parent': av_id}
        r = safe_req('post', 'product_cat', json=payload)
        tv_data = r.json()
        tv_id = tv_data['id']
        print(f"[CREATED] Category 'تلویزیون' created with ID: {tv_id} under 'صوتی و تصویری'")

    # Step 2: Update category 214 name from 'صوتی، تصویری و گرمایشی' to 'پنکه و گرمایشی'
    print("\n=== Step 2: Updating Category 214 Name ===")
    r214 = safe_req('post', 'product_cat/214', json={'name': 'پنکه و گرمایشی', 'parent': 241})
    if r214 and r214.status_code == 200:
        print("[OK] Category 214 renamed to 'پنکه و گرمایشی' under 'سرمایش و گرمایش' (241)")

    # Step 3: Move all 5 TVs to [av_id, tv_id]
    tv_pids = [3516, 3520, 3523, 3531, 3534]
    print(f"\n=== Step 3: Moving 5 TVs to [صوتی و تصویری: {av_id}, تلویزیون: {tv_id}] ===")
    for pid in tv_pids:
        r_prod = safe_req('post', f'product/{pid}', json={'product_cat': [av_id, tv_id]})
        if r_prod and r_prod.status_code == 200:
            print(f"  [OK] TV Product #{pid} moved to categories: {r_prod.json().get('product_cat')}")
        else:
            print(f"  [FAIL] TV Product #{pid}: {r_prod.status_code if r_prod else 'No response'}")

    # Ensure Fan 3540 is in category 214
    r_fan = safe_req('post', 'product/3540', json={'product_cat': [214]})
    if r_fan and r_fan.status_code == 200:
        print(f"  [OK] Fan Product #3540 kept in category 214 (پنکه و گرمایشی)")

    # Step 4: Update Menu 16 (Header Menu)
    print("\n=== Step 4: Updating Menu 16 ===")
    # 1. Update item 3733 title in menu 16
    r_m3733 = safe_req('post', 'menu-items/3733', json={'title': 'پنکه و گرمایشی'})
    if r_m3733 and r_m3733.status_code == 200:
        print("[OK] Menu Item 3733 title updated to 'پنکه و گرمایشی'")

    # 2. Check if 'صوتی و تصویری' menu item already exists in menu 16
    r_m_items = safe_req('get', 'menu-items?menus=16&per_page=100')
    menu_items = r_m_items.json() if r_m_items and r_m_items.status_code == 200 else []
    
    m_av = next((it for it in menu_items if 'صوتی' in (it.get('title', {}).get('raw') or it.get('title', {}).get('rendered', '')) and it.get('parent') == 0), None)
    if not m_av:
        # Create Root menu item for 'صوتی و تصویری'
        payload_m = {
            'title': 'صوتی و تصویری',
            'menus': 16,
            'status': 'publish',
            'type': 'custom',
            'url': f'https://hosseinykala.ir/product-category/audio-video/',
            'parent': 0,
            'menu_order': 38
        }
        r_new_m = safe_req('post', 'menu-items', json=payload_m)
        if r_new_m and r_new_m.status_code in [200, 201]:
            m_av_id = r_new_m.json()['id']
            print(f"[CREATED] Menu Item 'صوتی و تصویری' created with ID: {m_av_id}")
            
            # Create child menu item 'تلویزیون'
            payload_tv = {
                'title': 'تلویزیون',
                'menus': 16,
                'status': 'publish',
                'type': 'custom',
                'url': f'https://hosseinykala.ir/product-category/audio-video/television/',
                'parent': m_av_id,
                'menu_order': 39
            }
            safe_req('post', 'menu-items', json=payload_tv)
            print("[CREATED] Sub-menu Item 'تلویزیون' created under 'صوتی و تصویری'")
    else:
        print(f"[EXISTS] Menu Item 'صوتی و تصویری' exists with ID {m_av['id']}")

    print("\n=== Category & Menu Reorganization Finished Successfully! ===")

if __name__ == '__main__':
    main()
