import urllib.request
import base64
import json
import ssl
import sys

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://hosseinykala.ir/wp-json/rankmath/v1/updateMeta'
creds = base64.b64encode(b'agent:Mlwg pHHX NQ64 drrz 7ca2 IVto').decode('utf-8')

remaining = [
    {
        'id': 3065,
        'title': 'ماشین اصلاح موی سر و صورت پرو امگا مدل T7 خط زن و صفر زن | حسینی کالا',
        'desc': 'خرید ماشین اصلاح پرو امگا مدل T7 با بدنه تمام‌فلزی ارگونومیک، باتری لیتیومی بادوام و تیغه خط‌زن دقیق. گارانتی اصالت فیزیکی و ارسال سریع از حسینی کالا.',
        'keyword': 'ماشین اصلاح پرو امگا t7, ماشین اصلاح پرو امگا'
    },
    {
        'id': 3032,
        'title': 'گوشت کوب برقی دونالکس مدل DN-275 موتور قدرتمند | نقد و خرید حسینی کالا',
        'desc': 'خرید گوشت کوب برقی دونالکس مدل DN-275 با تیغه‌های استیل ضدزنگ و موتور کم‌صدا. قیمت دست اول بازار و ارسال فوری به سراسر کشور از فروشگاه حسینی کالا.',
        'keyword': 'گوشت کوب برقی دونالکس, گوشت کوب برقی دونالکس مدل dn 275'
    },
    {
        'id': 3026,
        'title': 'سرخ کن بدون روغن ۸ لیتری دونالکس مدل DN-950 لمسی | قیمت و خرید حسینی کالا',
        'desc': 'خرید سرخ کن بدون روغن (ایرفرایر) ۸ لیتر دونالکس مدل DN-950 با پنل دیجیتال لمسی و برنامه‌های پخت متنوع. قیمت رقابتی و ارسال سریع به سراسر کشور در حسینی کالا.',
        'keyword': 'سرخ کن دونالکس 950, ایرفرایر دونالکس'
    }
]

for item in remaining:
    payload = {
        'objectID': item['id'],
        'objectType': 'post',
        'meta': {
            'rank_math_title': item['title'],
            'rank_math_description': item['desc'],
            'rank_math_focus_keyword': item['keyword']
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Basic {creds}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        },
        method='POST'
    )
    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=8)
        print(f"ID {item['id']} updated successfully!")
    except Exception as e:
        print(f"ID {item['id']} err: {e}")
