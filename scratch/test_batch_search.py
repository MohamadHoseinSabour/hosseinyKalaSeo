import urllib.request
import urllib.parse
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def search_torob(q):
    url = f"https://api.torob.com/v4/base-product/search/?sort=popularity&page=0&size=5&query={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('results', [])
    except Exception as e:
        return []

def search_digikala(q):
    url = f"https://api.digikala.com/v1/search/?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('data', {}).get('products', [])
    except Exception as e:
        return []

test_items = [
    'دیپوینت اکسپلور',
    'دیپوینت دیسنت',
    'الکترواستیل سری 10',
    'الکترواستیل 14 فوت',
    'الکترواستیل کمپکت',
    'الکترواستیل 27 فوت تیتانیوم',
    'الکترواستیل 34 فوت',
    'تلویزیون دوو 7000 55',
    'جاروبرقی جنرال فیت 4500',
    'جاروبرقی جنرال فیت 5300',
    'جارو شارژی باخ 1454',
    'بخارگر BUVCK',
    'بخاری پلار سنگی',
    'آبگرمکن ایران شرق 3020',
    'بخاری آبسال 405',
    'اسپرسوساز وستینگهاوس 1663',
    'گوشت کوب وستینگهاوس قرمز',
    'آسیاب زیکو 6501',
    'آبمیوه گیری زیکو 4038',
    'میوه خشک کن مایر 5959',
    'سشوار زیکو 5020',
    'خردکن ویلز 6033',
    'هود التون 900'
]

for t in test_items:
    print(f"\n==================== SEARCH: {t} ====================")
    torob_res = search_torob(t)
    if torob_res:
        print("  Torob:")
        for r in torob_res[:2]:
            print(f"    - Title: {r.get('name1')} | Img: {r.get('image_url')}")
    else:
        print("  Torob: No results")
        
    dk_res = search_digikala(t)
    if dk_res:
        print("  Digikala:")
        for p in dk_res[:2]:
            img_url = p.get('images', {}).get('main', {}).get('url', [''])[0]
            print(f"    - Title: {p.get('title_fa')} | Img: {img_url}")
    else:
        print("  Digikala: No results")
