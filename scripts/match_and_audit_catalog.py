"""
match_and_audit_catalog.py
==========================
موتور جامع تطبیق هوشمند، اعتبارسنجی لوپ و استانداردسازی کاتالوگ حسینی کالا:
- تفکیک دقیق محصولات والد سایت vs تنوع‌ها vs اقلام قبلی اکسل vs اقلام جدید
- عدم تداخل کدهای مدل (مانند 990c و 990S، SG518 و S517، 8vw1 و 9tw1 و ...)
- اتصال رنگ‌های وستینگهاوس، دیپوینت، ایستکول و مینی کلور به Variation ID های مربوطه
- ثبت اقلام ناموجود (تعداد 0 یا منفی) با برچسب «✗ ناموجود»
- تولید پایگاه داده نگاشت استاندارد data/inventory_mapping_standard.json
"""

import os
import sys
import json
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
PARSED_INV_FILE = os.path.join(DATA_DIR, 'inventory_normalized.json')
REF_FILE = os.path.join(DATA_DIR, 'current_catalog_reference.json')
MAPPING_STANDARD_FILE = os.path.join(DATA_DIR, 'inventory_mapping_standard.json')
OUT_MATCHED_FILE = os.path.join(DATA_DIR, 'inventory_matched_results.json')

def normalize_text(text):
    if not text:
        return ""
    text = str(text).lower()
    text = text.replace('ي', 'ی').replace('ك', 'ک').replace('‌', ' ').replace('-', ' ').replace('_', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def run_matching_and_auditing():
    print("=" * 70)
    print("شروع فرآیند تطبیق و ممیزی کاتالوگ حسینی کالا (نسخه بهینه‌شده با فیدبک)")
    print("=" * 70)

    with open(PARSED_INV_FILE, 'r', encoding='utf-8') as f:
        incoming_items = json.load(f)

    with open(REF_FILE, 'r', encoding='utf-8') as f:
        catalog_ref = json.load(f)

    live_products = catalog_ref['live_products']
    live_by_id = {p['id']: p for p in live_products}
    old_excel_items = catalog_ref['excel_items']

    matched_results = []
    stats = {
        "total_incoming": len(incoming_items),
        "matched_site_parent": 0,
        "matched_site_variation": 0,
        "matched_old_offline": 0,
        "new_offline_items": 0,
        "accounting_rows": 0,
        "in_stock_count": 0,
        "out_of_stock_count": 0
    }

    for it in incoming_items:
        raw_idx = it['raw_index']
        raw_desc = it['cleaned_raw_desc']
        raw_qty = it['raw_quantity']
        in_stock = it['in_stock']
        brand = it['brand']
        model_code = it.get('model_code', '')
        cat = it['category']
        std_name = it['standard_name']

        if in_stock:
            stats["in_stock_count"] += 1
        else:
            stats["out_of_stock_count"] += 1

        norm_desc = normalize_text(raw_desc)
        norm_model = normalize_text(model_code)

        cat_slug = {
            'یخچال و فریزر': 'REF',
            'شستشو و نظافت': 'WASH_CLEAN',
            'لوازم برقی و پخت و پز': 'COOK_KITCHEN',
            'نوشیدنی ساز': 'BEVERAGE',
            'سرمایش و گرمایش': 'CLIMATE',
            'تصفیه کننده آب': 'WATER_TREAT',
            'صوتی و تصویری': 'AUDIO_VIDEO',
            'زیبایی و سلامت فردی': 'PERSONAL_CARE'
        }.get(cat, 'GEN')

        brand_slug = re.sub(r'[^a-zA-Z0-9]', '', normalize_text(brand)).upper() or 'GEN'
        model_slug = re.sub(r'[^a-zA-Z0-9]', '', norm_model).upper() or 'GEN'
        std_key = f"{cat_slug}__{brand_slug}__{model_slug}__{raw_idx}"

        match_info = {
            "raw_index": raw_idx,
            "raw_desc": raw_desc,
            "raw_quantity": raw_qty,
            "in_stock_label": "✓ موجود" if in_stock else "✗ ناموجود",
            "category": cat,
            "subcategory": brand,
            "brand": brand,
            "model_code": model_code,
            "standard_name": std_name,
            "standard_key": std_key,
            "match_type": None,
            "site_status": "در سایت تعریف نشده",
            "product_id": None,
            "variation_id": None,
            "variant_attr": "",
            "price_regular": None,
            "price_sale": None,
            "link": "",
            "sku": ""
        }

        # ۱. ردیف حسابداری
        if "کسرواضافات" in norm_desc or "کسورات" in norm_desc:
            match_info["match_type"] = "ACCOUNTING_ADJUSTMENT"
            match_info["site_status"] = "ردیف حسابداری"
            stats["accounting_rows"] += 1
            matched_results.append(match_info)
            continue

        # ۲. اقلام متغیر و تنوع‌های سایت (Variations)
        # وستینگهاوس
        if "وستینگهوس" in norm_desc or "وستینگهاوس" in norm_desc:
            # توستر ۳۶۳۷
            if "توستر" in norm_desc:
                p = live_by_id.get(3637)
                v_target = next((v for v in p['variations'] if ('آبی' in norm_desc and 'آبی' in str(v.get('attributes'))) or ('کرم' in norm_desc and 'کرم' in str(v.get('attributes')))), None) if p else None
                if v_target:
                    match_info["match_type"] = "EXACT_SITE_VARIATION"
                    match_info["site_status"] = "ثبت‌شده در سایت"
                    match_info["product_id"] = 3637
                    match_info["variation_id"] = v_target['variation_id']
                    match_info["variant_attr"] = str(v_target.get('attributes'))
                    match_info["price_regular"] = v_target.get('price_regular')
                    match_info["price_sale"] = v_target.get('price_sale')
                    match_info["link"] = f"https://hosseinykala.ir/?p={v_target['variation_id']}"
                    stats["matched_site_variation"] += 1
                    matched_results.append(match_info)
                    continue

            # کتری برقی ۳۶۶۴
            if "کتری" in norm_desc:
                p = live_by_id.get(3664)
                v_target = next((v for v in p['variations'] if ('آبی' in norm_desc and 'آبی' in str(v.get('attributes'))) or ('کرم' in norm_desc and 'کرم' in str(v.get('attributes')))), None) if p else None
                if v_target:
                    match_info["match_type"] = "EXACT_SITE_VARIATION"
                    match_info["site_status"] = "ثبت‌شده در سایت"
                    match_info["product_id"] = 3664
                    match_info["variation_id"] = v_target['variation_id']
                    match_info["variant_attr"] = str(v_target.get('attributes'))
                    match_info["price_regular"] = v_target.get('price_regular')
                    match_info["price_sale"] = v_target.get('price_sale')
                    match_info["link"] = f"https://hosseinykala.ir/?p={v_target['variation_id']}"
                    stats["matched_site_variation"] += 1
                    matched_results.append(match_info)
                    continue

            # مخلوط کن ۳۶۴۰
            if "مخلوط کن" in norm_desc:
                p = live_by_id.get(3640)
                v_target = next((v for v in p['variations'] if ('آبی' in norm_desc and 'آبی' in str(v.get('attributes'))) or ('کرم' in norm_desc and 'کرم' in str(v.get('attributes')))), None) if p else None
                if v_target:
                    match_info["match_type"] = "EXACT_SITE_VARIATION"
                    match_info["site_status"] = "ثبت‌شده در سایت"
                    match_info["product_id"] = 3640
                    match_info["variation_id"] = v_target['variation_id']
                    match_info["variant_attr"] = str(v_target.get('attributes'))
                    match_info["price_regular"] = v_target.get('price_regular')
                    match_info["price_sale"] = v_target.get('price_sale')
                    match_info["link"] = f"https://hosseinykala.ir/?p={v_target['variation_id']}"
                    stats["matched_site_variation"] += 1
                    matched_results.append(match_info)
                    continue

            # همزن ۳۶۴۵
            if "همزن" in norm_desc:
                p = live_by_id.get(3645)
                v_target = next((v for v in p['variations'] if ('آبی' in norm_desc and 'آبی' in str(v.get('attributes'))) or ('کرم' in norm_desc and 'کرم' in str(v.get('attributes')))), None) if p else None
                if v_target:
                    match_info["match_type"] = "EXACT_SITE_VARIATION"
                    match_info["site_status"] = "ثبت‌شده در سایت"
                    match_info["product_id"] = 3645
                    match_info["variation_id"] = v_target['variation_id']
                    match_info["variant_attr"] = str(v_target.get('attributes'))
                    match_info["price_regular"] = v_target.get('price_regular')
                    match_info["price_sale"] = v_target.get('price_sale')
                    match_info["link"] = f"https://hosseinykala.ir/?p={v_target['variation_id']}"
                    stats["matched_site_variation"] += 1
                    matched_results.append(match_info)
                    continue

        # دیپوینت T7 تنوع رنگ ۲۵۸۵
        if "دیپوینت" in norm_desc or "دیپونت" in norm_desc:
            if "t7" in norm_desc:
                p = live_by_id.get(2585)
                v_target = next((v for v in p['variations'] if ('سفید' in norm_desc and 'سفید' in str(v.get('attributes'))) or ('استیل' in norm_desc and ('نقره' in str(v.get('attributes')) or 'استیل' in str(v.get('attributes'))))), None) if p else None
                if v_target:
                    match_info["match_type"] = "EXACT_SITE_VARIATION"
                    match_info["site_status"] = "ثبت‌شده در سایت"
                    match_info["product_id"] = 2585
                    match_info["variation_id"] = v_target['variation_id']
                    match_info["variant_attr"] = str(v_target.get('attributes'))
                    match_info["price_regular"] = v_target.get('price_regular')
                    match_info["price_sale"] = v_target.get('price_sale')
                    match_info["link"] = f"https://hosseinykala.ir/?p={v_target['variation_id']}"
                    stats["matched_site_variation"] += 1
                    matched_results.append(match_info)
                    continue

        # ایستکول ۹ فوت ۲۶۹۱
        if "ایستکول" in norm_desc and "9" in norm_desc:
            p = live_by_id.get(2691)
            v_target = next((v for v in p['variations'] if ('سفید' in norm_desc and 'سفید' in str(v.get('attributes'))) or ('نوک مدادی' in norm_desc and ('استیل' in str(v.get('attributes')) or 'مدادی' in str(v.get('attributes'))))), None) if p else None
            if v_target:
                match_info["match_type"] = "EXACT_SITE_VARIATION"
                match_info["site_status"] = "ثبت‌شده در سایت"
                match_info["product_id"] = 2691
                match_info["variation_id"] = v_target['variation_id']
                match_info["variant_attr"] = str(v_target.get('attributes'))
                match_info["price_regular"] = v_target.get('price_regular')
                match_info["price_sale"] = v_target.get('price_sale')
                match_info["link"] = f"https://hosseinykala.ir/?p={v_target['variation_id']}"
                stats["matched_site_variation"] += 1
                matched_results.append(match_info)
                continue

        # مینی کلور ۲۴۳۱
        if "یخچال" in norm_desc and "کلور" in norm_desc and "مینی" in norm_desc:
            p = live_by_id.get(2431)
            v_target = None
            if p:
                if "آبی پاستیلی" in norm_desc:
                    v_target = next((v for v in p['variations'] if 'آبی' in str(v.get('attributes'))), None)
                elif "سبز پاستیلی" in norm_desc:
                    v_target = next((v for v in p['variations'] if 'سبز' in str(v.get('attributes'))), None)
                elif "قرمز" in norm_desc or "re01" in norm_desc:
                    v_target = next((v for v in p['variations'] if 'قرمز' in str(v.get('attributes'))), None)
                elif "سفید" in norm_desc:
                    v_target = next((v for v in p['variations'] if 'سفید' in str(v.get('attributes'))), None)
                elif "مشکی مات" in norm_desc:
                    v_target = next((v for v in p['variations'] if 'مشکی' in str(v.get('attributes'))), None)

            if v_target:
                match_info["match_type"] = "EXACT_SITE_VARIATION"
                match_info["site_status"] = "ثبت‌شده در سایت"
                match_info["product_id"] = 2431
                match_info["variation_id"] = v_target['variation_id']
                match_info["variant_attr"] = str(v_target.get('attributes'))
                match_info["price_regular"] = v_target.get('price_regular')
                match_info["price_sale"] = v_target.get('price_sale')
                match_info["link"] = f"https://hosseinykala.ir/?p={v_target['variation_id']}"
                stats["matched_site_variation"] += 1
                matched_results.append(match_info)
                continue

        # کلور کمبی 27 فوت مدل FRNT101 تنوع رنگ ۲۴۰۸
        if "کلور" in norm_desc and "101" in norm_desc and ("27" in norm_desc or "استیل" in norm_desc or "کره ای" in norm_desc):
            p = live_by_id.get(2408)
            v_target = None
            if p:
                if "استیل" in norm_desc:
                    v_target = next((v for v in p['variations'] if 'استیل' in str(v.get('attributes'))), None)
                elif "سفید" in norm_desc:
                    v_target = next((v for v in p['variations'] if 'سفید' in str(v.get('attributes'))), None)
            if v_target:
                match_info["match_type"] = "EXACT_SITE_VARIATION"
                match_info["site_status"] = "ثبت‌شده در سایت"
                match_info["product_id"] = 2408
                match_info["variation_id"] = v_target['variation_id']
                match_info["variant_attr"] = str(v_target.get('attributes'))
                match_info["price_regular"] = v_target.get('price_regular')
                match_info["price_sale"] = v_target.get('price_sale')
                match_info["link"] = f"https://hosseinykala.ir/?p={v_target['variation_id']}"
                stats["matched_site_variation"] += 1
                matched_results.append(match_info)
                continue

        # جاروبرقی دونالکس 750 تنوع رنگ ۳۵۱۰
        if "دونالکس" in norm_desc and "750" in norm_desc:
            p = live_by_id.get(3510)
            v_target = None
            if p:
                if "طلایی" in norm_desc:
                    v_target = next((v for v in p['variations'] if 'طلایی' in str(v.get('attributes'))), None)
                elif "سورمه" in norm_desc or "سرمه" in norm_desc:
                    v_target = next((v for v in p['variations'] if 'سرمه' in str(v.get('attributes'))), None)
            if v_target:
                match_info["match_type"] = "EXACT_SITE_VARIATION"
                match_info["site_status"] = "ثبت‌شده در سایت"
                match_info["product_id"] = 3510
                match_info["variation_id"] = v_target['variation_id']
                match_info["variant_attr"] = str(v_target.get('attributes'))
                match_info["price_regular"] = v_target.get('price_regular')
                match_info["price_sale"] = v_target.get('price_sale')
                match_info["link"] = f"https://hosseinykala.ir/?p={v_target['variation_id']}"
                stats["matched_site_variation"] += 1
                matched_results.append(match_info)
                continue

        # لباسشویی کلور 10 کیلو تنوع رنگ ۳۵۷۳
        if "کلور" in norm_desc and "10" in norm_desc and ("سبز" in norm_desc or "کرم" in norm_desc):
            p = live_by_id.get(3573)
            v_target = None
            if p:
                if "سبز" in norm_desc:
                    v_target = next((v for v in p['variations'] if 'سبز' in str(v.get('attributes'))), None)
                elif "کرم" in norm_desc:
                    v_target = next((v for v in p['variations'] if 'کرم' in str(v.get('attributes'))), None)
            if v_target:
                match_info["match_type"] = "EXACT_SITE_VARIATION"
                match_info["site_status"] = "ثبت‌شده در سایت"
                match_info["product_id"] = 3573
                match_info["variation_id"] = v_target['variation_id']
                match_info["variant_attr"] = str(v_target.get('attributes'))
                match_info["price_regular"] = v_target.get('price_regular')
                match_info["price_sale"] = v_target.get('price_sale')
                match_info["link"] = f"https://hosseinykala.ir/?p={v_target['variation_id']}"
                stats["matched_site_variation"] += 1
                matched_results.append(match_info)
                continue

        # سرویس قابلمه اویز ۱۰ پارچه سلین تنوع رنگ ۳۳۵۷
        if "سرویس قابلمه" in norm_desc and "اویز" in norm_desc and "10" in norm_desc and "سرمه" in norm_desc:
            p = live_by_id.get(3357)
            v_target = next((v for v in p['variations'] if 'سرمه' in str(v.get('attributes'))), None) if p else None
            if v_target:
                match_info["match_type"] = "EXACT_SITE_VARIATION"
                match_info["site_status"] = "ثبت‌شده در سایت"
                match_info["product_id"] = 3357
                match_info["variation_id"] = v_target['variation_id']
                match_info["variant_attr"] = str(v_target.get('attributes'))
                match_info["price_regular"] = v_target.get('price_regular')
                match_info["price_sale"] = v_target.get('price_sale')
                match_info["link"] = f"https://hosseinykala.ir/?p={v_target['variation_id']}"
                stats["matched_site_variation"] += 1
                matched_results.append(match_info)
                continue

        # قابلمه‌های اویز سایزدار ۳۵۹۶
        if "قابلمه" in norm_desc and "اویز" in norm_desc and any(str(s) in norm_desc for s in [16, 18, 20, 22, 24, 26, 28, 30, 32]):
            p = live_by_id.get(3596)
            size_match = re.search(r'(16|18|20|22|24|26|28|30|32)', norm_desc)
            if p and size_match:
                sz = size_match.group(1)
                v_target = next((v for v in p['variations'] if sz in str(v.get('attributes', {}))), None)
                if v_target:
                    match_info["match_type"] = "EXACT_SITE_VARIATION"
                    match_info["site_status"] = "ثبت‌شده در سایت"
                    match_info["product_id"] = 3596
                    match_info["variation_id"] = v_target['variation_id']
                    match_info["variant_attr"] = f"سایز: {sz}"
                    match_info["price_regular"] = v_target.get('price_regular')
                    match_info["price_sale"] = v_target.get('price_sale')
                    match_info["link"] = f"https://hosseinykala.ir/?p={v_target['variation_id']}"
                    stats["matched_site_variation"] += 1
                    matched_results.append(match_info)
                    continue

        # ۳. عدم تداخل مدل‌های مجزا (مانند دوو 990c، دوو 990S، دوو 991s، دوو 8 کیلو، هیمالیا آیس پول، آلتون SG518، کلور 8vw1)
        # این اقلام باید به عنوان محصول جدید/آفلاین جداگانه ثبت شوند تا با محصولات سایت اشتباه گرفته نشوند
        distinct_models = {
            "990c": ("شستشو و نظافت", "دوو", "ماشین لباسشویی اتوماتیک دوو 9 کیلویی سینیور مدل 990c سفید"),
            "990s": ("شستشو و نظافت", "دوو", "ماشین لباسشویی اتوماتیک دوو 9 کیلویی سینیور مدل 990S"),
            "991s": ("شستشو و نظافت", "دوو", "ماشین لباسشویی اتوماتیک دوو 9 کیلویی سینیور مدل 991s"),
            "8vw1": ("شستشو و نظافت", "کلور", "ماشین لباسشویی 8 کیلویی کلور مدل 8vw1 سفید"),
            "sg518": ("لوازم برقی و پخت و پز", "آلتون", "گاز صفحه ای آلتون استیل مدل SG518"),
            "7303": ("لوازم برقی و پخت و پز", "آلتون", "فر توکار آلتون مدل 7303"),
            "md5w": ("لوازم برقی و پخت و پز", "آلتون", "اجاق گاز مبله فردار آلتون مدل MD5W سفید"),
            "b3115": ("تصفیه کننده آب", "بوتان", "آبگرمکن دیواری بوتان مدل B3115"),
            "60mw": ("یخچال و فریزر", "هیمالیا", "هیمالیا آیس پول 60MW"),
            "rf84102e2": ("یخچال و فریزر", "نیکسان", "یخچال فریزر نیکسان مدل RF84102E2"),
        }

        matched_distinct = False
        for k_model, (d_cat, d_brand, d_name) in distinct_models.items():
            if k_model in norm_model or k_model in norm_desc:
                match_info["match_type"] = "NEW_OFFLINE_ITEM" if k_model not in ["60mw", "sg518"] else "EXISTING_OFFLINE_CATALOG"
                match_info["site_status"] = "در سایت تعریف نشده"
                match_info["category"] = d_cat
                match_info["subcategory"] = d_brand
                match_info["brand"] = d_brand
                stats["new_offline_items"] += 1
                matched_results.append(match_info)
                matched_distinct = True
                break

        if matched_distinct:
            continue

        # ۴. تطبیق با محصولات والد سایت (Parent Products)
        best_live = None
        if "75" in norm_desc and any(k in norm_desc for k in ["هاورسون", "هاورسن", "aversen", "averson"]):
            best_live = live_by_id.get(3531)
        elif "85" in norm_desc and any(k in norm_desc for k in ["aversen", "averson", "هاورسن", "هاورسون"]):
            best_live = live_by_id.get(3534)
        elif "32" in norm_desc and any(k in norm_desc for k in ["aversen", "averson", "هاورسن", "هاورسون"]):
            best_live = live_by_id.get(3516)
        elif "65" in norm_desc and any(k in norm_desc for k in ["هاورسن", "هاورسون", "aversen"]):
            best_live = live_by_id.get(3523)
        elif "55" in norm_desc and any(k in norm_desc for k in ["هاورسن", "هاورسون", "aversen"]):
            best_live = live_by_id.get(3520)
        elif "افترون" in norm_desc and "آب" in norm_desc:
            best_live = live_by_id.get(3301)
        elif "نیکائی" in norm_desc and "1206" in norm_desc:
            best_live = live_by_id.get(3312)
        elif "سافت واتر" in norm_desc:
            best_live = live_by_id.get(2766)
        elif "هوم گلد" in norm_desc or "هومگلد" in norm_desc:
            best_live = live_by_id.get(3504)
        elif "c.c.k" in norm_desc or "سی سی کا" in norm_desc:
            best_live = live_by_id.get(3305)
        elif "دلمونتی" in norm_desc and "580" in norm_desc:
            best_live = live_by_id.get(3631)
        elif "هیتاچی" in norm_desc and "سطلی" in norm_desc and "1200" not in norm_desc:
            best_live = live_by_id.get(2519)
        elif "دونالکس" in norm_desc and "750" in norm_desc:
            best_live = live_by_id.get(3510)
        elif "بست" in norm_desc and "جارو" in norm_desc:
            best_live = live_by_id.get(2885)
        elif "کورکماز" in norm_desc and "a331" in norm_desc:
            best_live = live_by_id.get(3673)
        elif "دونالکس" in norm_desc and "185" in norm_desc:
            best_live = live_by_id.get(3457)
        elif "سماوری گرنویک" in norm_desc or "سماور" in norm_desc and "گرنویک" in norm_desc:
            best_live = live_by_id.get(3681)
        elif "اسپرسو" in norm_desc and "گرنویک" in norm_desc:
            best_live = live_by_id.get(3679)
        elif "اسپرسو" in norm_desc and "480" in norm_desc:
            best_live = live_by_id.get(3013)
        elif "اسپرسو" in norm_desc and "475" in norm_desc:
            best_live = live_by_id.get(3016)
        elif "ابمیوه" in norm_desc and "دونالکس" in norm_desc and "120" in norm_desc:
            best_live = live_by_id.get(3711)
        elif "ابمیوه" in norm_desc and "دونالکس" in norm_desc and "110" in norm_desc:
            best_live = live_by_id.get(3019)
        elif "اپیلیدی" in norm_desc and "پرومارون" in norm_desc and "614" in norm_desc:
            best_live = live_by_id.get(3494)
        elif "اتو" in norm_desc and "دونالکس" in norm_desc and "815" in norm_desc:
            best_live = live_by_id.get(3007)
        elif "اتو" in norm_desc and ("فلیپس" in norm_desc or "فیلیپس" in norm_desc) and "5040" in norm_desc:
            best_live = live_by_id.get(3271)
        elif "پرومارون" in norm_desc and "1115" in norm_desc:
            best_live = live_by_id.get(3484)
        elif "پرومارون" in norm_desc and "1116" in norm_desc:
            best_live = live_by_id.get(3488)
        elif "پرومارون" in norm_desc and "1113" in norm_desc:
            best_live = live_by_id.get(3500)
        elif "سشوار" in norm_desc and "پروامگا" in norm_desc and "2200" in norm_desc:
            best_live = live_by_id.get(3049)
        elif "سشوار" in norm_desc and "امگا" in norm_desc and "2000" in norm_desc:
            best_live = live_by_id.get(3285)
        elif "سانی" in norm_desc and "2600" in norm_desc:
            best_live = live_by_id.get(3540)
        elif "پاکشوما" in norm_desc and "دوتیکه" in norm_desc and "18هزار" in norm_desc:
            best_live = live_by_id.get(3266)
        elif "کولر" in norm_desc and "ریتون" in norm_desc and "آبی" in norm_desc:
            best_live = live_by_id.get(2538)
        elif "التون" in norm_desc and "s517" in norm_desc:
            best_live = live_by_id.get(3383)
        elif "التون" in norm_desc and ("md5s" in norm_desc or "mds" in norm_desc):
            best_live = live_by_id.get(3380)
        elif "گوشت کوب" in norm_desc and "دونالکس" in norm_desc and "275" in norm_desc:
            best_live = live_by_id.get(3032)
        elif "گوشت کوب" in norm_desc and "دونالکس" in norm_desc and "290" in norm_desc:
            best_live = live_by_id.get(3626)
        elif "مخلوط کن" in norm_desc and "دونالکس" in norm_desc and "205" in norm_desc:
            best_live = live_by_id.get(3035)
        elif "همزن" in norm_desc and "دونالکس" in norm_desc and "355" in norm_desc:
            best_live = live_by_id.get(3622)
        elif "غذاساز" in norm_desc and "فیلیپس" in norm_desc and "7778" in norm_desc:
            best_live = live_by_id.get(3629)
        elif "ساندویچ ساز" in norm_desc and "دونالکس" in norm_desc and "940" in norm_desc:
            best_live = live_by_id.get(3617)
        elif "کتری" in norm_desc and "وگاتی" in norm_desc and "توپی" in norm_desc:
            best_live = live_by_id.get(3668)
        elif "هرمی" in norm_desc and "604" in norm_desc:
            best_live = live_by_id.get(3662)
        elif "زودپز" in norm_desc and "اویزپلاس" in norm_desc and "تکی" in norm_desc:
            best_live = live_by_id.get(3602)
        elif "زودپز" in norm_desc and "اویزپلاس" in norm_desc and "دوقلو" in norm_desc:
            best_live = live_by_id.get(3606)
        elif "شیرجوش" in norm_desc and "اویزپلاس" in norm_desc:
            best_live = live_by_id.get(3612)
        elif "سرویس قابلمه" in norm_desc and "اویزپلاس" in norm_desc and "12پ" in norm_desc:
            best_live = live_by_id.get(3610)
        elif "سرویس قابلمه" in norm_desc and "اویزپلاس" in norm_desc and "24پ" in norm_desc:
            best_live = live_by_id.get(3608)
        elif "سرویس قابلمه" in norm_desc and "اویزپلاس" in norm_desc and "ویولا" in norm_desc:
            best_live = live_by_id.get(3318)
        elif "سرویس قابلمه" in norm_desc and "اویز" in norm_desc and "10پ" in norm_desc:
            best_live = live_by_id.get(3592)
        elif "پاکیزان" in norm_desc and "40کیلو" in norm_desc:
            best_live = live_by_id.get(3709)
        elif "پاکشوما" in norm_desc and "21کیلو" in norm_desc:
            best_live = live_by_id.get(3707)
        elif "پاکشوما" in norm_desc and "15ک" in norm_desc:
            best_live = live_by_id.get(3563)
        elif "ریتون" in norm_desc and "17دوقلو" in norm_desc:
            best_live = live_by_id.get(3551)
        elif "کلور" in norm_desc and "10کیلو" in norm_desc and "کرم" in norm_desc:
            best_live = live_by_id.get(3573)
        elif "کلور" in norm_desc and "8کیلو" in norm_desc and "اینوکس" in norm_desc:
            best_live = live_by_id.get(2510)
        elif "کلور" in norm_desc and "9tw1" in norm_desc:
            best_live = live_by_id.get(2505)
        elif "ظرفشویی" in norm_desc and "15نفره" in norm_desc:
            best_live = live_by_id.get(2871)
        elif "ظرفشویی" in norm_desc and "16نفره" in norm_desc:
            best_live = live_by_id.get(3546)
        elif "دیپونت" in norm_desc and "boos" in norm_desc:
            best_live = live_by_id.get(2594)
        elif "بست" in norm_desc and "یخچال" in norm_desc:
            best_live = live_by_id.get(3389)
        elif "الکترواستیل" in norm_desc and ("فیوچر" in norm_desc or "21فوت" in norm_desc):
            best_live = live_by_id.get(3453)
        elif "الکتروسان" in norm_desc and ("صندوقی" in norm_desc or "345" in norm_desc or "280" in norm_desc):
            best_live = live_by_id.get(3513)
        elif "کلور" in norm_desc and "70" in norm_desc and "گلوری" in norm_desc and "دوقلو" in norm_desc:
            best_live = live_by_id.get(2497)
        elif "کلور" in norm_desc and "70" in norm_desc and "روسو" in norm_desc and "کمبی" in norm_desc:
            best_live = live_by_id.get(2484)
        elif "کلور" in norm_desc and "101" in norm_desc and ("27" in norm_desc or "کمبی" in norm_desc):
            best_live = live_by_id.get(2408)
        elif "کلور" in norm_desc and "54" in norm_desc and "گلوری" in norm_desc:
            best_live = live_by_id.get(2972)
        elif "زامروتی" in norm_desc and "مخلوط کن" in norm_desc:
            best_live = live_by_id.get(3655)
        elif "زامروتی" in norm_desc and "کتری" in norm_desc:
            best_live = live_by_id.get(3660)

        if best_live:
            match_info["match_type"] = "EXACT_SITE_PRODUCT"
            match_info["site_status"] = "ثبت‌شده در سایت"
            match_info["product_id"] = best_live['id']
            match_info["price_regular"] = best_live.get('price_regular')
            match_info["price_sale"] = best_live.get('price_sale')
            match_info["link"] = best_live.get('permalink') or f"https://hosseinykala.ir/?p={best_live['id']}"
            match_info["sku"] = best_live.get('sku', '')
            stats["matched_site_parent"] += 1
            matched_results.append(match_info)
            continue

        # ۵. تطبیق با اقلام آفلاین قبلی کاتالوگ اکسل (Old Offline)
        best_old_offline = None
        for old in old_excel_items:
            if old.get('status_note') == 'در سایت تعریف نشده' or not old.get('product_id'):
                old_name_norm = normalize_text(old['name'])
                if norm_model and norm_model in old_name_norm:
                    best_old_offline = old
                    break
                elif normalize_text(raw_desc) in old_name_norm or old_name_norm in normalize_text(raw_desc):
                    best_old_offline = old
                    break

        if best_old_offline:
            match_info["match_type"] = "EXISTING_OFFLINE_CATALOG"
            match_info["site_status"] = "در سایت تعریف نشده"
            match_info["category"] = best_old_offline.get('main_cat') or cat
            match_info["subcategory"] = best_old_offline.get('subcat') or brand
            match_info["brand"] = best_old_offline.get('brand') or brand
            stats["matched_old_offline"] += 1
            matched_results.append(match_info)
            continue

        # ۶. کالای کاملاً جدید (New Offline Item)
        match_info["match_type"] = "NEW_OFFLINE_ITEM"
        match_info["site_status"] = "در سایت تعریف نشده"
        stats["new_offline_items"] += 1
        matched_results.append(match_info)

    print(f"\nنتایج ممیزی و تطبیق:")
    print(f"- کل اقلام ورودی: {stats['total_incoming']}")
    print(f"- تطبیق با محصولات والد سایت: {stats['matched_site_parent']}")
    print(f"- تطبیق با تنوع‌های سایت: {stats['matched_site_variation']}")
    print(f"- تطبیق با اقلام آفلاین قبلی اکسل: {stats['matched_old_offline']}")
    print(f"- اقلام کاملاً جدید (New Items): {stats['new_offline_items']}")
    print(f"- ردیف‌های حسابداری (کسرواضافات): {stats['accounting_rows']}")
    print(f"- مجموع اقلام موجود: {stats['in_stock_count']}")
    print(f"- مجموع اقلام ناموجود: {stats['out_of_stock_count']}")

    with open(OUT_MATCHED_FILE, 'w', encoding='utf-8') as f:
        json.dump(matched_results, f, ensure_ascii=False, indent=2)
    print(f"نتایج تطبیق در: {OUT_MATCHED_FILE}")

    # ذخیره پایگاه داده نگاشت استاندارد
    mapping_standard = {}
    for r in matched_results:
        key = r['standard_key']
        mapping_standard[key] = {
            "standard_key": key,
            "standard_name": r['standard_name'],
            "brand": r['brand'],
            "model_code": r['model_code'],
            "category": r['category'],
            "subcategory": r['subcategory'],
            "site_status": r['site_status'],
            "product_id": r['product_id'],
            "variation_id": r['variation_id'],
            "sample_raw_desc": r['raw_desc']
        }
    with open(MAPPING_STANDARD_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping_standard, f, ensure_ascii=False, indent=2)
    print(f"پایگاه نگاشت استاندارد در: {MAPPING_STANDARD_FILE}")

    return matched_results, stats

if __name__ == '__main__':
    run_matching_and_auditing()
