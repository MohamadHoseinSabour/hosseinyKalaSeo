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

payload = {
    'objectID': 160,
    'objectType': 'term',
    'meta': {
        'rank_math_title': 'قیمت و خرید جاروبرقی بست (Bost) به قیمت کارخانه | حسینی کالا',
        'rank_math_description': 'خرید انواع جاروبرقی بست با موتور پرقدرت و کم‌صدا به قیمت درب کارخانه. ضمانت ۲۴ ماهه انتخاب سرویس، خرید نقد و اقساط با ارسال فوری از حسینی کالا.',
        'rank_math_focus_keyword': 'جاروبرقی بست, قیمت جاروبرقی بست'
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
    print("Term 160 updateMeta response:", resp.read().decode('utf-8'))
except Exception as e:
    print("Term 160 updateMeta err:", e)
