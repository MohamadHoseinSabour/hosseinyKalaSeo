"""
sync_maier_4099_to_site.py
==========================
اسکریپت همگام‌سازی اصلاح مدل آسیاب قهوه مایر از 4155 به 4099 روی سایت حسینی کالا
(در صورت در دسترس بودن سرور، تغییرات را روی ووکامرس و وردپرس اعمال می‌کند).
"""

import sys
import json
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

def sync_product_4099():
    with open('data/products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)

    target_p = None
    for p in products:
        if p.get('id') == 4249:
            target_p = p
            break

    if not target_p:
        print("خطا: محصول ۴۲۴۹ در دیتابیس محلی یافت نشد.")
        return False

    name = target_p.get('name')
    slug = target_p.get('slug')
    desc = target_p.get('description')
    short_desc = target_p.get('short_description')

    print(f"در حال ارسال تغییرات به سایت حسینی کالا برای محصول {name} ({slug})...")

    s = requests.Session()
    s.mount('https://', TLSAdapter())

    # روش ۱: استفاده از Endpoint رسمی ووکامرس
    wc_url = 'https://hosseinykala.ir/wp-json/wc/v3/products/4249'
    wc_payload = {
        'name': name,
        'slug': slug,
        'description': desc,
        'short_description': short_desc
    }

    # روش ۲: استفاده از Endpoint رسمی وردپرس
    wp_url = 'https://hosseinykala.ir/wp-json/wp/v2/product/4249'
    wp_payload = {
        'title': name,
        'slug': slug,
        'content': desc,
        'excerpt': short_desc
    }

    success = False
    for attempt in range(1, 4):
        print(f"\n[تلاش {attempt}/3] ارسال درخواست به سرور...")
        try:
            r = s.put(wc_url, auth=AUTH, headers=HEADERS, json=wc_payload, timeout=30)
            if r.status_code == 200:
                print("✓ محصول با موفقیت از طریق WooCommerce API به‌روزرسانی شد.")
                success = True
                break
            else:
                print(f"پاسخ WooCommerce API (کد {r.status_code}): {r.text[:150]}")
        except Exception as e:
            print(f"خطای ارتباط با WooCommerce API: {e}")

        # امتحان وردپرس
        try:
            r2 = s.post(wp_url, auth=AUTH, headers=HEADERS, json=wp_payload, timeout=30)
            if r2.status_code == 200:
                print("✓ محصول با موفقیت از طریق WordPress REST API به‌روزرسانی شد.")
                success = True
                break
            else:
                print(f"پاسخ WordPress REST API (کد {r2.status_code}): {r2.text[:150]}")
        except Exception as e:
            print(f"خطای ارتباط با WordPress REST API: {e}")

        if attempt < 3:
            time.sleep(5)

    return success

if __name__ == '__main__':
    res = sync_product_4099()
    sys.exit(0 if res else 1)
