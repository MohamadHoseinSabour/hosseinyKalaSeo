"""
update_prices.py
================
اسکریپت به‌روزرسانی دوطرفه قیمت محصولات از فایل اکسل به سایت hosseinykala.ir

نحوه استفاده:
  python update_prices.py                          # پیش‌نمایش تغییرات
  python update_prices.py --apply                  # اعمال تغییرات روی سایت
  python update_prices.py --apply --sheet "یخچال و فریزر"   # فقط یک شیت

محدودیت‌ها:
  - فقط قیمت‌ها و قیمت‌های حراج به‌روزرسانی می‌شوند
  - هیچ اطلاعات دیگری تغییر نمی‌کند
  - نیاز به Consumer Key/Secret وودکامرس یا Application Password
"""

import os
import sys
import json
import argparse
import base64
import time
import openpyxl
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "https://hosseinykala.ir"
WP_USER = "agent"
WP_APP_PASSWORD = "Mlwg pHHX NQ64 drrz 7ca2 IVto"

# Basic Auth header
AUTH_B64 = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
HEADERS = {
    'Authorization': f'Basic {AUTH_B64}',
    'Content-Type': 'application/json',
    'User-Agent': 'HosseinyKala-PriceUpdater/1.0',
}

SCRIPTS_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(SCRIPTS_DIR)
_primary_excel = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
_updated_excel = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog_updated.xlsx')
EXCEL_FILE = _updated_excel if os.path.exists(_updated_excel) else _primary_excel

def get_column_indices(ws):
    """تشخیص پویای اندیس ستون‌ها بر اساس عنوان هدر اکسل"""
    mapping = {
        'name': 0,
        'price_regular': 1,
        'price_reg_toman': 2,
        'price_sale': 3,
        'price_sale_toman': 4,
        'in_stock': 5,
        'category_path': 6,
        'subcategory': 7,
        'brand': 8,
        'type': 9,
        'variant_attr': 10,
        'product_id': 11,
        'variation_id': 12,
        'link': 13,
        'sku': 14,
        'status_note': 15,
    }
    header = [ws.cell(row=1, column=c).value for c in range(1, ws.max_column + 1)]
    for idx, h in enumerate(header):
        if not h:
            continue
        h_str = str(h).strip()
        if 'نام محصول' in h_str: mapping['name'] = idx
        elif 'عادی (ریال)' in h_str: mapping['price_regular'] = idx
        elif 'عادی (تومان)' in h_str: mapping['price_reg_toman'] = idx
        elif 'حراج (ریال)' in h_str: mapping['price_sale'] = idx
        elif 'حراج (تومان)' in h_str: mapping['price_sale_toman'] = idx
        elif 'موجودی' in h_str: mapping['in_stock'] = idx
        elif 'دسته‌بندی' in h_str: mapping['category_path'] = idx
        elif 'زیردسته' in h_str: mapping['subcategory'] = idx
        elif 'برند' in h_str: mapping['brand'] = idx
        elif 'نوع محصول' in h_str: mapping['type'] = idx
        elif 'مشخصه' in h_str: mapping['variant_attr'] = idx
        elif 'شناسه محصول' in h_str: mapping['product_id'] = idx
        elif 'شناسه تنوع' in h_str: mapping['variation_id'] = idx
        elif 'لینک' in h_str: mapping['link'] = idx
        elif 'SKU' in h_str: mapping['sku'] = idx
        elif 'وضعیت در سایت' in h_str: mapping['status_note'] = idx
    return mapping


