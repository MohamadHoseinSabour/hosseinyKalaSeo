"""
apply_3_specific_prices.py
===========================
اعمال قیمت‌های مشخص‌شده برای ۳ محصول:
۱. جاروبرقی کندی مدل KCV-325 G (شناسه 4492): ۱۷ میلیون تومان (۱۷۰,۰۰۰,۰۰۰ ریال)
۲. تلویزیون هوشمند 43 اینچ الیو مدل OL-43FSS30 (شناسه 4494): ۵۵ میلیون تومان (۵۵۰,۰۰۰,۰۰۰ ریال)
۳. تلویزیون هوشمند 43 اینچ ال ای دی ایکس ویژن مدل 43XT515 (شناسه 4497): ۶۳ میلیون تومان (۶۳۰,۰۰۰,۰۰۰ ریال)

به‌روزرسانی در:
- سایت حسینی کالا از طریق WooCommerce REST API
- کاتالوگ اکسل hosseiny_kala_catalog.xlsx
- دیتابیس‌های محلی data/products.json و data/id_mappings.json
"""

import os
import sys
import json
import shutil
import datetime
import requests
import openpyxl
from requests.auth import HTTPBasicAuth

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
PRODUCTS_JSON_PATH = os.path.join(PROJECT_DIR, 'data', 'products.json')
ID_MAPPINGS_PATH = os.path.join(PROJECT_DIR, 'data', 'id_mappings.json')

BASE_URL = 'https://hosseinykala.ir'
AUTH = HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

TARGET_PRODUCTS = [
    {
        'pid': 4492,
        'sheet': 'شستشو و نظافت',
        'row': 111,
        'name': 'جاروبرقی کیسه ای 2500 وات کندی مدل KCV-325 G',
        'price_toman': 17000000,
        'price_rial': 170000000,
    },
    {
        'pid': 4494,
        'sheet': 'صوتی و تصویری',
        'row': 11,
        'name': 'تلویزیون هوشمند 43 اینچ الیو مدل OL-43FSS30 اندروید 14',
        'price_toman': 55000000,
        'price_rial': 550000000,
    },
    {
        'pid': 4497,
        'sheet': 'صوتی و تصویری',
        'row': 13,
        'name': 'تلویزیون هوشمند 43 اینچ ال ای دی ایکس ویژن مدل 43XT515',
        'price_toman': 63000000,
        'price_rial': 630000000,
    }
]

def main():
    print("=" * 65)
    print("🚀 اعمال قیمت‌های جدید برای ۳ محصول (جاروبرقی کندی، الیو، ایکس ویژن)")
    print("=" * 65)

    # ۱. به‌روزرسانی در سایت از طریق WooCommerce API
    print("\n🌐 گام ۱: ارسال قیمت‌ها به سایت از طریق WooCommerce API...")
    payload = {
        'update': [
            {
                'id': item['pid'],
                'regular_price': str(item['price_toman']),
                'sale_price': ''
            }
            for item in TARGET_PRODUCTS
        ]
    }

    url = f"{BASE_URL}/wp-json/wc/v3/products/batch"
    res = requests.post(url, json=payload, auth=AUTH, headers=HEADERS, timeout=30)
    if res.status_code == 200:
        data = res.json()
        print(f"✓ پاسخ سرور دریافت شد (HTTP 200): {len(data.get('update', []))} محصول با موفقیت در سایت ثبت شد.")
        for p in data.get('update', []):
            print(f"  • ID #{p['id']}: regular_price={p.get('regular_price')} ت | price={p.get('price')} ت | {p.get('name')[:35]}")
    else:
        print(f"❌ خطا در ارسال به سایت: {res.status_code} - {res.text[:200]}")
        sys.exit(1)

    # ۲. به‌روزرسانی فایل کاتالوگ اکسل
    print("\n📊 گام ۲: به‌روزرسانی فایل اکسل کاتالوگ...")
    wb = openpyxl.load_workbook(CATALOG_PATH, data_only=False)

    for item in TARGET_PRODUCTS:
        ws = wb[item['sheet']]
        r = item['row']
        # اطمینان از نام محصول
        actual_name = ws.cell(r, 1).value
        print(f"  • سطر {r} در شیت «{item['sheet']}» ({actual_name[:30]}):")

        # ستون B: قیمت عادی ریال
        ws.cell(r, 2).value = item['price_rial']
        ws.cell(r, 2).number_format = '#,##0'

        # ستون D: آخرین قیمت مشخص‌شده (ریال)
        ws.cell(r, 4).value = item['price_rial']
        ws.cell(r, 4).number_format = '#,##0'

        # ستون F: قیمت حراج
        ws.cell(r, 6).value = None

        print(f"    - ستون B (ریال): {item['price_rial']:,}")
        print(f"    - ستون C (تومان): فرمول =B{r}/10 ({item['price_toman']:,})")
        print(f"    - ستون D (ریال): {item['price_rial']:,}")

    wb.save(CATALOG_PATH)
    print(f"✓ فایل اکسل با موفقیت ذخیره شد: {os.path.basename(CATALOG_PATH)}")

    # ۳. به‌روزرسانی دیتابیس‌های محلی
    print("\n💾 گام ۳: به‌روزرسانی دیتابیس‌های محلی (data/products.json و data/id_mappings.json)...")
    with open(PRODUCTS_JSON_PATH, 'r', encoding='utf-8') as f:
        products = json.load(f)

    target_map = {item['pid']: item for item in TARGET_PRODUCTS}

    up_count = 0
    for p in products:
        pid = p.get('id')
        if pid in target_map:
            p['regular_price'] = str(target_map[pid]['price_toman'])
            p['sale_price'] = ''
            p['price'] = str(target_map[pid]['price_toman'])
            up_count += 1

    with open(PRODUCTS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print(f"✓ دیتابیس data/products.json به‌روز شد ({up_count} محصول).")

    with open(ID_MAPPINGS_PATH, 'r', encoding='utf-8') as f:
        id_map = json.load(f)

    for pid_int, item in target_map.items():
        pid_str = str(pid_int)
        if pid_str in id_map:
            id_map[pid_str]['price'] = item['price_toman']

    with open(ID_MAPPINGS_PATH, 'w', encoding='utf-8') as f:
        json.dump(id_map, f, ensure_ascii=False, indent=2)
    print(f"✓ دیتابیس data/id_mappings.json به‌روز شد.")

    # ۴. راستی‌آزمایی زنده
    print("\n🔍 گام ۴: راستی‌آزمایی زنده در سایت...")
    for item in TARGET_PRODUCTS:
        res = requests.get(f"{BASE_URL}/wp-json/wc/v3/products/{item['pid']}", auth=AUTH, headers=HEADERS, timeout=15)
        if res.status_code == 200:
            d = res.json()
            reg = d.get('regular_price')
            price = d.get('price')
            expected = str(item['price_toman'])
            if reg == expected and price == expected:
                print(f"  ✅ PASS ID #{item['pid']} ({item['name'][:25]}): قیمت سایت = {int(price):,} تومان (کاملاً منطبق)")
            else:
                print(f"  ❌ MISMATCH ID #{item['pid']}: reg={reg}, price={price}, expected={expected}")
        else:
            print(f"  ❌ خطا در دریافت ID #{item['pid']}: {res.status_code}")

    print("\n" + "=" * 65)
    print("✅ تمامی مراحل اعمال قیمت‌های جدید با موفقیت به پایان رسید.")
    print("=" * 65)

if __name__ == '__main__':
    main()
