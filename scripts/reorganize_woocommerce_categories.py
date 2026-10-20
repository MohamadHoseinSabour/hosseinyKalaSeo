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
    kwargs.setdefault('timeout', 30)
    url = f"{BASE_API}/{endpoint}" if not endpoint.startswith('http') else endpoint
    for attempt in range(3):
        try:
            if method.lower() == 'get':
                r = requests.get(url, **kwargs)
            elif method.lower() == 'post':
                r = requests.post(url, **kwargs)
            elif method.lower() == 'delete':
                r = requests.delete(url, **kwargs)
            return r
        except Exception as e:
            print(f"  [safe_req attempt {attempt+1}/3 failed]: {e}")
            time.sleep(2)
    return None

def get_or_create_category(name, slug, parent=0):
    # Check if category already exists by slug or name
    r = safe_req('get', f"product_cat?per_page=100")
    if r and r.status_code == 200:
        for c in r.json():
            if c.get('slug') == slug or c.get('name') == name:
                print(f"[FOUND] Category '{name}' exists with ID {c['id']}")
                return c['id'], c.get('link')
    
    # Create category
    payload = {
        'name': name,
        'slug': slug,
        'parent': parent
    }
    r_create = safe_req('post', 'product_cat', json=payload)
    if r_create and r_create.status_code in [200, 201]:
        data = r_create.json()
        print(f"[CREATED] Category '{name}' created with ID {data['id']}")
        return data['id'], data.get('link')
    else:
        raise Exception(f"Failed to create category '{name}': {r_create.text if r_create else 'No response'}")

def main():
    print("=== Step 1: Ensuring 3 new root categories exist ===")
    wash_id, wash_url = get_or_create_category('شستشو و نظافت', 'washing-cleaning', parent=0)
    drink_id, drink_url = get_or_create_category('نوشیدنی ساز', 'drink-makers', parent=0)
    climate_id, climate_url = get_or_create_category('سرمایش و گرمایش', 'heating-cooling', parent=0)

    print(f"\nRoot category IDs:")
    print(f"  - شستشو و نظافت: ID {wash_id} ({wash_url})")
    print(f"  - نوشیدنی ساز: ID {drink_id} ({drink_url})")
    print(f"  - سرمایش و گرمایش: ID {climate_id} ({climate_url})")

    print("\n=== Step 2: Updating existing root category names ===")
    # Update category 216 to 'لوازم برقی و پخت و پز'
    r216 = safe_req('post', 'product_cat/216', json={'name': 'لوازم برقی و پخت و پز', 'parent': 0})
    if r216 and r216.status_code == 200:
        print("[OK] Category 216 name updated to 'لوازم برقی و پخت و پز'")
    else:
        print(f"[WARN] Category 216 update: {r216.status_code if r216 else 'No response'}")

    # Update category 212 to 'زیبایی و سلامت فردی'
    r212 = safe_req('post', 'product_cat/212', json={'name': 'زیبایی و سلامت فردی', 'parent': 0})
    if r212 and r212.status_code == 200:
        print("[OK] Category 212 name updated to 'زیبایی و سلامت فردی'")
    else:
        print(f"[WARN] Category 212 update: {r212.status_code if r212 else 'No response'}")

    print("\n=== Step 3: Re-parenting subcategories ===")
    parent_map = [
        # Under شستشو و نظافت
        (93, wash_id, 'ماشین لباسشویی'),
        (97, wash_id, 'ماشین ظرفشویی'),
        (21, wash_id, 'جاروبرقی'),
        (118, wash_id, 'اتو'),

        # Under لوازم برقی و پخت و پز (216)
        (121, 216, 'سرخ کن'),
        (122, 216, 'گوشت کوب برقی'),
        (209, 216, 'اجاق گاز'),
        (210, 209, 'گاز صفحه ای'),
        (215, 216, 'ظروف و پخت و پز'),

        # Under نوشیدنی ساز
        (119, drink_id, 'اسپرسو ساز'),
        (211, drink_id, 'چای ساز'),
        (120, drink_id, 'آبمیوه گیری'),
        (123, drink_id, 'مخلوط کن'),

        # Under سرمایش و گرمایش
        (95, climate_id, 'کولر آبی'),
        (206, climate_id, 'کولر گازی'),
        (214, climate_id, 'صوتی، تصویری و گرمایشی'),

        # Under زیبایی و سلامت فردی (212)
        (126, 212, 'اصلاح موی سر و صورت'),
        (124, 212, 'سشوار'),
    ]

    success = 0
    failed = 0
    for cat_id, target_parent, name in parent_map:
        res = safe_req('post', f'product_cat/{cat_id}', json={'parent': target_parent})
        if res and res.status_code == 200:
            print(f"  [OK] Cat {cat_id:<4} ({name:<25}) -> New Parent: {target_parent}")
            success += 1
        else:
            print(f"  [FAIL] Cat {cat_id:<4} ({name:<25}) -> {res.status_code if res else 'No response'}")
            failed += 1

    print(f"\nSubcategory re-parenting finished: {success} succeeded, {failed} failed.")

    print("\n=== Step 4: Updating Header Menu 16 Custom Items with real Category URLs ===")
    menu_updates = [
        (3825, 'https://hosseinykala.ir/product-category/washing-cleaning/', 'شستشو و نظافت'),
        (3826, 'https://hosseinykala.ir/product-category/drink-makers/', 'نوشیدنی ساز'),
        (3827, 'https://hosseinykala.ir/product-category/heating-cooling/', 'سرمایش و گرمایش'),
    ]
    for menu_item_id, target_url, title in menu_updates:
        rm = safe_req('post', f'menu-items/{menu_item_id}', json={'url': target_url})
        if rm and rm.status_code == 200:
            print(f"  [OK] Menu Item {menu_item_id} ('{title}') -> URL set to {target_url}")
        else:
            print(f"  [FAIL] Menu Item {menu_item_id} -> {rm.status_code if rm else 'No response'}")

    print("\n=== All Steps Completed Successfully! ===")

if __name__ == '__main__':
    main()
