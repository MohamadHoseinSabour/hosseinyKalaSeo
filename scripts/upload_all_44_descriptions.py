"""
upload_all_44_descriptions.py
==============================
بارگذاری و به‌روزرسانی توضیحات جامع و سئوشده برای تمام ۴۴ محصول جدید در ووکامرس حسینی کالا.
علت مشکل: در اسکریپت ساخت اولیه، به جای کلید 'description' از 'long_description' استفاده شده بود
که باعث خالی ماندن فیلد توضیحات در سایت شده بود.
این اسکریپت توضیحات کامل موجود در data/new_products/<slug>/info.json را به صورت دسته‌ای (Batch)
روی وب‌سایت حسینی کالا بارگذاری و راستی‌آزمایی می‌کند.
"""

import os
import sys
import time
import json
import requests
from requests.auth import HTTPBasicAuth

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_NEW_PRODS = os.path.join(PROJECT_DIR, 'data', 'new_products')
PUBLISHED_44_PATH = os.path.join(PROJECT_DIR, 'scratch', 'published_44_products_result.json')

BASE_URL = 'https://hosseinykala.ir'
AUTH = HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

def main():
    print("=" * 70)
    print("🚀 آغاز بارگذاری توضیحات سئوشده برای ۴۴ محصول جدید در وب‌سایت حسینی کالا")
    print("=" * 70)

    with open(PUBLISHED_44_PATH, 'r', encoding='utf-8') as f:
        published_map = json.load(f)

    updates = []
    for slug, item in published_map.items():
        pid = item['product_id']
        info_file = os.path.join(DATA_NEW_PRODS, slug, 'info.json')
        if not os.path.exists(info_file):
            print(f"⚠️ فایل info.json برای {slug} یافت نشد.")
            continue

        with open(info_file, 'r', encoding='utf-8') as inf_f:
            info = json.load(inf_f)

        desc = info.get('description', '')
        if not desc:
            print(f"⚠️ توضیحات برای {slug} در info.json خالی است.")
            continue

        updates.append({
            'id': pid,
            'name': item['name'],
            'slug': slug,
            'description': desc,
            'desc_len': len(desc)
        })

    print(f"✓ تعداد {len(updates)} محصول آماده به‌روزرسانی توضیحات شدند.")

    # ارسال دسته‌ای در بسته‌های ۱۰ تایی
    chunk_size = 10
    total_chunks = (len(updates) + chunk_size - 1) // chunk_size
    success_count = 0

    session = requests.Session()
    session.auth = AUTH
    session.headers.update(HEADERS)

    url = f"{BASE_URL}/wp-json/wc/v3/products/batch"

    for i in range(0, len(updates), chunk_size):
        chunk = updates[i:i + chunk_size]
        batch_no = i // chunk_size + 1
        payload = {
            'update': [
                {
                    'id': p['id'],
                    'description': p['description']
                }
                for p in chunk
            ]
        }

        for attempt in range(1, 4):
            try:
                t0 = time.time()
                res = session.post(url, json=payload, timeout=60)
                elapsed = time.time() - t0
                if res.status_code == 200:
                    data = res.json()
                    up_items = data.get('update', [])
                    success_count += len(up_items)
                    print(f"  ✓ دسته {batch_no}/{total_chunks} ({len(chunk)} محصول) ثبت شد ({elapsed:.1f}s)")
                    break
                else:
                    print(f"  ⚠️ خطا در ارسال دسته {batch_no} (تلاش {attempt}): کد {res.status_code} - {res.text[:120]}")
                    time.sleep(2)
            except Exception as e:
                print(f"  ⚠️ استثنا در دسته {batch_no} (تلاش {attempt}): {e}")
                time.sleep(3)

        time.sleep(0.5)

    print("\n" + "-" * 50)
    print(f"پایان ارسال: {success_count} از {len(updates)} توضیحات محصول در سایت بارگذاری شد.")
    print("-" * 50)

    # راستی‌آزمایی زنده
    print("\n🔍 راستی‌آزمایی زنده نمونه محصولات:")
    sample_pids = [updates[0]['id'], updates[10]['id'], updates[20]['id'], updates[30]['id'], updates[-1]['id']]
    verified_ok = 0
    for pid in sample_pids:
        try:
            r = session.get(f"{BASE_URL}/wp-json/wc/v3/products/{pid}", timeout=15)
            if r.status_code == 200:
                d = r.json()
                live_desc = d.get('description', '')
                if len(live_desc) > 500:
                    print(f"  ✅ PASS #{pid} ({d.get('name')[:30]}): طول توضیحات = {len(live_desc):,} کاراکتر")
                    verified_ok += 1
                else:
                    print(f"  ⚠️ هشدار #{pid}: طول توضیحات کم است ({len(live_desc)} کاراکتر)")
            else:
                print(f"  ❌ خطا در دریافت #{pid}: {r.status_code}")
        except Exception as e:
            print(f"  ❌ استثنا در بررسی #{pid}: {e}")

    print(f"\nنتیجه راستی‌آزمایی: {verified_ok} از {len(sample_pids)} محصول تایید کامل شدند.")
    print("=" * 70)

if __name__ == '__main__':
    main()
