import requests
import json
import sys
from concurrent.futures import ThreadPoolExecutor

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/json'
}

BASE_URL = 'https://hosseinykala.ir/wp-json/wp/v2/menu-items'

# Target IDs:
# wash_id = 3825
# drink_id = 3826
# climate_id = 3827

wash_id = 3825
drink_id = 3826
climate_id = 3827

updates = [
    # --- 1. یخچال فریزر (Root 1) ---
    (3749, 0, 1, None),
    (3753, 3749, 2, None), # کلور
    (3752, 3749, 3, None), # دیپوینت
    (3751, 3749, 4, None), # ایستکول
    (3750, 3749, 5, None), # الکترواستیل

    # --- 2. شستشو و نظافت (Root 2) ---
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

    # --- 3. لوازم برقی و پخت و پز آشپزخانه (Root 3) ---
    (3741, 0, 18, 'لوازم برقی و پخت و پز'), # لوازم برقی آشپزخانه
    (3729, 3741, 19, None), # سرخ کن
    (3730, 3729, 20, None), # سرخ کن دونالکس
    (3739, 3741, 21, None), # گوشت کوب برقی
    (3740, 3739, 22, None), # گوشت کوب دونالکس
    (3716, 3741, 23, None), # اجاق گاز
    (3738, 3716, 24, None), # گاز صفحه ای
    (3734, 3741, 25, None), # ظروف و پخت و پز

    # --- 4. نوشیدنی ساز (Root 4) ---
    (drink_id, 0, 26, 'نوشیدنی ساز'),
    (3717, drink_id, 27, None), # اسپرسو ساز
    (3718, 3717, 28, None), # اسپرسو دونالکس
    (3728, drink_id, 29, None), # چای ساز
    (3712, drink_id, 30, None), # آبمیوه گیری
    (3713, 3712, 31, None), # آبمیوه گیری دونالکس
    (3747, drink_id, 32, None), # مخلوط کن
    (3748, 3747, 33, None), # مخلوط کن دونالکس

    # --- 5. سرمایش و گرمایش (Root 5) ---
    (climate_id, 0, 34, 'سرمایش و گرمایش'),
    (3735, climate_id, 35, None), # کولر آبی
    (3736, 3735, 36, None), # کولر آبی ریتون
    (3737, climate_id, 37, None), # کولر گازی
    (3733, climate_id, 38, None), # صوتی تصویری و گرمایشی

    # --- 6. دستگاه تصفیه آب (Root 6) ---
    (3722, 0, 39, None), # تصفیه کننده آب
    (3723, 3722, 40, None), # تصفیه آب سافت واتر

    # --- 7. زیبایی و سلامت فردی (Root 7) ---
    (3721, 0, 41, 'زیبایی و سلامت فردی'), # اصلاح و زیبایی
    (3719, 3721, 42, None), # اصلاح موی سر و صورت
    (3720, 3719, 43, None), # اصلاح مو پرو امگا
    (3731, 3721, 44, None), # سشوار
    (3732, 3731, 45, None), # سشوار پرو امگا
]

def update_single_item(up):
    item_id, parent_id, menu_order, custom_title = up
    payload = {
        'parent': parent_id,
        'menu_order': menu_order
    }
    if custom_title:
        payload['title'] = custom_title

    for attempt in range(3):
        try:
            r = requests.post(f"{BASE_URL}/{item_id}", auth=AUTH, headers=HEADERS, json=payload, timeout=15)
            if r.status_code == 200:
                print(f"[OK] ID {item_id} -> Parent: {parent_id}, Order: {menu_order}", flush=True)
                return True
            else:
                print(f"[RETRY {attempt+1}] ID {item_id}: {r.status_code}", flush=True)
        except Exception as e:
            print(f"[ERROR {attempt+1}] ID {item_id}: {e}", flush=True)
    return False

def main():
    print(f"Updating {len(updates)} menu items in parallel...", flush=True)
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(update_single_item, updates))
    
    success = sum(1 for r in results if r)
    failed = sum(1 for r in results if not r)
    print(f"\nAll Done! Succeeded: {success}, Failed: {failed}", flush=True)

if __name__ == '__main__':
    main()