def read_excel_products(excel_path, target_sheet=None):
    """خواندن محصولات از فایل اکسل همراه با تبدیل ریال به تومان"""
    wb = openpyxl.load_workbook(excel_path)
    products = []

    sheets = [target_sheet] if target_sheet else [s for s in wb.sheetnames if not s.startswith('راهنما') and not 'داشبورد' in s]

    for sheet_name in sheets:
        if sheet_name not in wb.sheetnames:
            print(f"[WARN] Sheet '{sheet_name}' not found in Excel file.")
            continue

        ws = wb[sheet_name]
        col_map = get_column_indices(ws)

        for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            if not row or len(row) <= col_map['product_id']:
                continue
            name_val = row[col_map['name']]
            if not name_val or '📂' in str(name_val):
                continue
            if not row[col_map['product_id']]:
                continue

            product_id = row[col_map['product_id']]
            variation_id = row[col_map['variation_id']] if len(row) > col_map['variation_id'] else None
            product_type = str(row[col_map['type']] or '').strip() if len(row) > col_map['type'] else ''
            price_regular = row[col_map['price_regular']] if len(row) > col_map['price_regular'] else None
            price_sale = row[col_map['price_sale']] if len(row) > col_map['price_sale'] else None
            stock_val = str(row[col_map['in_stock']] or '').strip() if len(row) > col_map['in_stock'] else ''

            try:
                product_id = int(product_id)
            except (ValueError, TypeError):
                continue

            try:
                variation_id = int(variation_id) if variation_id else None
            except (ValueError, TypeError):
                variation_id = None

            try:
                price_regular = int(float(str(price_regular).replace(',', ''))) if price_regular else None
            except:
                price_regular = None

            try:
                price_sale = int(float(str(price_sale).replace(',', ''))) if price_sale else None
            except:
                price_sale = None

            # توجه: قیمت‌ها در اکسل به ریال هستند و سایت تومان دریافت می‌کند
            price_reg_toman = (price_regular // 10) if price_regular is not None else None
            price_sale_toman = (price_sale // 10) if price_sale is not None else None

            products.append({
                'sheet': sheet_name,
                'row': row_idx,
                'product_id': product_id,
                'variation_id': variation_id,
                'name': name_val,
                'type': product_type,
                'price_regular_rial': price_regular,
                'price_sale_rial': price_sale,
                'price_regular': price_reg_toman,  # واحد تومان برای سایت
                'price_sale': price_sale_toman,     # واحد تومان برای سایت
                'in_stock': stock_val,
            })

    return products


def get_current_price(product_id, variation_id=None):
    """دریافت قیمت فعلی محصول از API"""
    if variation_id:
        url = f"{BASE_URL}/wp-json/wc/v3/products/{product_id}/variations/{variation_id}"
    else:
        url = f"{BASE_URL}/wp-json/wc/v3/products/{product_id}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code == 200:
            data = r.json()
            return {
                'regular_price': data.get('regular_price', ''),
                'sale_price': data.get('sale_price', ''),
            }
    except Exception as e:
        print(f"  [ERROR] Failed to get price for product {product_id}: {e}")
    return None


def update_price_api(product_id, variation_id, new_regular, new_sale, dry_run=True):
    """ارسال قیمت جدید به API وردپرس"""
    if variation_id:
        url = f"{BASE_URL}/wp-json/wc/v3/products/{product_id}/variations/{variation_id}"
    else:
        url = f"{BASE_URL}/wp-json/wc/v3/products/{product_id}"

    payload = {}
    if new_regular is not None:
        payload['regular_price'] = str(new_regular)
    if new_sale is not None:
        payload['sale_price'] = str(new_sale)
    elif new_sale == 0:
        payload['sale_price'] = ''  # حذف قیمت حراج

    if dry_run:
        return True, "DRY RUN - no actual request sent"

    try:
        r = requests.patch(url, json=payload, headers=HEADERS, timeout=20)
        if r.status_code in (200, 201):
            return True, "OK"
        else:
            return False, f"HTTP {r.status_code}: {r.text[:200]}"
    except Exception as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(description='به‌روزرسانی قیمت محصولات از اکسل به سایت')
    parser.add_argument('--apply', action='store_true', help='اعمال تغییرات (بدون این flag فقط پیش‌نمایش)')
    parser.add_argument('--sheet', type=str, default=None, help='فقط شیت مشخص (مثال: "یخچال و فریزر")')
    parser.add_argument('--excel', type=str, default=EXCEL_FILE, help='مسیر فایل اکسل')
    args = parser.parse_args()

    dry_run = not args.apply

    if dry_run:
        print("\n[MODE] پیش‌نمایش تغییرات (DRY RUN) - هیچ تغییری اعمال نمی‌شود")
        print("  برای اعمال تغییرات با --apply اجرا کنید\n")
    else:
        print("\n[MODE] حالت اعمال واقعی - تغییرات روی سایت اعمال می‌شوند!\n")

    print(f"  فایل اکسل: {args.excel}", flush=True)
    products = read_excel_products(args.excel, target_sheet=args.sheet)
    print(f"  تعداد ردیف‌های خوانده شده: {len(products)}\n", flush=True)

    updated = 0
    skipped = 0
    failed = 0
    changes = []

    for prod in products:
        pid = prod['product_id']
        vid = prod['variation_id']
        new_reg = prod['price_regular']
        new_sale = prod['price_sale']

        if new_reg is None and new_sale is None:
            skipped += 1
            continue

        # دریافت قیمت فعلی برای مقایسه
        if not dry_run:
            current = get_current_price(pid, vid)
            if current:
                current_reg = int(current.get('regular_price', 0) or 0)
                current_sale = int(current.get('sale_price', 0) or 0)

                if current_reg == (new_reg or 0) and current_sale == (new_sale or 0):
                    skipped += 1
                    continue

        prod_name = str(prod['name'] or '')[:40]
        change_desc = f"محصول {pid}" + (f" واریاسیون {vid}" if vid else "")
        change_desc += f" ({prod_name})"
        if new_reg:
            change_desc += f" | قیمت عادی: {new_reg:,} تومان ({prod['price_regular_rial']:,} ریال)"
        if new_sale:
            change_desc += f" | قیمت حراج: {new_sale:,} تومان ({prod['price_sale_rial']:,} ریال)"

        success, msg = update_price_api(pid, vid, new_reg, new_sale, dry_run=dry_run)

        if success:
            updated += 1
            changes.append(f"  ✓ {change_desc}")
        else:
            failed += 1
            changes.append(f"  ✗ {change_desc} | خطا: {msg}")

        if not dry_run:
            time.sleep(0.3)  # جلوگیری از rate limiting

    print("\n" + "=" * 60)
    print(f"{'پیش‌نمایش' if dry_run else 'نتیجه'} به‌روزرسانی قیمت‌ها:")
    print("=" * 60)
    for c in changes[:50]:  # نمایش ۵۰ تا اول
        print(c)
    if len(changes) > 50:
        print(f"  ... و {len(changes) - 50} ردیف دیگر")

    print(f"\n  تغییر یافته: {updated}")
    print(f"  بدون تغییر: {skipped}")
    print(f"  خطا: {failed}")

    if dry_run and updated > 0:
        print(f"\n  برای اعمال {updated} تغییر، دستور زیر را اجرا کنید:")
        print(f"  python update_prices.py --apply" + (f" --sheet \"{args.sheet}\"" if args.sheet else ""))


if __name__ == '__main__':
    main()
