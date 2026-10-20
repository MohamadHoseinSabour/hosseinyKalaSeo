import requests
import json
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

BASE_API = 'https://hosseinykala.ir/wp-json/wp/v2/product'

updates = [
    {
        'id': 3516,
        'title': 'تلویزیون ال ای دی ۳۲ اینچ هاورسن مدل HD',
        'slug': 'haverson-32-inch-hd-led-tv'
    },
    {
        'id': 3534,
        'title': 'تلویزیون ال ای دی ۸۵ اینچ هوشمند 4K اسمارت هاورسن مدل Ultra HD',
        'slug': 'haverson-85-inch-4k-smart-tv'
    }
]

print("=" * 60)
print("به‌روزرسانی نام و اسلاگ تلویزیون‌های هاورسن روی وب‌سایت حسینی کالا...")
print("=" * 60)

for item in updates:
    pid = item['id']
    new_title = item['title']
    new_slug = item['slug']
    
    print(f"\nدر حال به‌روزرسانی محصول شناسه {pid}...")
    print(f"  عنوان جدید: {new_title}")
    print(f"  اسلاگ جدید: {new_slug}")
    
    payload = {
        'title': new_title,
        'slug': new_slug
    }
    
    success = False
    for attempt in range(3):
        try:
            r = requests.post(f"{BASE_API}/{pid}", auth=AUTH, headers=HEADERS, json=payload, timeout=40)
            if r.status_code == 200:
                res_data = r.json()
                print(f"  [OK 200] محصول {pid} با موفقیت به‌روزرسانی شد.")
                print(f"  عنوان ثبت‌شده: {res_data.get('title', {}).get('rendered')}")
                print(f"  اسلاگ ثبت‌شده: {res_data.get('slug')}")
                success = True
                break
            else:
                print(f"  [تلاش {attempt+1}] خطا در پاسخ سرور (کد {r.status_code}): {r.text[:150]}")
        except Exception as e:
            print(f"  [تلاش {attempt+1}] خطا در ارتباط: {e}")
            time.sleep(2)
            try:
                # بررسی وضعیت
                r_check = requests.get(f"{BASE_API}/{pid}", auth=AUTH, headers=HEADERS, timeout=20)
                if r_check.status_code == 200:
                    check_title = r_check.json().get('title', {}).get('rendered')
                    if 'هاورسن' in check_title:
                        print(f"  [تایید موفقیت]: عنوان با موفقیت تغییر یافته: {check_title}")
                        success = True
                        break
            except Exception as e2:
                print(f"  خطا در بررسی مجدد: {e2}")
        time.sleep(2)
        
    if not success:
        print(f"❌ خطا در به‌روزرسانی محصول {pid}")

print("\n" + "=" * 60)
print("پایان عملیات به‌روزرسانی روی سایت.")
print("=" * 60)
