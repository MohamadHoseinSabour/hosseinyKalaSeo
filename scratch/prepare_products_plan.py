import os
import sys
import json
import re
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)
category_sheets = [
    'یخچال و فریزر',
    'شستشو و نظافت',
    'لوازم برقی و پخت و پز',
    'نوشیدنی ساز',
    'سرمایش و گرمایش',
    'تصفیه کننده آب',
    'صوتی و تصویری',
    'زیبایی و سلامت فردی'
]

# Category ID mapping based on WordPress categories
# Main and subcategory IDs from data/categories.json
CAT_IDS = {
    'یخچال و فریزر': {
        'default': 92,
        'کلور': [92, 153],
        'دیپوینت': [92, 154],
        'ایستکول': [92, 155],
        'الکترواستیل': [92, 156],
        'هیمالیا': [92],
        'نیکسان': [92],
        'تکنوسان': [92],
    },
    'شستشو و نظافت': {
        'default': 239,
        'جاروبرقی': 21,
        'ماشین لباسشویی': 93,
        'ماشین ظرفشویی': 97,
        'اتو': 118,
    },
    'لوازم برقی و پخت و پز': {
        'default': 216,
        'سرخ کن': 121,
        'گوشت کوب برقی': 122,
        'اجاق گاز': 209,
        'گاز صفحه ای': 210,
        'فر': 216,
        'هود': 216,
        'ظروف و پخت و پز': 215,
        'پلوپز': 216,
        'خردکن': 216,
    },
    'نوشیدنی ساز': {
        'default': 240,
        'اسپرسو ساز': 119,
        'آبمیوه گیری': 120,
        'مخلوط کن': 123,
        'چای ساز': 211,
        'کتری برقی': 240,
        'آسیاب برقی': 240,
        'همزن برقی': 240,
    },
    'سرمایش و گرمایش': {
        'default': 241,
        'کولر آبی': 95,
        'کولر گازی': 206,
        'پنکه و گرمایشی': 214,
        'بخاری': 214,
        'پنکه': 214,
        'آبگرمکن': 241,
    },
    'زیبایی و سلامت فردی': {
        'default': 212,
        'سشوار': 124,
        'اصلاح موی سر و صورت': 126,
        'اتو مو': 212,
        'فر کننده مو': 212,
    }
}

# Canonical category URLs from data/categories.json
CAT_CANONICAL_URLS = {
    92: "https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/",
    153: "https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/clover-refrigerators/",
    154: "https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/depoint-refrigerators/",
    155: "https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/eastcool-refrigerators/",
    156: "https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/electrosteel-refrigerators/",
    239: "https://hosseinykala.ir/product-category/washing-cleaning/",
    21: "https://hosseinykala.ir/product-category/washing-cleaning/%d8%ac%d8%a7%d8%b1%d9%88%d8%a8%d8%b1%d9%82%db%8c/",
    93: "https://hosseinykala.ir/product-category/washing-cleaning/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d9%84%d8%a8%d8%a7%d8%b3%d8%b4%d9%88%db%8c%db%8c/",
    157: "https://hosseinykala.ir/product-category/washing-cleaning/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d9%84%d8%a8%d8%a7%d8%b3%d8%b4%d9%88%db%8c%db%8c/clover-washing-machines/",
    97: "https://hosseinykala.ir/product-category/washing-cleaning/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d8%b8%d8%b1%d9%81%d8%b4%d9%88%db%8c%db%8c/",
    118: "https://hosseinykala.ir/product-category/washing-cleaning/%d8%a7%d8%aa%d9%88/",
    216: "https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/",
    121: "https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/%d8%b3%d8%b1%d8%ae-%da%a9%d9%86/",
    122: "https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/%da%af%d9%88%d8%b4%d8%aa-%da%a9%d9%88%d8%a8-%d8%a8%d8%b1%d9%82%db%8c/",
    209: "https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/%d8%a7%d8%ac%d8%a7%d9%82-%da%af%d8%a7%d8%b2/",
    210: "https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/%d8%a7%d8%ac%d8%a7%d9%82-%da%af%d8%a7%d8%b2/%da%af%d8%a7%d8%b2-%d8%b5%d9%81%d8%ad%d9%87-%d8%a7%db%8c/",
    215: "https://hosseinykala.ir/product-category/%d9%84%d9%88%d8%a7%d8%b2%d9%85-%d8%a8%d8%b1%d9%82%db%8c-%d8%a2%d8%b4%d9%be%d8%b2%d8%ae%d8%a7%d9%86%d9%87/%d8%b8%d8%b1%d9%88%d9%81-%d9%88-%d9%be%d8%ae%d8%aa-%d9%88-%d9%be%d8%b2/",
    240: "https://hosseinykala.ir/product-category/drink-makers/",
    119: "https://hosseinykala.ir/product-category/drink-makers/%d8%a7%d8%b3%d9%be%d8%b1%d8%b3%d9%88-%d8%b3%d8%a7%d8%b2/",
    120: "https://hosseinykala.ir/product-category/drink-makers/%d8%a2%d8%a8%d9%85%db%8c%d9%88%d9%87-%da%af%db%8c%d8%b1%db%8c/",
    123: "https://hosseinykala.ir/product-category/drink-makers/%d9%85%d8%ae%d9%84%d9%88%d8%b7-%da%a9%d9%86/",
    211: "https://hosseinykala.ir/product-category/drink-makers/%da%86%d8%a7%db%8c-%d8%b3%d8%a7%d8%b2/",
    241: "https://hosseinykala.ir/product-category/heating-cooling/",
    95: "https://hosseinykala.ir/product-category/heating-cooling/%da%a9%d9%88%d9%84%d8%b1-%d8%a2%d8%a8%db%8c/",
    206: "https://hosseinykala.ir/product-category/heating-cooling/%da%a9%d9%88%d9%84%d8%b1-%da%af%d8%a7%d8%b2%db%8c/",
    214: "https://hosseinykala.ir/product-category/heating-cooling/%d8%b5%d9%88%d8%aa%db%8c%d8%8c-%d8%aa%d8%b5%d9%88%db%8c%d8%b1%db%8c-%d9%88-%da%af%d8%b1%d9%85%d8%a7%db%8c%d8%b4%db%8c/",
    212: "https://hosseinykala.ir/product-category/%d8%a7%d8%b5%d9%84%d8%a7%d8%ad-%d9%88-%d8%b2%db%8c%d8%a8%d8%a7%db%8c%db%8c/",
    124: "https://hosseinykala.ir/product-category/%d8%a7%d8%b5%d9%84%d8%a7%d8%ad-%d9%88-%d8%b2%db%8c%d8%a8%d8%a7%db%8c%db%8c/%d8%b3%d8%b4%d9%88%d8%a7%d8%b1/",
    126: "https://hosseinykala.ir/product-category/%d8%a7%d8%b5%d9%84%d8%a7%d8%ad-%d9%88-%d8%b2%db%8c%d8%a8%d8%a7%db%8c%db%8c/%d8%a5%d8%b5%d9%84%d8%a7%d8%ad-%d9%85%d9%88%db%8c-%d8%b3%d8%b1/",
    96: "https://hosseinykala.ir/product-category/%d8%aa%d8%b5%d9%81%db%8c%d9%87-%da%a9%d9%86%d9%86%d8%af%d9%87-%d8%a2%d8%a8/"
}

