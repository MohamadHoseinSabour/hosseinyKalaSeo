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

BASE_API = 'https://hosseinykala.ir/wp-json/wp/v2/product'

fixes = [
    (3551, [93], 'ماشین لباسشویی ۱۷ کیلوگرم دوقلو ریتون مدل دو موتوره'),
    (3453, [92, 156], 'یخچال فریزر دوقلو 21 فوت الکترواستیل مدل فیوچر'),
    (3573, [93, 157], 'ماشین لباسشویی ۱۰ کیلوگرم اینورتر کلور مدل دایرکت درایو کرم'),
    (3711, [120, 165], 'آبمیوه‌گیری تک‌کاره ۸۰۰ وات دونالکس مدل DN-120'),
    (3626, [122, 169], 'گوشت‌کوب و غذاساز چندکاره ۸۰۰ وات دونالکس مدل DN-290'),
    (3285, [124, 174], 'سشوار پرو امگا مدل 8805')
]

print(f"Applying category fixes to {len(fixes)} products...\n")

for pid, cat_ids, name in fixes:
    print(f"Updating Product {pid} ('{name}')...")
    payload = {'product_cat': cat_ids}
    
    success = False
    for attempt in range(3):
        try:
            r = requests.post(f"{BASE_API}/{pid}", auth=AUTH, headers=HEADERS, json=payload, timeout=60)
            if r.status_code == 200:
                print(f"  [OK] Product {pid} updated successfully to categories: {r.json().get('product_cat')}")
                success = True
                break
            else:
                print(f"  [Attempt {attempt+1} Status {r.status_code}]: {r.text[:100]}")
        except Exception as e:
            print(f"  [Attempt {attempt+1} Exception]: {e}")
            # Verify if it went through despite timeout
            time.sleep(3)
            try:
                r_check = requests.get(f"{BASE_API}/{pid}", auth=AUTH, headers=HEADERS, timeout=30)
                if r_check.status_code == 200 and set(r_check.json().get('product_cat', [])) == set(cat_ids):
                    print(f"  [VERIFIED OK] Product {pid} has correct categories: {cat_ids}")
                    success = True
                    break
            except Exception as e2:
                print(f"  [Check Error]: {e2}")
        time.sleep(2)
        
    if not success:
        print(f"  [FAILED] Could not update Product {pid}!")

print("\n=== All Product Category Fixes Finished! ===")
