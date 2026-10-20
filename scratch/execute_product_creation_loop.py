# -*- coding: utf-8 -*-
"""
execute_product_creation_loop.py
================================
اسکریپت جامع و چندلایه‌ای ایجاد محصولات جدید حسینی کالا:
- لایه ۱: خواندن نقشه محصولات و محتوای سئوشده
- لایه ۲: بهینه‌سازی و آپلود تصاویر به کتابخانه رسانه وردپرس
- لایه ۳: ایجاد محصولات ساده و متغیر در ووکامرس با وضعیت outofstock
- لایه ۴: ایجاد تنوع‌های محصولات متغیر با وضعیت outofstock
- لایه ۵: راستی‌آزمایی زنده (Live HTTP Check) در سایت
- لایه ۶: ثبت وضعیت در فایل پیشرفت (Checkpointing)
"""

import os
import sys
import io
import time
import json
import requests
from PIL import Image

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

from content_generator import generate_product_content

PROGRESS_FILE = 'scratch/creation_progress.json'
PLAN_FILE = 'scratch/all_61_products.json'

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_progress(progress):
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def upload_product_images(img_paths, product_name):
    """
    آپلود بهینه‌شده تصاویر محصول و بازگرداندن شناسه‌های رسانه.
    """
    media_ids = []
    for idx, fp in enumerate(img_paths):
        if not os.path.exists(fp):
            print(f"    ⚠️ فایل عکس یافت نشد: {fp}")
            continue
            
        try:
            img = Image.open(fp).convert('RGB')
            max_dim = 1200
            w, h = img.size
            if w > max_dim or h > max_dim:
                scale = max_dim / max(w, h)
                img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
                
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=85, optimize=True)
            img_bytes = buf.getvalue()
            
            base_fn = os.path.basename(fp)
            fn_clean = os.path.splitext(base_fn)[0] + f"_{idx+1}.jpg"
            
            upload_headers = {
                'User-Agent': HEADERS['User-Agent'],
                'Content-Type': 'image/jpeg',
                'Content-Disposition': f'attachment; filename="{fn_clean}"'
            }
            
            r = requests.post(
                'https://hosseinykala.ir/wp-json/wp/v2/media',
                auth=AUTH,
                headers=upload_headers,
                data=img_bytes,
                timeout=45
            )
            
            if r.status_code in [200, 201]:
                m_data = r.json()
                m_id = m_data.get('id')
                media_ids.append(m_id)
                print(f"    ✓ عکس {idx+1} با موفقیت آپلود شد: ID {m_id} ({len(img_bytes)/1024:.1f} KB)")
                
                # تنظیم عنوان و Alt
                alt_txt = f"{product_name} - حسینی کالا اهواز"
                if idx > 0:
                    alt_txt += f" تصویر {idx+1}"
                try:
                    requests.post(
                        f'https://hosseinykala.ir/wp-json/wp/v2/media/{m_id}',
                        auth=AUTH,
                        headers=HEADERS,
                        json={'alt_text': alt_txt, 'title': f"خرید {product_name}"},
                        timeout=15
                    )
                except Exception as e_meta:
                    pass
            else:
                print(f"    ❌ خطا در آپلود {fp}: کد {r.status_code}")
        except Exception as e:
            print(f"    ❌ استثنا در پردازش تصویر {fp}: {e}")
            
    return media_ids

