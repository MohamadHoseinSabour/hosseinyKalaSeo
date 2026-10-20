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

BASE_URL = 'https://hosseinykala.ir/wp-json/wp/v2/menu-items'

def safe_request(method, url, **kwargs):
    kwargs.setdefault('auth', AUTH)
    kwargs.setdefault('headers', HEADERS)
    kwargs.setdefault('timeout', 20)
    for attempt in range(3):
        try:
            if method.lower() == 'get':
                return requests.get(url, **kwargs)
            elif method.lower() == 'post':
                return requests.post(url, **kwargs)
            elif method.lower() == 'delete':
                return requests.delete(url, **kwargs)
        except Exception as e:
            print(f"  [Attempt {attempt+1}/3 failed]: {e}")
            time.sleep(2)
    return None

def get_or_create_custom_item(menu_id, title, url='#'):
    # Check if item with this title already exists in menu
    r = safe_request('get', f"{BASE_URL}?menus={menu_id}&per_page=100")
    if r and r.status_code == 200:
        for it in r.json():
            it_title = it.get('title', {}).get('raw') or it.get('title', {}).get('rendered', '')
            if it_title.strip() == title.strip() and it.get('type') == 'custom':
                print(f"[FOUND] Existing custom menu item '{title}' with ID {it['id']}")
                return it['id']
    
    # Create new custom item
    payload = {
        'title': title,
        'menus': menu_id,
        'status': 'publish',
        'type': 'custom',
        'url': url,
        'parent': 0
    }
    r_create = safe_request('post', BASE_URL, json=payload)
    if r_create and r_create.status_code in [200, 201]:
        new_id = r_create.json()['id']
        print(f"[CREATED] New custom menu item '{title}' with ID {new_id}")
        return new_id
    else:
        raise Exception(f"Failed to create menu item '{title}': {r_create.text if r_create else 'No response'}")

def main():
    print("=== Starting Menu 16 Reorganization ===")
    menu_id = 16

    # 1. Create or get container items
    wash_id = get_or_create_custom_item(menu_id, 'شستشو و نظافت')
    drink_id = get_or_create_custom_item(menu_id, 'نوشیدنی ساز')
    climate_id = get_or_create_custom_item(menu_id, 'سرمایش و گرمایش')

    # 2. Define the exact target structure: item_id -> (target_parent, target_order, optional_title)
    # Root items:
    # 3749: یخچال فریزر -> Parent: 0, Order: 1
    # wash_id: شستشو و نظافت -> Parent: 0, Order: 6
    # 3741: لوازم برقی آشپزخانه -> Parent: 0, Order: 18
    # drink_id: نوشیدنی ساز -> Parent: 0, Order: 26
    # climate_id: سرمایش و گرمایش -> Parent: 0, Order: 34
    # 3722: تصفیه کننده آب -> Parent: 0, Order: 39
    # 3721: اصلاح و زیبایی -> Parent: 0, Order: 41

    updates = [
        # --- 1. یخچال فریزر ---
        (3749, 0, 1, None),
        (3753, 3749, 2, None), # کلور
        (3752, 3749, 3, None), # دیپوینت
        (3751, 3749, 4, None), # ایستکول
        (3750, 3749, 5, None), # الکترواستیل

        # --- 2. شستشو و نظافت ---
        (wash_id, 0, 6, 'شستشو و نظافت'),
        (3744, wash_id, 7, None), # ماشین لباسشویی
        (3746, 3744, 8, None), # لباسشویی کلور
        (3745, 3744, 9, None), # لباسشویی دوو
        (3742, wash_id, 10, None), # ماشین ظرفشویی
        (3743, 3742, 11, None), # ظرفشویی کلور
        (3724, wash_id, 12, None), # جاروبرقی
        (3725, 3724, 13, None), # جاروبرقی بست
        (3726, 3724, 14, None), # جاروبرقی پاناسونیک
        (3727, 3724, 15, None), # جاروبرقی هیتاچی
        (3714, wash_id, 16, None), # اتو
        (3715, 3714, 17, None), # اتو بخار دونالکس

        # --- 3. لوازم برقی و پخت و پز آشپزخانه ---
        (3741, 0, 18, 'لوازم برقی و پخت و پز'), # لوازم برقی آشپزخانه
        (3729, 3741, 19, None), # سرخ کن
        (3730, 3729, 20, None), # سرخ کن دونالکس
        (3739, 3741, 21, None), # گوشت کوب برقی
        (3740, 3739, 22, None), # گوشت کوب دونالکس
        (3716, 3741, 23, None), # اجاق گاز
        (3738, 3716, 24, None), # گاز صفحه ای
        (3734, 3741, 25, None), # ظروف و پخت و پز

        # --- 4. نوشیدنی ساز ---
        (drink_id, 0, 26, 'نوشیدنی ساز'),
        (3717, drink_id, 27, None), # اسپرسو ساز
        (3718, 3717, 28, None), # اسپرسو دونالکس
        (3728, drink_id, 29, None), # چای ساز
        (3712, drink_id, 30, None), # آبمیوه گیری
        (3713, 3712, 31, None), # آبمیوه گیری دونالکس
        (3747, drink_id, 32, None), # مخلوط کن
        (3748, 3747, 33, None), # مخلوط کن دونالکس

        # --- 5. سرمایش و گرمایش ---
        (climate_id, 0, 34, 'سرمایش و گرمایش'),
        (3735, climate_id, 35, None), # کولر آبی
        (3736, 3735, 36, None), # کولر آبی ریتون
        (3737, climate_id, 37, None), # کولر گازی
        (3733, climate_id, 38, None), # صوتی تصویری و گرمایشی

        # --- 6. دستگاه تصفیه آب ---
        (3722, 0, 39, None), # تصفیه کننده آب
        (3723, 3722, 40, None), # تصفیه آب سافت واتر

        # --- 7. زیبایی و بهداشت فردی ---
        (3721, 0, 41, 'زیبایی و بهداشت شخصی'), # اصلاح و زیبایی
        (3719, 3721, 42, None), # اصلاح موی سر و صورت
        (3720, 3719, 43, None), # اصلاح مو پرو امگا
        (3731, 3721, 44, None), # سشوار
        (3732, 3731, 45, None), # سشوار پرو امگا
    ]

    success_count = 0
    fail_count = 0

    print(f"\nApplying hierarchy updates to {len(updates)} menu items...")
    for item_id, parent_id, menu_order, custom_title in updates:
        payload = {
            'parent': parent_id,
            'menu_order': menu_order
        }
        if custom_title:
            payload['title'] = custom_title

        r_up = safe_request('post', f"{BASE_URL}/{item_id}", json=payload)
        if r_up and r_up.status_code == 200:
            data = r_up.json()
            title = data.get('title', {}).get('raw') or data.get('title', {}).get('rendered')
            print(f"  [OK] ID {item_id} ('{title}') -> Parent: {parent_id}, Order: {menu_order}")
            success_count += 1
        else:
            print(f"  [FAIL] ID {item_id}: {r_up.status_code if r_up else 'No response'} - {r_up.text[:100] if r_up else ''}")
            fail_count += 1

    print(f"\nFinished updating menu items: {success_count} succeeded, {fail_count} failed.")

if __name__ == '__main__':
    main()
