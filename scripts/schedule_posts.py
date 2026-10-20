import sys
import json
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Content-Type': 'application/json'
}

# Schedule: Sunday, Tuesday, Thursday at 19:30:00
# Last previous scheduled: 2026-08-25T19:30:00 (Tuesday 3-6-1405)
SCHEDULE_MAP = [
    {
        'id': 3214,
        'title': 'راهنمای جامع خرید دستگاه تصفیه آب خانگی',
        'date': '2026-08-27T19:30:00',
        'persian_date': 'پنج‌شنبه ۵ شهریور ۱۴۰۵ - ساعت ۱۹:۳۰'
    },
    {
        'id': 3215,
        'title': 'بررسی تخصصی برند دیپوینت (Depoint)',
        'date': '2026-08-30T19:30:00',
        'persian_date': 'یک‌شنبه ۸ شهریور ۱۴۰۵ - ساعت ۱۹:۳۰'
    },
    {
        'id': 3217,
        'title': 'راهنمای خرید سرخ کن بدون روغن (ایرفرایر)',
        'date': '2026-09-01T19:30:00',
        'persian_date': 'سه‌شنبه ۱۰ شهریور ۱۴۰۵ - ساعت ۱۹:۳۰'
    },
    {
        'id': 3218,
        'title': 'راهنمای خرید اسپرسوساز خانگی',
        'date': '2026-09-03T19:30:00',
        'persian_date': 'پنج‌شنبه ۱۲ شهریور ۱۴۰۵ - ساعت ۱۹:۳۰'
    },
    {
        'id': 3219,
        'title': 'راهنمای خرید ماشین اصلاح موی سر و صورت',
        'date': '2026-09-06T19:30:00',
        'persian_date': 'یک‌شنبه ۱۵ شهریور ۱۴۰۵ - ساعت ۱۹:۳۰'
    },
    {
        'id': 3220,
        'title': 'نکات طلایی نگهداری و محافظت از لوازم خانگی در خوزستان',
        'date': '2026-09-08T19:30:00',
        'persian_date': 'سه‌شنبه ۱۷ شهریور ۱۴۰۵ - ساعت ۱۹:۳۰'
    }
]

def schedule_posts():
    print("=== Scheduling 6 Posts to Future Dates ===")
    for item in SCHEDULE_MAP:
        url = f"https://hosseinykala.ir/wp-json/wp/v2/posts/{item['id']}"
        payload = {
            'status': 'future',
            'date': item['date']
        }
        res = requests.post(url, auth=AUTH, headers=HEADERS, json=payload, timeout=20)
        if res.status_code == 200:
            data = res.json()
            print(f"[OK] Post {item['id']} scheduled -> Status: {data.get('status')}, Date: {data.get('date')} ({item['persian_date']})")
        else:
            print(f"[FAIL] Post {item['id']}: HTTP {res.status_code} - {res.text[:100]}")

if __name__ == '__main__':
    schedule_posts()
