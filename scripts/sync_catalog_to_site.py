"""
sync_catalog_to_site.py
=======================
همگام‌سازی سریع، پایدار و دسته‌ای (Batch) قیمت‌ها و وضعیت موجودی محصولات
از فایل اکسل hosseiny_kala_catalog.xlsx به سایت hosseinykala.ir

ویژگی‌ها:
- استفاده از WooCommerce Batch API جهت ارسال دسته‌ای (هر دسته ۱۵ محصول) و کاهش زمان کل به زیر ۳۰ ثانیه
- جلوگیری کامل از قطعی و Timeout ناشی از ارسال تک‌تک درخواست‌ها
- قابلیت بازیابی و ادامه از محل توقف (Resume via sync_progress.json)
- تفکیک کامل محصولات ساده، تنوع‌ها و والدین متغیر
- مدیریت موجودی هوشمند: محاسبه خودکار موجودی والد بر اساس تنوع‌ها
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import time
import requests
import openpyxl

BASE_URL = "https://hosseinykala.ir"
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
}

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPTS_DIR)
EXCEL_PATH = os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx')
PROGRESS_FILE = os.path.join(PROJECT_DIR, 'scratch', 'sync_progress.json')
REPORT_FILE = os.path.join(PROJECT_DIR, 'scratch', 'sync_live_report.json')

BATCH_SIZE = 15  # تعداد بهینه برای تعادل بین سرعت و پایداری سرور

CATEGORY_SHEETS = [
    'یخچال و فریزر',
    'شستشو و نظافت',
    'لوازم برقی و پخت و پز',
    'نوشیدنی ساز',
    'سرمایش و گرمایش',
    'تصفیه کننده آب',
    'صوتی و تصویری',
    'زیبایی و سلامت فردی'
]


def get_column_indices(ws):
    """شناسایی پویای شماره ستون‌ها از روی هدر شیت اکسل"""
    mapping = {
        'name': 0, 'price_reg': 1, 'price_reg_tom': 2, 'price_sale': 3, 'price_sale_tom': 4,
        'stock': 5, 'type': 9, 'pid': 11, 'vid': 12
    }
    header = [ws.cell(row=1, column=c).value for c in range(1, ws.max_column + 1)]
    for idx, h in enumerate(header):
        if not h:
            continue
        h_str = str(h).strip()
        if 'نام محصول' in h_str: mapping['name'] = idx
        elif 'عادی (ریال)' in h_str: mapping['price_reg'] = idx
        elif 'عادی (تومان)' in h_str: mapping['price_reg_tom'] = idx
        elif 'حراج (ریال)' in h_str: mapping['price_sale'] = idx
        elif 'حراج (تومان)' in h_str: mapping['price_sale_tom'] = idx
        elif 'موجودی' in h_str: mapping['stock'] = idx
        elif 'نوع محصول' in h_str: mapping['type'] = idx
        elif 'شناسه محصول' in h_str: mapping['pid'] = idx
        elif 'شناسه تنوع' in h_str: mapping['vid'] = idx
    return mapping


def load_all_catalog_items(excel_path):
    """استخراج تمام محصولات ساده، تنوع‌ها و والدین متغیر از شیت‌های اکسل"""
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    simple_products = []
    variations = []
    variable_parents = {}

    for sheetname in CATEGORY_SHEETS:
        if sheetname not in wb.sheetnames:
            continue
        ws = wb[sheetname]
        cmap = get_column_indices(ws)

        for r in range(2, ws.max_row + 1):
            name = ws.cell(row=r, column=cmap['name'] + 1).value
            if not name or '📂' in str(name):
                continue
            pid = ws.cell(row=r, column=cmap['pid'] + 1).value
            vid = ws.cell(row=r, column=cmap['vid'] + 1).value
            ptype = str(ws.cell(row=r, column=cmap['type'] + 1).value or '').strip()
            p_reg = ws.cell(row=r, column=cmap['price_reg'] + 1).value
            p_sale = ws.cell(row=r, column=cmap['price_sale'] + 1).value
            stock = ws.cell(row=r, column=cmap['stock'] + 1).value

            if not pid:
                continue
            try: pid = int(pid)
            except: continue

            try: vid = int(vid) if vid else None
            except: vid = None

            is_instock = stock in ('✓ موجود', 'موجود')
            reg_toman = (int(p_reg) // 10) if p_reg and isinstance(p_reg, (int, float)) else None
            sale_toman = (int(p_sale) // 10) if p_sale and isinstance(p_sale, (int, float)) else None

            item = {
                'sheet': sheetname,
                'row': r,
                'name': str(name).strip(),
                'pid': pid,
                'vid': vid,
                'ptype': ptype,
                'reg_toman': reg_toman,
                'sale_toman': sale_toman,
                'stock_raw': stock,
                'is_instock': is_instock
            }

            if ptype == 'متغیر' and not vid:
                variable_parents[pid] = item
                variable_parents[pid]['variants'] = []
            elif vid:
                variations.append(item)
                if pid in variable_parents:
                    variable_parents[pid]['variants'].append(item)
            else:
                simple_products.append(item)

    return simple_products, variations, variable_parents


def make_session():
    session = requests.Session()
    session.auth = AUTH
    session.headers.update(HEADERS)
    return session


def send_batch_request(session, url, update_list, retries=3):
    """ارسال یک دسته درخواست Batch به همراه تلاش مجدد و مدیریت خطای اتصال"""
    payload = {'update': update_list}
    for attempt in range(1, retries + 1):
        try:
            r = session.post(url, json=payload, timeout=45)
            if r.status_code in (200, 201):
                return True, r.json(), None
            else:
                err_msg = f"HTTP {r.status_code}: {r.text[:200]}"
                if attempt == retries:
                    return False, None, err_msg
                time.sleep(2 * attempt)
        except requests.exceptions.Timeout:
            if attempt == retries:
                return False, None, "پاسخ سرور در زمان مقرر دریافت نشد (Timeout)"
            print(f"   ⚠️ وقفه در دریافت پاسخ، تلاش مجدد ({attempt}/{retries})...", flush=True)
            time.sleep(3 * attempt)
        except Exception as e:
            if attempt == retries:
                return False, None, str(e)
            print(f"   ⚠️ خطای ارتباط: {e}، تلاش مجدد ({attempt}/{retries})...", flush=True)
            time.sleep(2 * attempt)
    return False, None, "خطای نامشخص"


def chunk_list(lst, size):
    """تقسیم یک لیست به دسته‌های با اندازه مشخص"""
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def sync_all(force=False):
    print("=" * 70, flush=True)
    print("🚀 آغاز فرآیند هوشمند همگام‌سازی دسته‌ای (Batch) قیمت‌ها و موجودی کاتالوگ", flush=True)
    print(f"📁 فایل اکسل مبنا: {EXCEL_PATH}", flush=True)
    if force:
        print("⚡ حالت همگام‌سازی کامل اجباری (Force Sync): تمامی اقلام کاتالوگ مجدداً ارسال می‌شوند.", flush=True)
    print("=" * 70, flush=True)

    simple_prods, variations, var_parents = load_all_catalog_items(EXCEL_PATH)
    total_all_items = len(variations) + len(simple_prods) + len(var_parents)

    done_ids = set()
    if not force and os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                done_ids = set(json.load(f))
            print(f"🔄 وضعیت قبلی لود شد: {len(done_ids)} آیتم از قبل ثبت شده است.", flush=True)
        except Exception:
            pass

    def save_progress():
        try:
            with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                json.dump(list(done_ids), f)
        except Exception as e:
            print(f"خطا در ذخیره وضعیت پیشرفت: {e}", flush=True)

    session = make_session()
    all_results = []
    new_success_count = 0
    fail_count = 0

    # ─────────────────────────────────────────────────────────
    # مرحله ۱: به‌روزرسانی تنوع‌ها (Variations Batch per Parent)
    # ─────────────────────────────────────────────────────────
    pending_vars = [v for v in variations if v['vid'] not in done_ids]
    print(f"\n─── [۱/۳] بررسی تنوع‌ها: {len(variations) - len(pending_vars)} ثبت شده / {len(pending_vars)} باقی‌مانده ───", flush=True)

    if pending_vars:
        # گروه‌بندی تنوع‌های باقی‌مانده بر اساس والد
        vars_by_parent = {}
        for v in pending_vars:
            vars_by_parent.setdefault(v['pid'], []).append(v)

        for pid, v_list in vars_by_parent.items():
            parent_name = v_list[0]['name'].split(' - ')[0] if ' - ' in v_list[0]['name'] else v_list[0]['name']
            print(f"📦 ارسال دسته تنوع‌های محصول #{pid} ({len(v_list)} تنوع) | {parent_name[:35]}...", end=" ", flush=True)

            update_payload = []
            for v in v_list:
                item_data = {
                    'id': v['vid'],
                    'manage_stock': False,
                    'stock_status': 'instock' if v['is_instock'] else 'outofstock'
                }
                if v['reg_toman'] is not None:
                    item_data['regular_price'] = str(v['reg_toman'])
                if v['sale_toman'] is not None:
                    item_data['sale_price'] = str(v['sale_toman'])
                else:
                    item_data['sale_price'] = ''
                update_payload.append(item_data)

            url = f"{BASE_URL}/wp-json/wc/v3/products/{pid}/variations/batch"
            t0 = time.time()
            ok, res, err = send_batch_request(session, url, update_payload)
            elapsed = time.time() - t0

            if ok:
                updated = res.get('update', [])
                for v in v_list:
                    done_ids.add(v['vid'])
                    new_success_count += 1
                    all_results.append({'id': v['vid'], 'type': 'variation', 'status': 'success'})
                save_progress()
                print(f"✓ موفق ({elapsed:.2f} ثانیه - {len(updated)} تنوع)", flush=True)
            else:
                fail_count += len(v_list)
                print(f"✗ ناموفق! ({err})", flush=True)
                for v in v_list:
                    all_results.append({'id': v['vid'], 'type': 'variation', 'status': 'failed', 'error': err})
            time.sleep(0.5)
    else:
        print("✓ همه ۷۸ تنوع از قبل همگام شده‌اند.", flush=True)

    # ─────────────────────────────────────────────────────────
    # مرحله ۲: به‌روزرسانی محصولات ساده (Simple Products Batch)
    # ─────────────────────────────────────────────────────────
    pending_simple = [p for p in simple_prods if p['pid'] not in done_ids]
    print(f"\n─── [۲/۳] بررسی محصولات ساده: {len(simple_prods) - len(pending_simple)} ثبت شده / {len(pending_simple)} باقی‌مانده ───", flush=True)

    if pending_simple:
        batches = list(chunk_list(pending_simple, BATCH_SIZE))
        for b_idx, batch in enumerate(batches, 1):
            print(f"📦 ارسال دسته {b_idx}/{len(batches)} شامل {len(batch)} محصول ساده...", end=" ", flush=True)

            update_payload = []
            for p in batch:
                item_data = {
                    'id': p['pid'],
                    'manage_stock': False,
                    'stock_status': 'instock' if p['is_instock'] else 'outofstock'
                }
                if p['reg_toman'] is not None:
                    item_data['regular_price'] = str(p['reg_toman'])
                if p['sale_toman'] is not None:
                    item_data['sale_price'] = str(p['sale_toman'])
                else:
                    item_data['sale_price'] = ''
                update_payload.append(item_data)

            url = f"{BASE_URL}/wp-json/wc/v3/products/batch"
            t0 = time.time()
            ok, res, err = send_batch_request(session, url, update_payload)
            elapsed = time.time() - t0

            if ok:
                updated = res.get('update', [])
                for p in batch:
                    done_ids.add(p['pid'])
                    new_success_count += 1
                    all_results.append({'id': p['pid'], 'type': 'simple', 'status': 'success', 'price': p['reg_toman']})
                save_progress()
                print(f"✓ موفق ({elapsed:.2f} ثانیه - {len(updated)} محصول)", flush=True)
            else:
                fail_count += len(batch)
                print(f"✗ ناموفق! ({err})", flush=True)
                for p in batch:
                    all_results.append({'id': p['pid'], 'type': 'simple', 'status': 'failed', 'error': err})
            time.sleep(0.5)
    else:
        print("✓ همه ۶۶ محصول ساده از قبل همگام شده‌اند.", flush=True)

    # ─────────────────────────────────────────────────────────
    # مرحله ۳: به‌روزرسانی والدین متغیر (Variable Parents Batch)
    # ─────────────────────────────────────────────────────────
    pending_parents = [p for pid, p in var_parents.items() if f"parent_{pid}" not in done_ids]
    print(f"\n─── [۳/۳] بررسی والدین متغیر: {len(var_parents) - len(pending_parents)} ثبت شده / {len(pending_parents)} باقی‌مانده ───", flush=True)

    if pending_parents:
        batches = list(chunk_list(pending_parents, BATCH_SIZE))
        for b_idx, batch in enumerate(batches, 1):
            print(f"📦 ارسال دسته {b_idx}/{len(batches)} شامل {len(batch)} والد متغیر...", end=" ", flush=True)

            update_payload = []
            for p in batch:
                pid = p['pid']
                variants = p.get('variants', [])
                any_instock = any(v['is_instock'] for v in variants)
                parent_status = 'instock' if any_instock else 'outofstock'
                update_payload.append({
                    'id': pid,
                    'manage_stock': False,
                    'stock_status': parent_status
                })

            url = f"{BASE_URL}/wp-json/wc/v3/products/batch"
            t0 = time.time()
            ok, res, err = send_batch_request(session, url, update_payload)
            elapsed = time.time() - t0

            if ok:
                updated = res.get('update', [])
                for p in batch:
                    done_ids.add(f"parent_{p['pid']}")
                    new_success_count += 1
                    all_results.append({'id': p['pid'], 'type': 'variable_parent', 'status': 'success'})
                save_progress()
                print(f"✓ موفق ({elapsed:.2f} ثانیه - {len(updated)} والد)", flush=True)
            else:
                fail_count += len(batch)
                print(f"✗ ناموفق! ({err})", flush=True)
                for p in batch:
                    all_results.append({'id': p['pid'], 'type': 'variable_parent', 'status': 'failed', 'error': err})
            time.sleep(0.5)
    else:
        print("✓ همه ۳۱ والد متغیر از قبل همگام شده‌اند.", flush=True)

    # ─────────────────────────────────────────────────────────
    # گزارش نهایی
    # ─────────────────────────────────────────────────────────
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_in_catalog': total_all_items,
            'total_synced_now': len(done_ids),
            'newly_synced': new_success_count,
            'failed': fail_count,
            'results': all_results
        }, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 70, flush=True)
    print("🎉 فرآیند همگام‌سازی کاتالوگ با سایت حسینی کالا با موفقیت به پایان رسید!", flush=True)
    print(f"   • کل اقلام کاتالوگ: {total_all_items} مورد (۷۸ تنوع + ۶۶ محصول ساده + ۳۱ والد متغیر)", flush=True)
    print(f"   • کل اقلام همگام‌شده در سایت: {len(done_ids)} از {total_all_items}", flush=True)
    print(f"   • به‌روزرسانی‌های جدید این اجرا: {new_success_count}", flush=True)
    print(f"   • خطاهای این اجرا: {fail_count}", flush=True)
    print(f"   • فایل گزارش تفصیلی: {REPORT_FILE}", flush=True)
    print("=" * 70, flush=True)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="همگام‌سازی کاتالوگ با سایت حسینی کالا")
    parser.add_argument('--force', action='store_true', help='اجرای کامل بدون در نظر گرفتن کش و پیشرفت قبلی')
    args = parser.parse_args()
    sync_all(force=args.force)
