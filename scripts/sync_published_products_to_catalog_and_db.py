import os
import sys
import json
import shutil
import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
PUBLISHED_PATH = os.path.join(PROJECT_DIR, 'scratch', 'published_44_products_result.json')
STRUCTURED_PATH = os.path.join(PROJECT_DIR, 'scratch', 'structured_44_new_products.json')
NEW_PRODS_DIR = os.path.join(PROJECT_DIR, 'data', 'new_products')
ID_MAPPINGS_PATH = os.path.join(PROJECT_DIR, 'data', 'id_mappings.json')
PRODUCTS_JSON_PATH = os.path.join(PROJECT_DIR, 'data', 'products.json')

CATEGORY_SHEETS = [
    'یخچال و فریزر', 'شستشو و نظافت', 'لوازم برقی و پخت و پز', 'نوشیدنی ساز',
    'سرمایش و گرمایش', 'تصفیه کننده آب', 'صوتی و تصویری', 'زیبایی و سلامت فردی'
]

FONT_LINK = Font(name="Calibri", size=9.5, color="0563C1", underline="single")
FONT_REGULAR = Font(name="Calibri", size=9.5, bold=False, color="000000")
FONT_STOCK_RED = Font(name="Calibri", size=10, bold=True, color="721C24")
FILL_STOCK_RED = PatternFill(start_color="FFF8D7DA", end_color="FFF8D7DA", fill_type="solid")