# Determine categories for product
def get_product_cats(sheet, subcat, brand, name):
    cats = []
    if sheet == 'یخچال و فریزر':
        cats.append(92)
        if 'کلور' in brand or 'کلور' in name:
            cats.append(153)
        elif 'دیپوینت' in brand or 'دیپوینت' in name:
            cats.append(154)
        elif 'ایستکول' in brand or 'ایستکول' in name:
            cats.append(155)
        elif 'الکترواستیل' in brand or 'الکترواستیل' in name:
            cats.append(156)
    elif sheet == 'شستشو و نظافت':
        cats.append(239)
        if 'جاروبرقی' in name or 'جاروبرقی' in subcat:
            cats.append(21)
        elif 'لباسشویی' in name or 'پتوشور' in name or 'مینی واش' in name or 'لباسشویی' in subcat:
            cats.append(93)
            if 'کلور' in brand or 'کلور' in name:
                cats.append(157)
        elif 'ظرفشویی' in name or 'ظرفشویی' in subcat:
            cats.append(97)
        elif 'اتو' in name or 'اتو' in subcat:
            cats.append(118)
    elif sheet == 'لوازم برقی و پخت و پز':
        cats.append(216)
        if 'سرخ کن' in name or 'هواپز' in name or 'سرخ کن' in subcat:
            cats.append(121)
        elif 'گوشت کوب' in name or 'گوشت کوب' in subcat:
            cats.append(122)
        elif 'گاز صفحه ای' in name:
            cats.append(209)
            cats.append(210)
        elif 'فر' in name:
            cats.append(216)
        elif 'قابلمه' in name or 'تابه' in name:
            cats.append(215)
    elif sheet == 'نوشیدنی ساز':
        cats.append(240)
        if 'اسپرسو' in name or 'اسپرسو' in subcat:
            cats.append(119)
        elif 'آبمیوه گیری' in name or 'آبمیوه گیری' in subcat:
            cats.append(120)
        elif 'مخلوط کن' in name or 'مخلوط کن' in subcat:
            cats.append(123)
        elif 'چای ساز' in name or 'چای ساز' in subcat:
            cats.append(211)
    elif sheet == 'سرمایش و گرمایش':
        cats.append(241)
        if 'کولر آبی' in name:
            cats.append(95)
        elif 'کولر' in name and 'گازی' in name:
            cats.append(206)
        elif 'بخاری' in name or 'پنکه' in name:
            cats.append(214)
    elif sheet == 'زیبایی و سلامت فردی':
        cats.append(212)
        if 'سشوار' in name or 'سشوار' in subcat:
            cats.append(124)
        elif 'ریش تراش' in name or 'پیرایش' in name or 'اصلاح' in name:
            cats.append(126)
            
    if not cats:
        cats = [239]
    return cats

# Get primary canonical category URL for internal linking
def get_primary_cat_url(cat_ids):
    # Prefer most specific category
    for cid in reversed(cat_ids):
        if cid in CAT_CANONICAL_URLS:
            return cid, CAT_CANONICAL_URLS[cid]
    return 239, "https://hosseinykala.ir/product-category/washing-cleaning/"

print("Script template ready.")
