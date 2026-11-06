import os
import sys
import json
import requests
from requests.auth import HTTPBasicAuth
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
PUBLISHED_PATH = os.path.join(PROJECT_DIR, 'scratch', 'published_44_products_result.json')

def main():
    print("=== ۱. بررسی زنده ۳ نمونه از محصولات منتشرشده روی سایت حسینی کالا ===")
    with open(PUBLISHED_PATH, 'r', encoding='utf-8') as f:
        pub = json.load(f)

    sample_slugs = list(pub.keys())[:3]
    auth = HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')

    for slug in sample_slugs:
        item = pub[slug]
        pid = item['product_id']
        url = f'https://hosseinykala.ir/wp-json/wc/v3/products/{pid}'
        try:
            res = requests.get(url, auth=auth, timeout=15)
            if res.status_code == 200:
                data = res.json()
                print(f"✓ تایید زنده سایت - شناسه {pid} ({slug}):")
                print(f"   نام: {data.get('name')}")
                print(f"   وضعیت انتشار: {data.get('status')}")
                print(f"   وضعیت موجودی: {data.get('stock_status')}")
                print(f"   دسته‌بندی‌ها: {[c.get('name') for c in data.get('categories', [])]}")
                print(f"   تصویر شاخص: {data.get('images', [{}])[0].get('src') if data.get('images') else 'ندارد'}")
                print(f"   لینک دائمی: {data.get('permalink')}")
            else:
                print(f"✗ خطا در دریافت شناسه {pid}: کد {res.status_code}")
        except Exception as e:
            print(f"✗ خطای ارتباطی: {e}")

    print("\n=== ۲. بررسی صحت فایل کاتالوگ اکسل (hosseiny_kala_catalog.xlsx) ===")
    wb = openpyxl.load_workbook(CATALOG_PATH, data_only=True)

    unregistered_count = 0
    registered_44_count = 0
    outofstock_44_count = 0

    CATEGORY_SHEETS = [
        'یخچال و فریزر', 'شستشو و نظافت', 'لوازم برقی و پخت و پز', 'نوشیدنی ساز',
        'سرمایش و گرمایش', 'تصفیه کننده آب', 'صوتی و تصویری', 'زیبایی و سلامت فردی'
    ]

    all_pids_in_pub = {v['product_id'] for v in pub.values()}

    for sname in CATEGORY_SHEETS:
        ws = wb[sname]
        for r in range(2, ws.max_row + 1):
            val_a = ws.cell(r, 1).value
            if not val_a or '📂' in str(val_a):
                continue

            status_r = str(ws.cell(r, 18).value or '').strip()
            if status_r == 'در سایت تعریف نشده':
                unregistered_count += 1

            pid_val = ws.cell(r, 14).value
            if pid_val in all_pids_in_pub:
                registered_44_count += 1
                stk = str(ws.cell(r, 8).value or '').strip()
                if stk == 'ناموجود':
                    outofstock_44_count += 1

    print(f"تعداد ردیف‌های «در سایت تعریف نشده» در کاتالوگ: {unregistered_count} (باید 0 باشد)")
    print(f"تعداد ۴۴ محصول تطبیق‌یافته در شیت‌ها با PID: {registered_44_count} از 44")
    print(f"تعداد ۴۴ محصول با وضعیت موجودی «ناموجود»: {outofstock_44_count} از 44")

    print("\n=== ۳. مقادیر شیت خلاصه و داشبورد ===")
    ws_dash = wb['📊 خلاصه و داشبورد']
    print(f"ردیف ۵: کل محصولات={ws_dash.cell(5, 2).value} | ثبت‌شده در سایت={ws_dash.cell(5, 3).value} | تنوع‌ها={ws_dash.cell(5, 4).value} | موجود={ws_dash.cell(5, 5).value} | ناموجود={ws_dash.cell(5, 6).value}")

    assert unregistered_count == 0, "هنوز کالای تعریف نشده در سایت وجود دارد!"
    assert registered_44_count == 44, "تعداد کالاهای ثبت شده به 44 نرسیده!"
    assert outofstock_44_count == 44, "تمام 44 کالا ناموجود نشده‌اند!"
    print("\n🎉 تمامی بررسی‌ها و اعتبارسنجی‌ها با موفقیت ۱۰۰٪ پاس شدند!")

if __name__ == '__main__':
    main()