def main():
    print("=== ۱. بارگذاری داده‌های محصولات منتشرشده و ایجاد نسخه‌های پشتیبان ===")
    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # بکاپ کاتالوگ
    backup_catalog = os.path.join(PROJECT_DIR, f'hosseiny_kala_catalog.backup_before_published_sync_{now_str}.xlsx')
    shutil.copy2(CATALOG_PATH, backup_catalog)
    print(f"✓ بکاپ کاتالوگ ایجاد شد: {os.path.basename(backup_catalog)}")

    # بکاپ دیتابیس‌ها
    shutil.copy2(ID_MAPPINGS_PATH, ID_MAPPINGS_PATH + f'.bak_{now_str}')
    shutil.copy2(PRODUCTS_JSON_PATH, PRODUCTS_JSON_PATH + f'.bak_{now_str}')
    print("✓ بکاپ id_mappings.json و products.json ایجاد شد.")

    # بارگذاری نتایج انتشار
    with open(PUBLISHED_PATH, 'r', encoding='utf-8') as f:
        published_map = json.load(f)
    print(f"✓ تعداد {len(published_map)} محصول منتشرشده در سایت بارگذاری شد.")

    # بارگذاری structured و ساخت مپ نام به اسلاگ
    with open(STRUCTURED_PATH, 'r', encoding='utf-8') as f:
        structured_list = json.load(f)
    
    name_to_raw = {p['name'].strip(): p['raw_title'].strip() for p in structured_list}

    # بارگذاری info.json برای استخراج جزییات تک‌تک محصولات
    raw_to_slug = {}
    slug_to_info = {}
    for d in os.listdir(NEW_PRODS_DIR):
        ip = os.path.join(NEW_PRODS_DIR, d, 'info.json')
        if os.path.isfile(ip):
            with open(ip, 'r', encoding='utf-8') as f:
                inf = json.load(f)
                raw_to_slug[inf['raw_title'].strip()] = inf['slug']
                slug_to_info[inf['slug']] = inf

    print(f"✓ اطلاعات پوشه‌های ۴۴ محصول خوانده شد.")

    # مپ نام در کاتالوگ به دیتای انتشار
    name_to_published = {}
    for cat_name, raw in name_to_raw.items():
        slug = raw_to_slug.get(raw)
        if slug and slug in published_map:
            name_to_published[cat_name] = published_map[slug]
            name_to_published[cat_name]['info'] = slug_to_info[slug]

    print(f"✓ تعداد {len(name_to_published)} تطبیق نام کاتالوگ با محصولات منتشرشده آماده گردید.")

    print("\n=== ۲. اعمال تغییرات در شیت‌های دسته‌بندی کاتالوگ اکسل ===")
    wb = openpyxl.load_workbook(CATALOG_PATH, data_only=False)

    updated_count = 0
    sheet_stats = {}

    for sname in CATEGORY_SHEETS:
        ws = wb[sname]
        main_prods_count = 0
        vars_count = 0
        in_stock_count = 0
        out_stock_count = 0

        for r in range(2, ws.max_row + 1):
            val_a = ws.cell(r, 1).value
            val_a_str = str(val_a).strip() if val_a is not None else ""
            if not val_a_str or '📂' in val_a_str or val_a_str in ['\\', '/', '-', '•']:
                continue

            ptype = str(ws.cell(r, 12).value or '').strip()
            if ptype == 'تنوع':
                vars_count += 1
            else:
                main_prods_count += 1

            status_r = str(ws.cell(r, 18).value or '').strip()

            # بررسی اینکه آیا این سطر مربوط به یکی از ۴۴ محصول جدید است
            if status_r == 'در سایت تعریف نشده' and val_a_str in name_to_published:
                pub_data = name_to_published[val_a_str]
                slug = pub_data['slug']
                pid = pub_data['product_id']
                link = pub_data['permalink']
                sku = f"HK-{slug.upper()}"

                # ستون H (8): موجودی -> ناموجود
                cell_h = ws.cell(r, 8, "ناموجود")
                cell_h.font = FONT_STOCK_RED
                cell_h.fill = FILL_STOCK_RED

                # ستون N (14): شناسه ووکامرس (PID)
                ws.cell(r, 14, pid)
                ws.cell(r, 14).alignment = Alignment(horizontal="center", vertical="center")

                # ستون P (16): لینک محصول
                cell_p = ws.cell(r, 16, link)
                cell_p.hyperlink = link
                cell_p.font = FONT_LINK
                cell_p.alignment = Alignment(horizontal="center", vertical="center")

                # ستون Q (17): کد SKU
                cell_q = ws.cell(r, 17, sku)
                cell_q.font = FONT_REGULAR
                cell_q.alignment = Alignment(horizontal="center", vertical="center")

                # ستون R (18): وضعیت در سایت -> ثبت‌شده در سایت
                cell_r = ws.cell(r, 18, "ثبت‌شده در سایت")
                cell_r.font = FONT_REGULAR
                cell_r.alignment = Alignment(horizontal="center", vertical="center")

                # اطمینان از حذف پس‌زمینه زرد از تمام سلول‌های این سطر
                for col in range(1, 19):
                    if col != 8: # ستون موجودی استایل قرمز خود را دارد
                        ws.cell(r, col).fill = PatternFill(fill_type=None)

                updated_count += 1

            # آمار موجودی سطر
            stk_val = str(ws.cell(r, 8).value or '').strip()
            if 'ناموجود' in stk_val:
                out_stock_count += 1
            else:
                in_stock_count += 1

        sheet_stats[sname] = {
            'main_prods': main_prods_count,
            'vars': vars_count,
            'in_stock': in_stock_count,
            'out_stock': out_stock_count,
        }
        print(f"  ✓ شیت «{sname}»: کالای اصلی={main_prods_count} (موجود={in_stock_count}، ناموجود={out_stock_count}) | تنوع‌ها={vars_count}")

    print(f"\nتعداد کل سطرهای آپدیت‌شده کاتالوگ: {updated_count} از 44")

    print("\n=== ۳. به‌روزرسانی داشبورد مدیریتی کاتالوگ (📊 خلاصه و داشبورد) ===")
    ws_dash = wb['📊 خلاصه و داشبورد']

    total_main = sum(s['main_prods'] for s in sheet_stats.values())
    total_vars = sum(s['vars'] for s in sheet_stats.values())
    total_in_stock = sum(s['in_stock'] for s in sheet_stats.values())
    total_out_stock = sum(s['out_stock'] for s in sheet_stats.values())

    site_registered_count = 0
    unregistered_count = 0
    for sname in CATEGORY_SHEETS:
        ws_temp = wb[sname]
        for r in range(2, ws_temp.max_row + 1):
            val_a = ws_temp.cell(r, 1).value
            if not val_a or '📂' in str(val_a):
                continue
            if str(ws_temp.cell(r, 12).value or '').strip() != 'تنوع':
                st_r = str(ws_temp.cell(r, 18).value or '').strip()
                if st_r == 'ثبت‌شده در سایت':
                    site_registered_count += 1
                elif st_r == 'در سایت تعریف نشده':
                    unregistered_count += 1

    print(f"آمار کل: کالاهای اصلی={total_main} | ثبت‌شده در سایت={site_registered_count} | تعریف‌نشده={unregistered_count}")
    print(f"موجودی کل: موجود={total_in_stock} | ناموجود={total_out_stock} | مجموع={total_in_stock + total_out_stock}")

    # ردیف ۵ داشبورد
    ws_dash.cell(5, 2, total_main)
    ws_dash.cell(5, 3, site_registered_count)
    ws_dash.cell(5, 4, total_vars)
    ws_dash.cell(5, 5, total_in_stock)
    ws_dash.cell(5, 6, total_out_stock)

    # به‌روزرسانی سطرهای ۸ تا ۱۵ داشبورد
    row_map = {
        'یخچال و فریزر': 8,
        'شستشو و نظافت': 9,
        'لوازم برقی و پخت و پز': 10,
        'نوشیدنی ساز': 11,
        'سرمایش و گرمایش': 12,
        'تصفیه کننده آب': 13,
        'صوتی و تصویری': 14,
        'زیبایی و سلامت فردی': 15,
    }

    for cat_name, r_idx in row_map.items():
        if cat_name in sheet_stats:
            st = sheet_stats[cat_name]
            ws_dash.cell(r_idx, 3, st['main_prods'])
            ws_dash.cell(r_idx, 4, st['vars'])
            ws_dash.cell(r_idx, 5, st['in_stock'])
            ws_dash.cell(r_idx, 6, st['out_stock'])

    wb.save(CATALOG_PATH)
    print(f"✓ فایل کاتالوگ اکسل ذخیره گردید: {os.path.basename(CATALOG_PATH)}")

    print("\n=== ۴. همگام‌سازی دیتابیس‌های محلی id_mappings.json و products.json ===")
    
    # ۱. آپدیت id_mappings.json
    with open(ID_MAPPINGS_PATH, 'r', encoding='utf-8') as f:
        id_mappings = json.load(f)

    for slug, p in published_map.items():
        pid = p['product_id']
        id_mappings[str(pid)] = {
            'name': p['name'],
            'slug': slug,
            'type': 'simple',
            'url': p['permalink'],
            'price': 0
        }

    with open(ID_MAPPINGS_PATH, 'w', encoding='utf-8') as f:
        json.dump(id_mappings, f, ensure_ascii=False, indent=2)
    print(f"✓ دیتابیس id_mappings.json با موفقیت به‌روزرسانی شد (تعداد کل: {len(id_mappings)})")

    # ۲. آپدیت products.json
    with open(PRODUCTS_JSON_PATH, 'r', encoding='utf-8') as f:
        products_list = json.load(f)

    existing_ids = {p['id'] for p in products_list}
    added_to_products = 0

    for slug, p in published_map.items():
        pid = p['product_id']
        if pid not in existing_ids:
            inf = slug_to_info.get(slug, {})
            cat_id = inf.get('category_id', 0)
            cat_name = inf.get('wc_category_name', '')
            cat_slug = inf.get('category_slug', '')
            
            new_item = {
                'id': pid,
                'url': p['permalink'],
                'slug': slug,
                'name': p['name'],
                'type': 'simple',
                'status': 'publish',
                'price': '0',
                'regular_price': '',
                'sale_price': '',
                'currency': 'IRT',
                'in_stock': False,
                'stock_status': 'outofstock',
                'categories': [{'id': cat_id, 'name': cat_name, 'slug': cat_slug}],
                'featured_image': p.get('media_url', ''),
                'short_description': inf.get('short_description', ''),
                'description': inf.get('description', ''),
                'date': p.get('published_at', ''),
                'modified': p.get('published_at', '')
            }
            products_list.append(new_item)
            added_to_products += 1

    with open(PRODUCTS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(products_list, f, ensure_ascii=False, indent=2)
    print(f"✓ دیتابیس products.json به‌روزرسانی شد ({added_to_products} محصول جدید اضافه شد، تعداد کل: {len(products_list)})")

    print("\n✅ تمامی مراحل همگام‌سازی با موفقیت کامل انجام شد.")

if __name__ == '__main__':
    main()