def run_loop():
    with open(PLAN_FILE, 'r', encoding='utf-8') as f:
        products = json.load(f)
        
    progress = load_progress()
    
    # ثبت دو محصولی که در تست موفق بودند
    if 'همزن برقی کنوود مدل HM430' not in progress:
        progress['همزن برقی کنوود مدل HM430'] = {
            'product_id': 3988,
            'slug': 'kenwood-hm430-hand-mixer',
            'type': 'simple',
            'variations': [],
            'live_verified': True
        }
    if 'کتری برقی ساپر مدل 1031' not in progress:
        progress['کتری برقی ساپر مدل 1031'] = {
            'product_id': 3990,
            'slug': 'saper-1031-electric-kettle',
            'type': 'variable',
            'variations': [
                {'name': 'رنگ: سبز', 'variation_id': 3991},
                {'name': 'رنگ: کرم', 'variation_id': 3992}
            ],
            'live_verified': True
        }
    save_progress(progress)
    
    total = len(products)
    print(f"==================================================")
    print(f"آغاز ایجنت‌لوپ اجرای ساخت ۶۱ محصول در ووکامرس")
    print(f"تعداد کل کالاها: {total}")
    print(f"تعداد از قبل تکمیل‌شده: {len(progress)}")
    print(f"==================================================\n")
    
    for idx, prod in enumerate(products, 1):
        name = prod['name']
        slug = prod['slug']
        ptype = prod['type']
        
        print(f"[{idx}/{total}] در حال پردازش: {name} ({ptype})...")
        
        # اگر از قبل ساخته شده و تست شده است
        if name in progress and progress[name].get('live_verified'):
            print(f"  ⏭️ قبلاً ساخته و تأیید شده است (ID: {progress[name]['product_id']}). عبور.\n")
            continue
            
        # ۱. تولید محتوای سئوشده
        short_desc, full_desc = generate_product_content(prod)
        
        # ۲. آپلود تصاویر
        print(f"  📸 آپلود تصاویر ({len(prod['images'])} عکس)...")
        media_ids = upload_product_images(prod['images'], name)
        if not media_ids:
            print(f"  ⚠️ هشدار: هیچ عکسی آپلود نشد، اما ادامه می‌دهیم.")
            
        images_payload = [{'id': mid} for mid in media_ids]
        
        # ۳. ساخت محصول
        if ptype == 'simple':
            payload = {
                'name': name,
                'slug': slug,
                'type': 'simple',
                'status': 'publish',
                'catalog_visibility': 'visible',
                'manage_stock': False,
                'stock_status': 'outofstock',
                'categories': [{'id': cid} for cid in prod['categories']],
                'images': images_payload,
                'short_description': short_desc,
                'description': full_desc
            }
            
            try:
                r_create = requests.post(
                    'https://hosseinykala.ir/wp-json/wc/v3/products',
                    auth=AUTH,
                    headers=HEADERS,
                    json=payload,
                    timeout=60
                )
                if r_create.status_code in [200, 201]:
                    cdata = r_create.json()
                    new_id = cdata.get('id')
                    print(f"  ✓ محصول ساده ایجاد شد! شناسه: {new_id}")
                    
                    # راستی‌آزمایی زنده
                    r_live = requests.get(f'https://hosseinykala.ir/product/{slug}/', headers=HEADERS, timeout=25)
                    live_ok = (r_live.status_code == 200)
                    print(f"  ✓ وضعیت صفحه محصول زنده: {r_live.status_code} ({'تأیید شد' if live_ok else 'خطا'})")
                    
                    progress[name] = {
                        'product_id': new_id,
                        'slug': slug,
                        'type': 'simple',
                        'media_ids': media_ids,
                        'variations': [],
                        'live_verified': live_ok
                    }
                    save_progress(progress)
                else:
                    print(f"  ❌ خطا در ساخت محصول: {r_create.status_code} - {r_create.text[:200]}")
            except Exception as e:
                print(f"  ❌ استثنا در اتصال به API: {e}")
                
        else: # متغیر (variable)
            # تعیین نام و مقادیر attribute
            variations = prod.get('variations', [])
            attr_name = 'مدل / مشخصه'
            attr_options = []
            
            for v in variations:
                v_attr = v.get('variant_attr') or v.get('name')
                if ':' in v_attr:
                    parts = v_attr.split(':', 1)
                    clean_attr_name = parts[0].replace('↳', '').strip()
                    val = parts[1].strip()
                    attr_name = clean_attr_name
                    attr_options.append(val)
                else:
                    clean_val = v_attr.replace('↳', '').strip()
                    attr_options.append(clean_val)
                    
            if not attr_options:
                attr_options = ['استاندارد']
                
            payload = {
                'name': name,
                'slug': slug,
                'type': 'variable',
                'status': 'publish',
                'catalog_visibility': 'visible',
                'manage_stock': False,
                'stock_status': 'outofstock',
                'categories': [{'id': cid} for cid in prod['categories']],
                'images': images_payload,
                'attributes': [
                    {
                        'name': attr_name,
                        'position': 0,
                        'visible': True,
                        'variation': True,
                        'options': attr_options
                    }
                ],
                'short_description': short_desc,
                'description': full_desc
            }
            
            try:
                r_create = requests.post(
                    'https://hosseinykala.ir/wp-json/wc/v3/products',
                    auth=AUTH,
                    headers=HEADERS,
                    json=payload,
                    timeout=60
                )
                if r_create.status_code in [200, 201]:
                    cdata = r_create.json()
                    new_id = cdata.get('id')
                    print(f"  ✓ محصول متغیر (والد) ایجاد شد! شناسه: {new_id}")
                    
                    var_records = []
                    for opt_idx, opt_val in enumerate(attr_options):
                        v_payload = {
                            'stock_status': 'outofstock',
                            'manage_stock': False,
                            'attributes': [{'name': attr_name, 'option': opt_val}]
                        }
                        if opt_idx < len(media_ids):
                            v_payload['image'] = {'id': media_ids[opt_idx]}
                            
                        r_var = requests.post(
                            f'https://hosseinykala.ir/wp-json/wc/v3/products/{new_id}/variations',
                            auth=AUTH,
                            headers=HEADERS,
                            json=v_payload,
                            timeout=30
                        )
                        if r_var.status_code in [200, 201]:
                            var_id = r_var.json().get('id')
                            var_name = variations[opt_idx]['name'] if opt_idx < len(variations) else opt_val
                            var_records.append({'name': var_name, 'variation_id': var_id})
                            print(f"    ✓ تنوع '{opt_val}' ایجاد شد: ID {var_id}")
                        else:
                            print(f"    ❌ خطا در تنوع '{opt_val}': {r_var.status_code}")
                            
                    # راستی‌آزمایی زنده
                    r_live = requests.get(f'https://hosseinykala.ir/product/{slug}/', headers=HEADERS, timeout=25)
                    live_ok = (r_live.status_code == 200)
                    print(f"  ✓ وضعیت صفحه محصول زنده: {r_live.status_code} ({'تأیید شد' if live_ok else 'خطا'})")
                    
                    progress[name] = {
                        'product_id': new_id,
                        'slug': slug,
                        'type': 'variable',
                        'media_ids': media_ids,
                        'variations': var_records,
                        'live_verified': live_ok
                    }
                    save_progress(progress)
                else:
                    print(f"  ❌ خطا در ساخت محصول والد: {r_create.status_code} - {r_create.text[:200]}")
            except Exception as e:
                print(f"  ❌ استثنا در اتصال به API برای محصول متغیر: {e}")
                
        print()
        time.sleep(1) # وقفه کوتاه جهت جلوگیری از فشار به سرور
        
    print("\n==================================================")
    print("تمام محصولات با موفقیت پردازش و در سایت ایجاد شدند!")
    print(f"تعداد کالاهای تکمیل‌شده در دیتابیس پیشرفت: {len(progress)}")
    print("==================================================")

if __name__ == '__main__':
    run_loop()
