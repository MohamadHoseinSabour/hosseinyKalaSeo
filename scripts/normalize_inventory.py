"""
scripts/normalize_inventory.py
==============================
اسکریپت تخصصی نرمال‌سازی ۲۳۸ قلم موجودی انبار حسینی کالا:
۱. پاکسازی خط‌فاصله‌ها و کاراکترهای نامناسب
۲. استخراج دقیق کد مدل
۳. تشخیص برند معتبر کالا
۴. تخصیص یکی از ۸ دسته‌بندی اصلی سایت
۵. تولید عنوان تمیز، استاندارد و تجاری فارسی
۶. ذخیره در data/inventory_normalized.json
"""

import os
import sys
import json
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"
INPUT_JSON = os.path.join(PROJECT_DIR, 'data', 'inventory_parsed.json')
OUTPUT_JSON = os.path.join(PROJECT_DIR, 'data', 'inventory_normalized.json')

# نگاشت جامع و دقیق ۲۳۸ قلم ورودی بر اساس تحلیل تک‌تک اقلام
ITEMS_METADATA = {
    1: {"brand": "هاورسن", "model_code": "75aversen", "category": "صوتی و تصویری", "standard_name": "تلویزیون ال ای دی هوشمند 75 اینچ هاورسن مدل 75aversen"},
    2: {"brand": "کلور", "model_code": "8vw1", "category": "شستشو و نظافت", "standard_name": "ماشین لباسشویی 8 کیلویی کلور مدل 8vw1 سفید"},
    3: {"brand": "افترون", "model_code": "AFWD-5700", "category": "تصفیه کننده آب", "standard_name": "آبسردکن رومیزی افترون مدل AFWD-5700"},
    4: {"brand": "نیکائی", "model_code": "1206", "category": "تصفیه کننده آب", "standard_name": "آبسردکن ایستاده نیکائی مدل 1206"},
    5: {"brand": "الکترواستیل", "model_code": "مخزندار دیواری", "category": "تصفیه کننده آب", "standard_name": "آبگرمکن مخزن دار دیواری الکترواستیل"},
    6: {"brand": "بوتان", "model_code": "B3115", "category": "تصفیه کننده آب", "standard_name": "آبگرمکن دیواری بوتان مدل B3115"},
    7: {"brand": "جنرال", "model_code": "607", "category": "نوشیدنی ساز", "standard_name": "آبمیوه گیری و غذاساز جنرال مدل 607"},
    8: {"brand": "کاستلو", "model_code": "470", "category": "نوشیدنی ساز", "standard_name": "آسیاب برقی کاستلو مدل 470"},
    9: {"brand": "دونالکس", "model_code": "120", "category": "نوشیدنی ساز", "standard_name": "آبمیوه گیری تک کاره دونالکس مدل DN-120"},
    10: {"brand": "دونالکس", "model_code": "110", "category": "نوشیدنی ساز", "standard_name": "آبمیوه گیری 4 کاره دونالکس مدل DN-110"},
    11: {"brand": "پرومارون", "model_code": "614", "category": "زیبایی و سلامت فردی", "standard_name": "اپیلیدی 5 کاره پرومارون مدل RL-614"},
    12: {"brand": "دونالکس", "model_code": "815", "category": "شستشو و نظافت", "standard_name": "اتو بخار دستی دونالکس مدل DN-815"},
    13: {"brand": "فیلیپس", "model_code": "5040", "category": "شستشو و نظافت", "standard_name": "اتو بخار دستی فیلیپس مدل DST5040"},
    14: {"brand": "بابیلیس", "model_code": "baby3383a", "category": "زیبایی و سلامت فردی", "standard_name": "اتو مو بابیلیس مدل baby3383a"},
    15: {"brand": "پاناسونیک", "model_code": "HV11", "category": "زیبایی و سلامت فردی", "standard_name": "اتو مو پاناسونیک مدل HV11"},
    16: {"brand": "ساپر", "model_code": "4025", "category": "شستشو و نظافت", "standard_name": "اتو بخار ساپر مدل 4025 کف سرامیک"},
    17: {"brand": "ساپر", "model_code": "4035", "category": "شستشو و نظافت", "standard_name": "اتو بخار ساپر مدل 4035 کف سرامیک"},
    18: {"brand": "رانکو", "model_code": "رانکو", "category": "شستشو و نظافت", "standard_name": "اتو بخار دستی رانکو"},
    19: {"brand": "سیماران", "model_code": "8002", "category": "شستشو و نظافت", "standard_name": "اتو بخار سیماران مدل 8002 زرد"},
    20: {"brand": "دوو", "model_code": "990c", "category": "شستشو و نظافت", "standard_name": "ماشین لباسشویی اتوماتیک دوو 9 کیلویی سینیور مدل 990c سفید"},
    21: {"brand": "دوو", "model_code": "990S", "category": "شستشو و نظافت", "standard_name": "ماشین لباسشویی اتوماتیک دوو 9 کیلویی سینیور مدل 990S"},
    22: {"brand": "پرومارون", "model_code": "1115", "category": "زیبایی و سلامت فردی", "standard_name": "اتو مو کراتینه پرومارون مدل 1115"},
    23: {"brand": "پرومارون", "model_code": "1116", "category": "زیبایی و سلامت فردی", "standard_name": "اتو مو پرومارون مدل 1116"},
    24: {"brand": "مونزا", "model_code": "VR3000W", "category": "شستشو و نظافت", "standard_name": "اتو بخار مخزن دار مونزا مدل VR3000W"},
    25: {"brand": "دونالکس", "model_code": "480", "category": "نوشیدنی ساز", "standard_name": "اسپرسوساز دونالکس مدل DN-480"},
    26: {"brand": "دونالکس", "model_code": "475", "category": "نوشیدنی ساز", "standard_name": "اسپرسوساز دونالکس مدل DN-475"},
    27: {"brand": "رانکو", "model_code": "حرفه ای", "category": "نوشیدنی ساز", "standard_name": "اسپرسوساز حرفه ای رانکو"},
    28: {"brand": "گرنویک", "model_code": "رترو نارنجی", "category": "نوشیدنی ساز", "standard_name": "اسپرسوساز گرنویک مدل رترو نارنجی"},
    29: {"brand": "ونتو", "model_code": "ونتو", "category": "نوشیدنی ساز", "standard_name": "آسیاب برقی ونتو"},
    30: {"brand": "کلور", "model_code": "اکونومی 27 فوت", "category": "یخچال و فریزر", "standard_name": "فریزر تک 27 فوت کلور مدل اکونومی استیل"},
    31: {"brand": "کلور", "model_code": "روسو اکونومی", "category": "یخچال و فریزر", "standard_name": "فریزر تک کلور مدل روسو استیل اکونومی"},
    32: {"brand": "کلور", "model_code": "اکونومی 27 فوت", "category": "یخچال و فریزر", "standard_name": "فریزر تک 27 فوت کلور مدل اکونومی سفید"},
    33: {"brand": "هاورسن", "model_code": "32aversen", "category": "صوتی و تصویری", "standard_name": "تلویزیون ال ای دی 32 اینچ هاورسن مدل HD (32aversen)"},
    34: {"brand": "هاورسن", "model_code": "85aversen", "category": "صوتی و تصویری", "standard_name": "تلویزیون ال ای دی 85 اینچ هوشمند 4K اسمارت هاورسن مدل Ultra HD (85aversen)"},
    35: {"brand": "کلور", "model_code": "اکونومی 27 فوت", "category": "یخچال و فریزر", "standard_name": "یخچال تک 27 فوت کلور مدل اکونومی سفید"},
    36: {"brand": "کلور", "model_code": "اکونومی 27 فوت", "category": "یخچال و فریزر", "standard_name": "یخچال تک 27 فوت کلور مدل اکونومی استیل"},
    37: {"brand": "کلور", "model_code": "روسو اکونومی", "category": "یخچال و فریزر", "standard_name": "یخچال تک کلور مدل روسو استیل اکونومی"},
    38: {"brand": "گلدن لوکس", "model_code": "گلدن لوکس", "category": "سرمایش و گرمایش", "standard_name": "بخاری گازی گلدن لوکس"},
    39: {"brand": "پارس خزر", "model_code": "FH-2000P", "category": "سرمایش و گرمایش", "standard_name": "بخاری برقی فن دار پارس خزر مدل FH-2000P"},
    40: {"brand": "پلار", "model_code": "3pn-new", "category": "سرمایش و گرمایش", "standard_name": "بخاری پلار مدل 3pn-new طرح ماشینی"},
    41: {"brand": "پاکیزان", "model_code": "30 کیلو", "category": "شستشو و نظافت", "standard_name": "پتوشور 30 کیلویی پاکیزان"},
    42: {"brand": "پاکیزان", "model_code": "40 کیلو", "category": "شستشو و نظافت", "standard_name": "پتوشور 40 کیلویی پاکیزان"},
    43: {"brand": "پرومارون", "model_code": "1113", "category": "زیبایی و سلامت فردی", "standard_name": "برس حرارتی پرومارون مدل 1113"},
    44: {"brand": "پارس خزر", "model_code": "361", "category": "لوازم برقی و پخت و پز", "standard_name": "پلوپز پارس خزر مدل 361"},
    45: {"brand": "الکترا", "model_code": "پایه بلند", "category": "سرمایش و گرمایش", "standard_name": "پنکه پایه بلند الکترا"},
    46: {"brand": "پارس خزر", "model_code": "پایه بلند", "category": "سرمایش و گرمایش", "standard_name": "پنکه پایه بلند پارس خزر"},
    47: {"brand": "پاناسونیک", "model_code": "2 حالته", "category": "سرمایش و گرمایش", "standard_name": "پنکه دو حالته پاناسونیک"},
    48: {"brand": "سانی", "model_code": "2600", "category": "سرمایش و گرمایش", "standard_name": "پنکه ایستاده ریموت دار سانی مدل DWS-2600"},
    49: {"brand": "اویز", "model_code": "سایز 28", "category": "لوازم برقی و پخت و پز", "standard_name": "تابه گرانیتی درب دار اویز سایز 28"},
    50: {"brand": "اویز", "model_code": "سایز 30 مشکی", "category": "لوازم برقی و پخت و پز", "standard_name": "تابه گرانیتی اویز سایز 30 مشکی"},
    51: {"brand": "اویز", "model_code": "سایز 22 مشکی", "category": "لوازم برقی و پخت و پز", "standard_name": "تابه گرانیتی اویز سایز 22 مشکی"},
    52: {"brand": "اویز", "model_code": "سایز 32 فوج مشکی", "category": "لوازم برقی و پخت و پز", "standard_name": "تابه گرانیتی درب دار اویز مدل فوج مشکی سایز 32"},
    53: {"brand": "اویز", "model_code": "سایز 24", "category": "لوازم برقی و پخت و پز", "standard_name": "تابه گرانیتی اویز سایز 24"},
    54: {"brand": "اویز", "model_code": "سایز 24 مشکی", "category": "لوازم برقی و پخت و پز", "standard_name": "تابه گرانیتی اویز سایز 24 مشکی"},
    55: {"brand": "اویز", "model_code": "سایز 26", "category": "لوازم برقی و پخت و پز", "standard_name": "تابه گرانیتی اویز سایز 26"},
    56: {"brand": "سافت واتر", "model_code": "6 مرحله", "category": "تصفیه کننده آب", "standard_name": "دستگاه تصفیه آب 6 مرحله ای سافت واتر مدل IR-06"},
    57: {"brand": "وست واتر", "model_code": "وست واتر", "category": "تصفیه کننده آب", "standard_name": "دستگاه تصفیه آب خانگی وست واتر"},
    58: {"brand": "هوم گلد", "model_code": "هوم گلد", "category": "تصفیه کننده آب", "standard_name": "دستگاه تصفیه آب خانگی 6 مرحله ای هوم گلد مدل RO"},
    59: {"brand": "سی سی کا", "model_code": "c.c.k", "category": "تصفیه کننده آب", "standard_name": "دستگاه تصفیه آب خانگی سی سی کا مدل c.c.k"},
    60: {"brand": "متفرقه", "model_code": "60 لیتر", "category": "لوازم برقی و پخت و پز", "standard_name": "آون توستر 60 لیتری"},
    61: {"brand": "دلمونتی", "model_code": "580", "category": "لوازم برقی و پخت و پز", "standard_name": "توستر نان دلمونتی مدل DL-580"},
    62: {"brand": "وستینگهاوس", "model_code": "آبی", "category": "لوازم برقی و پخت و پز", "standard_name": "توستر نان رترو وستینگهاوس رنگ آبی"},
    63: {"brand": "وستینگهاوس", "model_code": "کرم", "category": "لوازم برقی و پخت و پز", "standard_name": "توستر نان رترو وستینگهاوس رنگ کرم"},
    64: {"brand": "پاندا", "model_code": "80 لیتر آب و خاک", "category": "شستشو و نظافت", "standard_name": "جاروبرقی صنعتی آب و خاک 80 لیتری پاندا"},
    65: {"brand": "آراز", "model_code": "40 لیتر", "category": "شستشو و نظافت", "standard_name": "جاروبرقی سطلی 40 لیتری آراز"},
    66: {"brand": "سران", "model_code": "21 لیتر آب و خاک", "category": "شستشو و نظافت", "standard_name": "جاروبرقی سطلی سران 21 لیتری آب و خاک"},
    67: {"brand": "سران", "model_code": "21 لیتر آب و خاک زرد", "category": "شستشو و نظافت", "standard_name": "جاروبرقی سطلی سران 21 لیتری آب و خاک زرد"},
    68: {"brand": "سران", "model_code": "21 لیتر زرد", "category": "شستشو و نظافت", "standard_name": "جاروبرقی سطلی سران 21 لیتری زرد"},
    69: {"brand": "سران", "model_code": "21 لیتر مشکی", "category": "شستشو و نظافت", "standard_name": "جاروبرقی سطلی سران 21 لیتری مشکی"},
    70: {"brand": "هیتاچی", "model_code": "1200", "category": "شستشو و نظافت", "standard_name": "جاروبرقی سطلی هیتاچی مدل 1200"},
    71: {"brand": "دونالکس", "model_code": "750", "category": "شستشو و نظافت", "standard_name": "جاروبرقی کیسه ای دونالکس مدل DN-750 سرمه ای"},
    72: {"brand": "دونالکس", "model_code": "750", "category": "شستشو و نظافت", "standard_name": "جاروبرقی کیسه ای دونالکس مدل DN-750 طلایی"},
    73: {"brand": "کلور", "model_code": "سطلی", "category": "شستشو و نظافت", "standard_name": "جاروبرقی سطلی کلور"},
    74: {"brand": "بست", "model_code": "BOST", "category": "شستشو و نظافت", "standard_name": "جاروبرقی سطلی بست مدل BOST"},
    75: {"brand": "دونالکس", "model_code": "185", "category": "نوشیدنی ساز", "standard_name": "چای ساز دونالکس مدل DN-185 مشکی"},
    76: {"brand": "گرنویک", "model_code": "سماوری", "category": "نوشیدنی ساز", "standard_name": "چای ساز سماوری گرنویک"},
    77: {"brand": "کورکماز", "model_code": "A331", "category": "نوشیدنی ساز", "standard_name": "چای ساز کورکماز مدل A331"},
    78: {"brand": "ویلز", "model_code": "2015", "category": "نوشیدنی ساز", "standard_name": "چای ساز روهمی ویلز مدل 2015"},
    79: {"brand": "ویلز", "model_code": "ویلز", "category": "لوازم برقی و پخت و پز", "standard_name": "چرخ گوشت قدرتمند ویلز"},
    80: {"brand": "ویلز", "model_code": "6031", "category": "لوازم برقی و پخت و پز", "standard_name": "خردکن کاسه استیل ویلز مدل 6031"},
    81: {"brand": "ویلز", "model_code": "6032", "category": "لوازم برقی و پخت و پز", "standard_name": "خردکن 3 لیتری ویلز مدل 6032"},
    82: {"brand": "پرومارون", "model_code": "731", "category": "زیبایی و سلامت فردی", "standard_name": "دستگاه پیرایش سیمی سر و صورت پرومارون مدل RL-731"},
    83: {"brand": "پرومارون", "model_code": "706", "category": "زیبایی و سلامت فردی", "standard_name": "ماشین ریش تراش چرخشی پرومارون مدل RL-706"},
    84: {"brand": "اویز پلاس", "model_code": "تکی مشکی رزگلد", "category": "لوازم برقی و پخت و پز", "standard_name": "زودپز تک دسته اویز پلاس مشکی رزگلد"},
    85: {"brand": "اویز پلاس", "model_code": "دوقلو مشکی رزگلد", "category": "لوازم برقی و پخت و پز", "standard_name": "زودپز دوقلو اویز پلاس مشکی رزگلد"},
    86: {"brand": "متفرقه", "model_code": "ساندویچ ساز", "category": "لوازم برقی و پخت و پز", "standard_name": "ساندویچ ساز برقی خانگی"},
    87: {"brand": "دونالکس", "model_code": "940", "category": "لوازم برقی و پخت و پز", "standard_name": "ساندویچ ساز دونالکس مدل DN-940 سفید"},
    88: {"brand": "دونالکس", "model_code": "940", "category": "لوازم برقی و پخت و پز", "standard_name": "ساندویچ ساز دونالکس مدل DN-940 مشکی"},
    89: {"brand": "کنرا", "model_code": "KENRA", "category": "لوازم برقی و پخت و پز", "standard_name": "سبزی خردکن برقی کنرا مدل KENRA"},
    90: {"brand": "نیاک", "model_code": "3 کیلو", "category": "لوازم برقی و پخت و پز", "standard_name": "سبزی خردکن خانگی 3 کیلویی نیاک"},
    91: {"brand": "دونالکس", "model_code": "بدون روغن", "category": "لوازم برقی و پخت و پز", "standard_name": "سرخ کن بدون روغن دونالکس"},
    92: {"brand": "گرنویک", "model_code": "خاکستری", "category": "لوازم برقی و پخت و پز", "standard_name": "سرخ کن بدون روغن (ایرفرایر) گرنویک مدل ProMar خاکستری"},
    93: {"brand": "دونالکس", "model_code": "970", "category": "لوازم برقی و پخت و پز", "standard_name": "سرخ کن بدون روغن دونالکس مدل DN-970 استیل"},
    94: {"brand": "ویلز", "model_code": "5062", "category": "لوازم برقی و پخت و پز", "standard_name": "سرخ کن بدون روغن ویلز مدل 5062"},
    95: {"brand": "اویز", "model_code": "10 پارچه سرمه ای", "category": "لوازم برقی و پخت و پز", "standard_name": "سرویس قابلمه 10 پارچه گرانیتی اویز سرمه ای"},
    96: {"brand": "اویز پلاس", "model_code": "10 پارچه اناری", "category": "لوازم برقی و پخت و پز", "standard_name": "سرویس قابلمه 10 پارچه گرانیتی اویز پلاس رنگ اناری"},
    97: {"brand": "اویز پلاس", "model_code": "12 پارچه مشکی", "category": "لوازم برقی و پخت و پز", "standard_name": "سرویس قابلمه 12 پارچه گرانیتی اویز پلاس مشکی"},
    98: {"brand": "اویز پلاس", "model_code": "24 پارچه سبز", "category": "لوازم برقی و پخت و پز", "standard_name": "سرویس قابلمه 24 پارچه گرانیتی اویز پلاس سبز"},
    99: {"brand": "اویز پلاس", "model_code": "ویولا 11 پارچه", "category": "لوازم برقی و پخت و پز", "standard_name": "سرویس قابلمه 11 پارچه اویز پلاس مدل ویولا"},
    100: {"brand": "پرو امگا", "model_code": "2000 وات", "category": "زیبایی و سلامت فردی", "standard_name": "سشوار حرفه ای پرو امگا 2000 وات"},
    101: {"brand": "پرو امگا", "model_code": "2200 وات", "category": "زیبایی و سلامت فردی", "standard_name": "سشوار حرفه ای موتور سنگین پرو امگا 2200 وات"},
    102: {"brand": "اویز پلاس", "model_code": "السا 11 پارچه سبز", "category": "لوازم برقی و پخت و پز", "standard_name": "سرویس قابلمه 11 پارچه گرانیتی اویز پلاس مدل السا سبز"},
    103: {"brand": "اویز پلاس", "model_code": "مشکی", "category": "لوازم برقی و پخت و پز", "standard_name": "شیرجوش گرانیتی اویز پلاس مشکی"},
    104: {"brand": "کلور", "model_code": "15 نفره استیل", "category": "شستشو و نظافت", "standard_name": "ماشین ظرفشویی 15 نفره اینورتر کلور استیل"},
    105: {"brand": "کلور", "model_code": "16 نفره لمسی استیل", "category": "شستشو و نظافت", "standard_name": "ماشین ظرفشویی 16 نفره لمسی کلور استیل"},
    106: {"brand": "فیلیپس", "model_code": "7778", "category": "لوازم برقی و پخت و پز", "standard_name": "غذاساز همه کاره فیلیپس مدل HR7778"},
    107: {"brand": "الکترواستیل", "model_code": "21", "category": "لوازم برقی و پخت و پز", "standard_name": "فر الکترواستیل عرض 60 چرمی مدل 21"},
    108: {"brand": "آلتون", "model_code": "7303", "category": "لوازم برقی و پخت و پز", "standard_name": "فر توکار آلتون مدل 7303"},
    109: {"brand": "پرومارون", "model_code": "9909", "category": "زیبایی و سلامت فردی", "standard_name": "فر کننده مو مخروطی پرومارون مدل RL-9909"},
    110: {"brand": "آلتون", "model_code": "MDS", "category": "لوازم برقی و پخت و پز", "standard_name": "اجاق گاز مبله فردار آلتون مدل MDS"},
    111: {"brand": "آلتون", "model_code": "MD5W", "category": "لوازم برقی و پخت و پز", "standard_name": "اجاق گاز مبله فردار آلتون مدل MD5W سفید"},
    112: {"brand": "ریگور", "model_code": "ریگور", "category": "یخچال و فریزر", "standard_name": "فریزر تک خانگی ریگور"},
    113: {"brand": "الکتروسان", "model_code": "345", "category": "یخچال و فریزر", "standard_name": "فریزر صندوقی الکتروسان مدل 345"},
    114: {"brand": "تکنو سان", "model_code": "سفید بزرگ", "category": "یخچال و فریزر", "standard_name": "فریزر صندوقی تکنو سان سفید بزرگ"},
    115: {"brand": "الکتروسان", "model_code": "280", "category": "یخچال و فریزر", "standard_name": "فریزر صندوقی الکتروسان مدل 280 سفید"},
    116: {"brand": "کلور", "model_code": "روسوپلاس عرض 60", "category": "یخچال و فریزر", "standard_name": "فریزر تک کلور عرض 60 مدل روسو پلاس سفید"},
    117: {"brand": "کلور", "model_code": "روسوپلاس عرض 60", "category": "یخچال و فریزر", "standard_name": "فریزر تک کلور عرض 60 مدل روسو پلاس مشکی"},
    118: {"brand": "کلور", "model_code": "روسوپلاس عرض 60", "category": "یخچال و فریزر", "standard_name": "فریزر تک کلور عرض 60 مدل روسو پلاس استیل"},
    119: {"brand": "کلور", "model_code": "گلوری عرض 60", "category": "یخچال و فریزر", "standard_name": "فریزر تک کلور عرض 60 مدل گلوری استیل"},
    120: {"brand": "کلور", "model_code": "گلوری پلاس عرض 60", "category": "یخچال و فریزر", "standard_name": "فریزر تک کلور عرض 60 مدل گلوری پلاس سفید"},
    121: {"brand": "کلور", "model_code": "گلوری عرض 60", "category": "یخچال و فریزر", "standard_name": "فریزر تک کلور عرض 60 مدل گلوری سفید کره ای"},
    122: {"brand": "کلور", "model_code": "روسو 70 آبریز استیل", "category": "یخچال و فریزر", "standard_name": "فریزر تک کلور 70 فوت مدل روسو آبریزدار استیل"},
    123: {"brand": "کلور", "model_code": "روسو 70 آبریز سفید", "category": "یخچال و فریزر", "standard_name": "فریزر تک کلور 70 فوت مدل روسو آبریزدار سفید"},
    124: {"brand": "کلور", "model_code": "روسو 70 هوم بار استیل", "category": "یخچال و فریزر", "standard_name": "فریزر تک کلور 70 فوت مدل روسو هوم بار استیل"},
    125: {"brand": "کلور", "model_code": "روسو 70 هوم بار سفید", "category": "یخچال و فریزر", "standard_name": "فریزر تک کلور 70 فوت مدل روسو هوم بار سفید"},
    126: {"brand": "کلور", "model_code": "گلوری پلاس عرض 70", "category": "یخچال و فریزر", "standard_name": "فریزر تک کلور عرض 70 مدل گلوری پلاس سفید"},
    127: {"brand": "کلور", "model_code": "101", "category": "یخچال و فریزر", "standard_name": "فریزر تک 27 فوت کلور مدل 101 سفید کره ای"},
    128: {"brand": "هیمالیا", "model_code": "60MW", "category": "یخچال و فریزر", "standard_name": "فریزر تک هیمالیا مدل آیس پول 60MW استیل"},
    129: {"brand": "هیمالیا", "model_code": "60MW", "category": "یخچال و فریزر", "standard_name": "فریزر تک هیمالیا مدل آیس پول 60MW طرح چرم"},
    130: {"brand": "اویز", "model_code": "سایز 20 مشکی", "category": "لوازم برقی و پخت و پز", "standard_name": "قابلمه گرانیتی اویز سایز 20 مشکی"},
    131: {"brand": "اویز", "model_code": "سایز 22 مشکی", "category": "لوازم برقی و پخت و پز", "standard_name": "قابلمه گرانیتی اویز سایز 22 مشکی"},
    132: {"brand": "اویز", "model_code": "سایز 32 مشکی", "category": "لوازم برقی و پخت و پز", "standard_name": "قابلمه گرانیتی اویز سایز 32 مشکی"},
    133: {"brand": "اویز", "model_code": "سایز 32 مشکی", "category": "لوازم برقی و پخت و پز", "standard_name": "قابلمه گرانیتی اویز سایز 32 مشکی"},
    134: {"brand": "اویز", "model_code": "سایز 24 مشکی", "category": "لوازم برقی و پخت و پز", "standard_name": "قابلمه گرانیتی اویز سایز 24 مشکی"},
    135: {"brand": "اویز", "model_code": "سایز 24 مشکی", "category": "لوازم برقی و پخت و پز", "standard_name": "قابلمه گرانیتی اویز سایز 24 مشکی"},
    136: {"brand": "اویز", "model_code": "سایز 16 مشکی", "category": "لوازم برقی و پخت و پز", "standard_name": "قابلمه گرانیتی اویز سایز 16 مشکی"},
    137: {"brand": "اویز", "model_code": "سایز 26 مشکی", "category": "لوازم برقی و پخت و پز", "standard_name": "قابلمه گرانیتی اویز سایز 26 مشکی"},
    138: {"brand": "اویز", "model_code": "سایز 18 مشکی", "category": "لوازم برقی و پخت و پز", "standard_name": "قابلمه گرانیتی اویز سایز 18 مشکی"},
    139: {"brand": "اویز", "model_code": "سایز 28 مشکی", "category": "لوازم برقی و پخت و پز", "standard_name": "قابلمه گرانیتی اویز سایز 28 مشکی"},
    140: {"brand": "لاوان", "model_code": "سایز 14", "category": "لوازم برقی و پخت و پز", "standard_name": "قابلمه تک گرانیتی لاوان سایز 14"},
    141: {"brand": "اویز پلاس", "model_code": "مرغ خوری مشکی", "category": "لوازم برقی و پخت و پز", "standard_name": "قابلمه مرغ خوری اویز پلاس مشکی"},
    142: {"brand": "تفال", "model_code": "2L", "category": "نوشیدنی ساز", "standard_name": "کتری برقی تفال مدل 2L"},
    143: {"brand": "زامروتی", "model_code": "تک کرم", "category": "نوشیدنی ساز", "standard_name": "کتری برقی زامروتی رنگ کرم"},
    144: {"brand": "سانی", "model_code": "1.5 لیتر", "category": "نوشیدنی ساز", "standard_name": "کتری برقی سانی 1.5 لیتری"},
    145: {"brand": "وگاتی", "model_code": "وگاتی", "category": "نوشیدنی ساز", "standard_name": "کتری برقی پیرکس وگاتی"},
    146: {"brand": "وگاتی", "model_code": "توپی", "category": "نوشیدنی ساز", "standard_name": "کتری برقی وگاتی طرح توپی"},
    147: {"brand": "وولگا", "model_code": "وولگا", "category": "نوشیدنی ساز", "standard_name": "کتری برقی استیل وولگا"},
    148: {"brand": "وستینگهاوس", "model_code": "آبی", "category": "نوشیدنی ساز", "standard_name": "کتری برقی رترو وستینگهاوس رنگ آبی"},
    149: {"brand": "وستینگهاوس", "model_code": "کرم", "category": "نوشیدنی ساز", "standard_name": "کتری برقی رترو وستینگهاوس رنگ کرم"},
    150: {"brand": "پروکس", "model_code": "پروکس", "category": "نوشیدنی ساز", "standard_name": "کتری برقی پیرکس پروکس"},
    151: {"brand": "ساپر", "model_code": "1011", "category": "نوشیدنی ساز", "standard_name": "کتری برقی ساپر مدل SEK-1011 استیل"},
    152: {"brand": "ساپر", "model_code": "1031", "category": "نوشیدنی ساز", "standard_name": "کتری برقی ساپر مدل SEK-1031 سبز"},
    153: {"brand": "ساپر", "model_code": "1031", "category": "نوشیدنی ساز", "standard_name": "کتری برقی ساپر مدل SEK-1031 کرم"},
    154: {"brand": "سیماران", "model_code": "750", "category": "نوشیدنی ساز", "standard_name": "کتری برقی سیماران مدل SEK-750 استیل"},
    155: {"brand": "ژمبو", "model_code": "2022", "category": "نوشیدنی ساز", "standard_name": "کتری و قوری روگازی ژمبو مدل 2022 دسته استیل"},
    156: {"brand": "ژمبو", "model_code": "2022", "category": "نوشیدنی ساز", "standard_name": "کتری و قوری روگازی ژمبو مدل 2022 دسته چوبی"},
    157: {"brand": "متفرقه", "model_code": "604", "category": "نوشیدنی ساز", "standard_name": "کتری و قوری روگازی هرمی مدل 604 تمام طلا"},
    158: {"brand": "سیستمی انبار", "model_code": "کسر و اضافات", "category": "لوازم برقی و پخت و پز", "standard_name": "کسر و اضافات کالا (ردیف تعدیل موجودی انبار)"},
    159: {"brand": "هیمالیا", "model_code": "عرض 850 تیتان", "category": "یخچال و فریزر", "standard_name": "یخچال فریزر کمبی هیمالیا عرض 850 تیتانیوم"},
    160: {"brand": "متفرقه", "model_code": "4500", "category": "سرمایش و گرمایش", "standard_name": "کولر آبی مدل 4500"},
    161: {"brand": "اوناکس", "model_code": "H50", "category": "سرمایش و گرمایش", "standard_name": "کولر آبی اوناکس یاسان مدل H50"},
    162: {"brand": "اوناکس", "model_code": "B35", "category": "سرمایش و گرمایش", "standard_name": "کولر آبی اوناکس مدل B35"},
    163: {"brand": "اوجنرال", "model_code": "18هزار", "category": "سرمایش و گرمایش", "standard_name": "کولر گازی پنجره ای 18000 اوجنرال"},
    164: {"brand": "پاکشوما", "model_code": "18هزار", "category": "سرمایش و گرمایش", "standard_name": "کولر گازی اسپلیت دیواری 18000 پاکشوما"},
    165: {"brand": "ریتون", "model_code": "ریتون", "category": "سرمایش و گرمایش", "standard_name": "کولر آبی سلولزی پرتابل ریتون"},
    166: {"brand": "وستینگهاوس", "model_code": "30کوپلند", "category": "سرمایش و گرمایش", "standard_name": "کولر گازی اسپلیت 30000 وستینگهاوس موتور کوپلند"},
    167: {"brand": "آلتون", "model_code": "S517", "category": "لوازم برقی و پخت و پز", "standard_name": "اجاق گاز صفحه ای آلتون مدل S517 استیل"},
    168: {"brand": "آلتون", "model_code": "SG518", "category": "لوازم برقی و پخت و پز", "standard_name": "اجاق گاز صفحه ای آلتون مدل SG518 استیل"},
    169: {"brand": "دونالکس", "model_code": "275", "category": "لوازم برقی و پخت و پز", "standard_name": "گوشت کوب برقی تک کاره دونالکس مدل DN-275"},
    170: {"brand": "دونالکس", "model_code": "290", "category": "لوازم برقی و پخت و پز", "standard_name": "گوشت کوب برقی و غذاساز چند کاره دونالکس مدل DN-290"},
    171: {"brand": "ریتون", "model_code": "17 دوقلو", "category": "شستشو و نظافت", "standard_name": "ماشین لباسشویی دوقلو 17 کیلویی ریتون"},
    172: {"brand": "پاکشوما", "model_code": "15ک", "category": "شستشو و نظافت", "standard_name": "ماشین لباسشویی دوقلو 15 کیلویی پاکشوما"},
    173: {"brand": "پاکشوما", "model_code": "9 کیلو", "category": "شستشو و نظافت", "standard_name": "ماشین لباسشویی دوقلو 9 کیلویی پاکشوما"},
    174: {"brand": "فریدولین", "model_code": "3.5 کیلو", "category": "شستشو و نظافت", "standard_name": "ماشین لباسشویی مینی واش فریدولین 3.5 کیلویی"},
    175: {"brand": "کلور", "model_code": "9tw1", "category": "شستشو و نظافت", "standard_name": "ماشین لباسشویی 9 کیلویی لمسی کلور مدل 9tw1 سفید"},
    176: {"brand": "دوو", "model_code": "991s", "category": "شستشو و نظافت", "standard_name": "ماشین لباسشویی اتوماتیک دوو 9 کیلویی مدل 991s"},
    177: {"brand": "پاکشوما", "model_code": "21 کیلو", "category": "شستشو و نظافت", "standard_name": "ماشین لباسشویی دوقلو 21 کیلویی پاکشوما"},
    178: {"brand": "دوو", "model_code": "8 کیلو سیلور", "category": "شستشو و نظافت", "standard_name": "ماشین لباسشویی اتوماتیک دوو 8 کیلویی سیلور"},
    179: {"brand": "فریدولین", "model_code": "3.5 تک درب", "category": "شستشو و نظافت", "standard_name": "ماشین لباسشویی مینی واش تک درب فریدولین 3.5 کیلویی"},
    180: {"brand": "کلور", "model_code": "10 کیلو سبز", "category": "شستشو و نظافت", "standard_name": "ماشین لباسشویی 10 کیلویی دایرکت درایو کلور سبز پاستیلی"},
    181: {"brand": "کلور", "model_code": "10 کیلو کرمی", "category": "شستشو و نظافت", "standard_name": "ماشین لباسشویی 10 کیلویی دایرکت درایو کلور رنگ کرم"},
    182: {"brand": "کلور", "model_code": "8 کیلو اینوکس", "category": "شستشو و نظافت", "standard_name": "ماشین لباسشویی 8 کیلویی لمسی کلور رنگ اینوکس"},
    183: {"brand": "کلور", "model_code": "9 کیلو ویوا", "category": "شستشو و نظافت", "standard_name": "ماشین لباسشویی 9 کیلویی کلور مدل ویوا سفید"},
    184: {"brand": "هیمالیا", "model_code": "تسلا پرو 10k استیل", "category": "شستشو و نظافت", "standard_name": "ماشین لباسشویی 10 کیلویی هیمالیا مدل تسلا پرو استیل"},
    185: {"brand": "هیمالیا", "model_code": "تسلا پرو 10k سفید", "category": "شستشو و نظافت", "standard_name": "ماشین لباسشویی 10 کیلویی هیمالیا مدل تسلا پرو سفید"},
    186: {"brand": "پرو امگا", "model_code": "تک", "category": "زیبایی و سلامت فردی", "standard_name": "ماشین اصلاح سر و صورت پرو امگا مدل تک"},
    187: {"brand": "پرو امگا", "model_code": "8 کاره", "category": "زیبایی و سلامت فردی", "standard_name": "ماشین اصلاح چند کاره پرو امگا مدل 8 کاره"},
    188: {"brand": "پرو امگا", "model_code": "شارژی و برقی", "category": "زیبایی و سلامت فردی", "standard_name": "ماشین اصلاح سر و صورت پرو امگا مدل شارژی و برقی"},
    189: {"brand": "زامروتی", "model_code": "کرم", "category": "نوشیدنی ساز", "standard_name": "مخلوط کن زامروتی رنگ کرم"},
    190: {"brand": "دونالکس", "model_code": "205", "category": "نوشیدنی ساز", "standard_name": "مخلوط کن و آسیاب دونالکس مدل DN-205"},
    191: {"brand": "وستینگهاوس", "model_code": "آبی", "category": "نوشیدنی ساز", "standard_name": "مخلوط کن رترو وستینگهاوس رنگ آبی"},
    192: {"brand": "وستینگهاوس", "model_code": "کرم", "category": "نوشیدنی ساز", "standard_name": "مخلوط کن رترو وستینگهاوس رنگ کرم"},
    193: {"brand": "اوریکس", "model_code": "کاسه چرخ دار", "category": "نوشیدنی ساز", "standard_name": "همزن کاسه دار چرخشی اوریکس"},
    194: {"brand": "کنوود", "model_code": "HM430", "category": "نوشیدنی ساز", "standard_name": "همزن کاسه دار کنوود مدل HM430"},
    195: {"brand": "دونالکس", "model_code": "355", "category": "نوشیدنی ساز", "standard_name": "همزن برقی دستی دونالکس مدل DN-355"},
    196: {"brand": "وستینگهاوس", "model_code": "آبی", "category": "نوشیدنی ساز", "standard_name": "همزن برقی دستی وستینگهاوس رنگ آبی"},
    197: {"brand": "وستینگهاوس", "model_code": "کرم", "category": "نوشیدنی ساز", "standard_name": "همزن برقی دستی وستینگهاوس رنگ کرم"},
    198: {"brand": "ساپر", "model_code": "1710", "category": "لوازم برقی و پخت و پز", "standard_name": "هواپز ساپر 7.2 لیتری مدل SAF-1710"},
    199: {"brand": "آلتون", "model_code": "H312", "category": "لوازم برقی و پخت و پز", "standard_name": "هود مخفی آلتون مدل H312"},
    200: {"brand": "آلتون", "model_code": "H315B", "category": "لوازم برقی و پخت و پز", "standard_name": "هود مخفی آلتون مدل H315B"},
    201: {"brand": "بست", "model_code": "BOST", "category": "یخچال و فریزر", "standard_name": "یخچال و فریزر 24 فوت بست مدل BOST"},
    202: {"brand": "دیپوینت", "model_code": "T7", "category": "یخچال و فریزر", "standard_name": "یخچال و فریزر 32 فوت دیپوینت مدل T7 استیل"},
    203: {"brand": "دیپوینت", "model_code": "T7", "category": "یخچال و فریزر", "standard_name": "یخچال و فریزر 28 فوت دیپوینت مدل T7 سفید"},
    204: {"brand": "دیپوینت", "model_code": "Dipoent", "category": "یخچال و فریزر", "standard_name": "یخچال و فریزر دیپوینت استیل"},
    205: {"brand": "کلور", "model_code": "مینی پاستیلی", "category": "یخچال و فریزر", "standard_name": "مینی یخچال 10 فوت کلور رنگ آبی پاستیلی"},
    206: {"brand": "کلور", "model_code": "مینی طرحدار", "category": "یخچال و فریزر", "standard_name": "مینی یخچال 10 فوت کلور رنگ آبی طرح دار"},
    207: {"brand": "کلور", "model_code": "مینی پاستیلی", "category": "یخچال و فریزر", "standard_name": "مینی یخچال 10 فوت کلور رنگ سبز پاستیلی"},
    208: {"brand": "کلور", "model_code": "مینی طرحدار", "category": "یخچال و فریزر", "standard_name": "مینی یخچال 10 فوت کلور رنگ سبز طرح دار"},
    209: {"brand": "کلور", "model_code": "مینی طرحدار", "category": "یخچال و فریزر", "standard_name": "مینی یخچال 10 فوت کلور رنگ سفید طرح دار"},
    210: {"brand": "کلور", "model_code": "مینی طرحدار", "category": "یخچال و فریزر", "standard_name": "مینی یخچال 10 فوت کلور رنگ مشکی طرح دار"},
    211: {"brand": "کلور", "model_code": "مینی مات", "category": "یخچال و فریزر", "standard_name": "مینی یخچال 10 فوت کلور رنگ مشکی مات"},
    212: {"brand": "الکترواستیل", "model_code": "یخساز تیتانیوم", "category": "یخچال و فریزر", "standard_name": "یخچال الکترواستیل یخسازدار تیتانیوم"},
    213: {"brand": "ایستکول", "model_code": "9 فوت", "category": "یخچال و فریزر", "standard_name": "یخچال 9 فوت ایستکول سفید مدل هتلی 2919"},
    214: {"brand": "ایستکول", "model_code": "9 فوت", "category": "یخچال و فریزر", "standard_name": "یخچال 9 فوت ایستکول نوک مدادی مدل هتلی 2919"},
    215: {"brand": "کلور", "model_code": "روسو 70 سفید", "category": "یخچال و فریزر", "standard_name": "یخچال و فریزر کمبی کلور 70 فوت مدل روسو سفید"},
    216: {"brand": "دیپوینت", "model_code": "BOOS", "category": "یخچال و فریزر", "standard_name": "یخچال فریزر 30 فوت دیپوینت مدل Boss Pro سفید"},
    217: {"brand": "هیمالیا", "model_code": "60MW", "category": "یخچال و فریزر", "standard_name": "یخچال فریزر 5 کاره هیمالیا هوم بار طرح چرم مدل 60MW"},
    218: {"brand": "هیمالیا", "model_code": "omega", "category": "یخچال و فریزر", "standard_name": "یخچال فریزر هیمالیا مدل امگا (Omega) هوم بار سفید"},
    219: {"brand": "نیکسان", "model_code": "RF84102E2", "category": "یخچال و فریزر", "standard_name": "یخچال فریزر نیکسان مدل RF84102E2 استیل"},
    220: {"brand": "نیکسان", "model_code": "RF84102E2", "category": "یخچال و فریزر", "standard_name": "یخچال فریزر نیکسان مدل RF84102E2 طرح چرم"},
    221: {"brand": "کلور", "model_code": "101", "category": "یخچال و فریزر", "standard_name": "یخچال فریزر کمبی کلور 27 فوت مدل FRNT101 سفید ساده"},
    222: {"brand": "کلور", "model_code": "روسوپلاس عرض 60", "category": "یخچال و فریزر", "standard_name": "یخچال تک کلور عرض 60 مدل روسو پلاس استیل"},
    223: {"brand": "کلور", "model_code": "روسوپلاس عرض 60", "category": "یخچال و فریزر", "standard_name": "یخچال تک کلور عرض 60 مدل روسو پلاس سفید"},
    224: {"brand": "کلور", "model_code": "روسوپلاس عرض 60", "category": "یخچال و فریزر", "standard_name": "یخچال تک کلور عرض 60 مدل روسو پلاس مشکی"},
    225: {"brand": "کلور", "model_code": "گلوری عرض 60", "category": "یخچال و فریزر", "standard_name": "یخچال تک کلور عرض 60 مدل گلوری استیل"},
    226: {"brand": "کلور", "model_code": "گلوری پلاس عرض 60", "category": "یخچال و فریزر", "standard_name": "یخچال تک کلور عرض 60 مدل گلوری پلاس سفید"},
    227: {"brand": "کلور", "model_code": "گلوری عرض 60", "category": "یخچال و فریزر", "standard_name": "یخچال تک کلور عرض 60 مدل گلوری سفید کره ای"},
    228: {"brand": "کلور", "model_code": "روسو 70 آبریز استیل", "category": "یخچال و فریزر", "standard_name": "یخچال تک کلور 70 فوت مدل روسو آبریزدار استیل"},
    229: {"brand": "کلور", "model_code": "روسو 70 آبریز سفید", "category": "یخچال و فریزر", "standard_name": "یخچال تک کلور 70 فوت مدل روسو آبریزدار سفید"},
    230: {"brand": "کلور", "model_code": "روسو 70 هوم بار استیل", "category": "یخچال و فریزر", "standard_name": "یخچال تک کلور 70 فوت مدل روسو هوم بار استیل"},
    231: {"brand": "کلور", "model_code": "روسو 70 هوم بار سفید", "category": "یخچال و فریزر", "standard_name": "یخچال تک کلور 70 فوت مدل روسو هوم بار سفید"},
    232: {"brand": "کلور", "model_code": "گلوری پلاس عرض 70", "category": "یخچال و فریزر", "standard_name": "یخچال تک کلور عرض 70 مدل گلوری پلاس سفید"},
    233: {"brand": "کلور", "model_code": "101", "category": "یخچال و فریزر", "standard_name": "یخچال تک 27 فوت کلور مدل 101 استیل"},
    234: {"brand": "کلور", "model_code": "101", "category": "یخچال و فریزر", "standard_name": "یخچال تک 27 فوت کلور مدل 101 سفید کره ای"},
    235: {"brand": "کلور", "model_code": "R(re01)", "category": "یخچال و فریزر", "standard_name": "مینی یخچال 10 فوت کلور مدل R(re01) قرمز"},
    236: {"brand": "کلور", "model_code": "مینی", "category": "یخچال و فریزر", "standard_name": "مینی یخچال 10 فوت کلور سفید"},
    237: {"brand": "هیمالیا", "model_code": "60MW", "category": "یخچال و فریزر", "standard_name": "یخچال تک هیمالیا مدل آیس پول 60MW استیل"},
    238: {"brand": "هیمالیا", "model_code": "60MW", "category": "یخچال و فریزر", "standard_name": "یخچال تک هیمالیا مدل آیس پول 60MW طرح چرم"},
}

