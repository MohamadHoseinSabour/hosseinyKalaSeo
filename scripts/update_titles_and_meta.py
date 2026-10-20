import sys
import requests
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

POST_UPDATES = [
    {
        'id': 3000,
        'title': 'راهنمای خرید کولر آبی سلولزی و پرتابل؛ بهترین مارک، ابعاد و قیمت روز بازار | حسینی کالا',
        'meta': {
            'rank_math_title': 'راهنمای خرید کولر آبی سلولزی و پرتابل؛ بررسی سرمایش، ابعاد و قیمت روز | حسینی کالا',
            'rank_math_description': 'بهترین کولر آبی سلولزی و پرتابل کدام است؟ راهنمای انتخاب کولر بدون کانال‌کشی ریتون برای خانه و مغازه در خوزستان و جنوب با ضمانت اصالت در حسینی کالا اهواز.',
            'rank_math_focus_keyword': 'راهنمای خرید کولر آبی سلولزی'
        }
    },
    {
        'id': 3098,
        'title': 'راهنمای خرید یخچال کوچک و هتلی (۳ تا ۹ فوت)؛ مناسب مغازه، سوئیت و اتاق | حسینی کالا',
        'meta': {
            'rank_math_title': 'راهنمای خرید یخچال کوچک و هتلی؛ بهترین مدل‌های ۳ تا ۹ فوت برای مغازه و اتاق | حسینی کالا',
            'rank_math_description': 'راهنمای انتخاب و خرید یخچال کوچک و هتلی ارزان. بررسی ابعاد یخچال ایستکول و کلور برای مغازه، هتل، اداره و خوابگاه با بهترین قیمت در حسینی کالا اهواز.',
            'rank_math_focus_keyword': 'راهنمای خرید یخچال کوچک'
        }
    },
    {
        'id': 3100,
        'title': 'یخچال کمبی یا دوقلو بخریم؟ مقایسه تخصصی فضا، ابعاد و قیمت روز انواع مدل‌ها',
        'meta': {
            'rank_math_title': 'یخچال کمبی بخریم یا دوقلو؟ مقایسه فضا، تفاوت ابعاد و هزینه خرید | حسینی کالا',
            'rank_math_description': 'مقایسه کامل یخچال کمبی با دوقلو. کدام مدل برای آشپزخانه و متراژ شما مناسب‌تر است؟ بررسی گنجایش، مصرف برق و قیمت در فروشگاه لوازم خانگی حسینی اهواز.',
            'rank_math_focus_keyword': 'یخچال کمبی یا دوقلو'
        }
    }
]

PRODUCT_UPDATES = [
    {
        'id': 2885,
        'title': 'جاروبرقی بست مدل BVC-PC18B موتور ۱۴۰۰ وات (ضمانت انتخاب سرویس)',
        'meta': {
            'rank_math_title': 'قیمت و خرید جاروبرقی بست مدل BVC-PC18B اصل (گارانتی انتخاب سرویس) | حسینی کالا',
            'rank_math_description': 'خرید اینترنتی جاروبرقی بست مدل BVC-PC18B با موتور پرقدرت ۱۴۰۰ وات، فیلتر بهداشتی HEPA و گارانتی رسمی انتخاب سرویس. ارسال سریع و بهترین قیمت در حسینی کالا اهواز.',
            'rank_math_focus_keyword': 'جاروبرقی بست'
        }
    },
    {
        'id': 2538,
        'title': 'کولر آبی سلولزی پرتابل ۱۶۰۰۰ ریتون مدل VENTO (سرمایش فوق‌العاده)',
        'meta': {
            'rank_math_title': 'خرید کولر آبی سلولزی پرتابل ریتون ۱۶۰۰۰ مدل VENTO (سرمایش بالا) | حسینی کالا',
            'rank_math_description': 'قیمت و خرید کولر آبی سلولزی پرتابل ۱۶۰۰۰ ریتون مدل VENTO مناسب سالن‌های بزرگ و فضاهای تجاری. موتور کم‌مصرف، پد سلولزی ضخیم و ارسال به سراسر کشور از حسینی کالا.',
            'rank_math_focus_keyword': 'کولر پرتابل ریتون ۱۶۰۰۰'
        }
    },
    {
        'id': 3056,
        'title': 'ماشین اصلاح موی سر و صورت پرو امگا مدل T5 با تیغه کربن استیل',
        'meta': {
            'rank_math_title': 'خرید ماشین اصلاح موی سر و صورت پرو امگا مدل T5 با تیغه کربن استیل | حسینی کالا',
            'rank_math_description': 'خرید آنلاین ماشین اصلاح پرو امگا T5 با موتور پرقدرت و باتری لیتیومی بادوام. مناسب اصلاح حرفه‌ای سر و صورت با تضمین اصالت کالا در حسینی کالا اهواز.',
            'rank_math_focus_keyword': 'ماشین اصلاح پرو امگا'
        }
    },
    {
        'id': 3453,
        'title': 'یخچال فریزر دوقلو 21 فوت الکترواستیل مدل فیوچر (موتور اینورتر)',
        'meta': {
            'rank_math_title': 'قیمت و خرید یخچال فریزر دوقلو الکترواستیل مدل فیوچر ۲۱ فوت | حسینی کالا',
            'rank_math_description': 'خرید اینترنتی یخچال فریزر دوقلو الکترواستیل مدل فیوچر با ظرفیت ۲۱ فوت، سیستم نوفراست کامل، کمپرسور کم‌مصرف و گارانتی معتبر در حسینی کالا اهواز.',
            'rank_math_focus_keyword': 'یخچال فریزر دوقلو الکترواستیل'
        }
    }
]

print("=== Updating Post Titles and Meta ===", flush=True)
for item in POST_UPDATES:
    pid = item['id']
    payload = {
        'title': item['title'],
        'meta': item['meta']
    }
    url = f"https://hosseinykala.ir/wp-json/wp/v2/posts/{pid}"
    try:
        r = requests.post(url, auth=AUTH, headers=HEADERS, json=payload, timeout=20)
        print(f"[OK] Post {pid}: HTTP {r.status_code} -> Title: {item['title'][:40]}", flush=True)
    except Exception as e:
        print(f"[ERR] Post {pid}: {e}", flush=True)

print("\n=== Updating Product Titles and Meta ===", flush=True)
for item in PRODUCT_UPDATES:
    pid = item['id']
    payload = {
        'title': item['title'],
        'meta': item['meta']
    }
    url = f"https://hosseinykala.ir/wp-json/wp/v2/product/{pid}"
    try:
        r = requests.post(url, auth=AUTH, headers=HEADERS, json=payload, timeout=20)
        print(f"[OK] Product {pid}: HTTP {r.status_code} -> Title: {item['title'][:40]}", flush=True)
    except Exception as e:
        print(f"[ERR] Product {pid}: {e}", flush=True)

print("\n=== All Titles and Metadata Updated Successfully ===", flush=True)