def clean_raw_desc(raw_desc):
    # تمیزکاری خط‌فاصله‌ها و کاراکترهای اسلش
    cleaned = re.sub(r'[-—_/]+', ' ', raw_desc).strip()
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned

def run_normalization():
    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        incoming_items = json.load(f)
        
    print(f"تعداد ورودی اولیه: {len(incoming_items)}")
    
    normalized_list = []
    category_counts = {}
    brand_counts = {}
    
    for it in incoming_items:
        raw_idx = it['raw_index']
        raw_desc = it['raw_desc']
        qty = it['raw_quantity']
        in_stock = it['in_stock']
        line_num = it.get('line_num')
        
        meta = ITEMS_METADATA.get(raw_idx)
        if not meta:
            raise ValueError(f"اطلاعات ردیف {raw_idx} تعریف نشده است!")
            
        cleaned = clean_raw_desc(raw_desc)
        
        item_obj = {
            "raw_index": raw_idx,
            "line_num": line_num,
            "raw_quantity": qty,
            "in_stock": in_stock,
            "raw_desc": raw_desc,
            "cleaned_raw_desc": cleaned,
            "brand": meta["brand"],
            "model_code": meta["model_code"],
            "category": meta["category"],
            "standard_name": meta["standard_name"]
        }
        
        normalized_list.append(item_obj)
        
        # آمار
        c = meta["category"]
        category_counts[c] = category_counts.get(c, 0) + 1
        b = meta["brand"]
        brand_counts[b] = brand_counts.get(b, 0) + 1
        
    # ذخیره در فایل خروجی نهایی
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(normalized_list, f, ensure_ascii=False, indent=2)
        
    print(f"عملیات نرمال‌سازی با موفقیت انجام شد و در {OUTPUT_JSON} ذخیره گردید.")
    print(f"تعداد کل اقلام پردازش شده: {len(normalized_list)}")
    
    print("\n--- تفکیک اقلام بر اساس دسته‌بندی‌های ۸ گانه ---")
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  * {cat}: {count} قلم")
        
    print("\n--- تفکیک اقلام بر اساس برندها ---")
    for brand, count in sorted(brand_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  * {brand}: {count} قلم")

if __name__ == '__main__':
    run_normalization()
