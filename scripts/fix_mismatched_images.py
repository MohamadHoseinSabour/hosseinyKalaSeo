import os
import sys
import json
import requests
from PIL import Image
import io

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_NEW_PRODS = os.path.join(PROJECT_DIR, 'data', 'new_products')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

# Accurate, verified image sources for products that had mismatches
FIX_MAP = {
    # Donalex
    'donalex-dn-150-salad-maker-white': {
        'url': 'https://donalex.ir/Uploads/4e3fb609-5dfa-4ebf-85e7-eac37a84a25a.jpg',
        'title': 'سالادساز 6 کاره دونالکس مدل DN-150 (رنگ سفید)',
        'source': 'donalex.ir (سایت رسمی برند)'
    },
    'donalex-dn-150-salad-maker-black': {
        'url': 'https://donalex.ir/Uploads/022fccfc-c323-461c-b4f8-c0b97e070231.jpg',
        'title': 'سالادساز 6 کاره دونالکس مدل DN-150 (رنگ مشکی)',
        'source': 'donalex.ir (سایت رسمی برند)'
    },
    'donalex-dn-940-sandwich-maker-black': {
        'url': 'https://donalex.ir/Uploads/ac38d25d-34b0-4326-ac09-4ce071bf6d36.jpg',
        'title': 'ساندویچ‌ساز دونالکس مدل DN-940',
        'source': 'donalex.ir (سایت رسمی برند)'
    },
    'donalex-dn-955-air-fryer-8l': {
        'url': 'https://donalex.ir/Uploads/c07fb935-dfd6-41a3-8d00-b1ab60a2123f.gif',
        'title': 'سرخ‌کن بدون روغن دونالکس مدل DN-955',
        'source': 'donalex.ir (سایت رسمی برند)'
    },
    
    # Bellanzo
    'bellanzo-1136-electric-chopper': {
        'url': 'https://files.emalls.ir/files/Products/automatic/26784019/zymi3y5f.jpg',
        'title': 'خردکن دیجیتال دو کاسه بلانزو مدل BCH-1136',
        'source': 'emalls / بلانزو رسمی'
    },
    
    # Kahler irons
    'kahler-kh-812-steam-iron-white': {
        'url': 'https://kahler.ir/wp-content/uploads/2022/12/اتو-بخار-دستی-کاخلر-مدل-KH-812-W.webp',
        'title': 'اتو بخار دستی کاخلر مدل KH-812 سفید',
        'source': 'kahler.ir (سایت رسمی کاخلر)'
    },
    'kahler-kh-813-steam-iron-black-silver': {
        'url': 'https://kahler.ir/wp-content/uploads/2022/12/اتو-بخار-دستی-کاخلر-مدل-KH-813-G.webp',
        'title': 'اتو بخار دستی کاخلر مدل KH-813 خاکستری/مشکی',
        'source': 'kahler.ir (سایت رسمی کاخلر)'
    },
    'kahler-kh-814-steam-iron-black-rosegold': {
        'url': 'https://kahler.ir/wp-content/uploads/2022/12/اتو-بخار-دستی-kh-814-b.webp',
        'title': 'اتو بخار دستی کاخلر مدل KH-814 مشکی رزگلد',
        'source': 'kahler.ir (سایت رسمی کاخلر)'
    },
    
    # Edmilson
    'edmilson-ot-820-toaster-oven': {
        'url': 'https://edmilson.ir/wp-content/uploads/2021/12/to820-1.jpg',
        'title': 'آون توستر ادمیلسون مدل TO820',
        'source': 'edmilson.ir (سایت رسمی ادمیلسون)'
    },
    'edmilson-ot-827-solar-toaster-oven': {
        'url': 'https://edmilson.ir/wp-content/uploads/2024/11/ادمیلسون-OT827B.jpg',
        'title': 'آون سولار کانوکشن ادمیلسون مدل OT827',
        'source': 'edmilson.ir (سایت رسمی ادمیلسون)'
    },
    'edmilson-811-cordless-vacuum-cleaner-black': {
        'url': 'https://edmilson.ir/wp-content/uploads/2025/12/VC-512-811-B.jpg',
        'title': 'جارو شارژی عصایی و دستی ادمیلسون مدل VC811 مشکی',
        'source': 'edmilson.ir (سایت رسمی ادمیلسون)'
    },
    
    # Ebkazo
    'ebkazo-2139-garment-steamer': {
        'url': 'https://ebkazoshop.com/wp-content/uploads/2024/06/2137-700x700.webp',
        'title': 'اتو بخار مخزن‌دار ابکازو مدل SL-2137/2139',
        'source': 'ebkazoshop.com (سایت رسمی ابکازو)'
    },
    
    # Satia
    'satia-1215-stand-fan': {
        'url': 'https://satiacompany.com/wp-content/uploads/2025/12/IMG_20251206_141914_820.jpg',
        'title': 'پنکه ایستاده ساتیا مدل 1215',
        'source': 'satiacompany.com (سایت رسمی ساتیا)'
    },
    'satia-st-9015-digital-air-fryer': {
        'url': 'https://satiacompany.com/wp-content/uploads/2025/01/سرخ-کن-9050-300.jpg',
        'title': 'سرخ کن بدون روغن ساتیا مدل SDF-9015 / 9050',
        'source': 'satiacompany.com (سایت رسمی ساتیا)'
    },
    'satia-st-9025-digital-air-fryer': {
        'url': 'https://satiacompany.com/wp-content/uploads/2024/07/سرخ-کن-72.jpg',
        'title': 'سرخ کن بدون روغن ساتیا مدل SDF-9025 / 9955',
        'source': 'satiacompany.com (سایت رسمی ساتیا)'
    },
    
    # Monaco
    'monaco-20-bar-espresso-coffee-machine': {
        'url': 'https://dkstatics-public.digikala.com/digikala-products/304605902f7fc80a4dc5297b670abc8dd9a10ba8_1776669870.jpg',
        'title': 'دستگاه اسپرسوساز 1200 میلی‌لیتر موناکو مدل MF-1080FM',
        'source': 'digikala (اورجینال موناکو)'
    },
    
    # Oryx
    'oryx-rotating-bowl-stand-mixer': {
        'url': 'https://oryx.ir/wp-content/uploads/2024/01/همزن2.gif',
        'title': 'همزن کاسه دار چرخشی اوریکس مدل SM-4326',
        'source': 'oryx.ir (سایت رسمی اوریکس)'
    },
    
    # Pumps
    'shimge-1hp-cpm158-water-pump': {
        'url': 'https://www.famcocorp.com/Uploadfiles/CkEditor/Images/Shimge/shimge-pump-cpm-series.jpg',
        'title': 'پمپ آب یک اسب بشقابی شیمجه مدل CPM-158',
        'source': 'famcocorp.com (فامکو تخصصی پمپ شیمجه)'
    },
    'vatek-1hp-jet-water-pump': {
        'url': 'https://dkstatics-public.digikala.com/digikala-products/31f5c8fa9f45c6b76fbf972d75e774296552c80b_1785774261.jpg',
        'title': 'پمپ آب خانگی یک اسب بخار واتک مدل جتی CAM100',
        'source': 'digikala (اورجینال واتک)'
    },
    
    # Mixi
    'mixi-digital-body-scale-tempered-glass': {
        'url': 'https://dkstatics-public.digikala.com/digikala-products/0cc0d96e09bf5dbeed3fa513cb62e72236ed601a_1699199740.jpg',
        'title': 'ترازو وزن‌کشی دیجیتال شیشه‌ای دقیق خانگی (میکسی/مکسی)',
        'source': 'digikala'
    },
    
    # Tefal
    'tefal-2-2l-stainless-steel-electric-kettle': {
        'url': 'https://dkstatics-public.digikala.com/digikala-products/1870fd6ab044e6a4b2998e2bab263bffc528d48a_1716750195.jpg',
        'title': 'کتری برقی استیل ضد زنگ تفال مدل KI280D10 ظرفیت بالا',
        'source': 'digikala'
    },
    'tefal-easy-fry-healthy-air-fryer': {
        'url': 'https://dkstatics-public.digikala.com/digikala-products/abfe4d2691a72a56a752316a5710bc221715d0d1_1786652492.jpg',
        'title': 'سرخ کن بدون روغن تفال مدل ایزی فرای EY505',
        'source': 'digikala'
    },
    
    # Green heater
    'green-gas-heater-with-fan': {
        'url': 'https://dkstatics-public.digikala.com/digikala-products/064e62ffcffec1e32047395efbbff643b7ef33f0_1736780077.jpg',
        'title': 'فن هیتر برقی گرین لاین مدل GHT1500',
        'source': 'digikala'
    }
}

def download_and_optimize(img_url, out_path):
    r = requests.get(img_url, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        return False, f"HTTP {r.status_code}"
    
    img = Image.open(io.BytesIO(r.content))
    img = img.convert('RGB')
    
    w, h = img.size
    max_dim = max(w, h)
    
    # White square canvas
    square_img = Image.new('RGB', (max_dim, max_dim), (255, 255, 255))
    paste_x = (max_dim - w) // 2
    paste_y = (max_dim - h) // 2
    square_img.paste(img, (paste_x, paste_y))
    
    # Resize to 1000x1000
    if max_dim != 1000:
        square_img = square_img.resize((1000, 1000), Image.Resampling.LANCZOS)
        
    square_img.save(out_path, 'WEBP', quality=86, method=6)
    kb = os.path.getsize(out_path) / 1024
    return True, kb

print(f"=== شروع جایگزینی و بهینه‌سازی تصاویر مغایر ({len(FIX_MAP)} کالا) ===")
fixed_count = 0

for slug, data in FIX_MAP.items():
    folder = os.path.join(DATA_NEW_PRODS, slug, 'images')
    os.makedirs(folder, exist_ok=True)
    out_webp = os.path.join(folder, 'featured.webp')
    
    print(f"در حال پردازش: {slug}...")
    try:
        ok, res = download_and_optimize(data['url'], out_webp)
        if ok:
            print(f"   ✓ با موفقیت جایگزین شد ({res:.1f} KB) - {data['title'][:35]}")
            meta = {
                'source': data['source'],
                'source_title': data['title'],
                'img_url': data['url'],
                'size_kb': round(res, 2),
                'verified': True,
                'target_file': 'featured.webp',
                'dimensions': '1000x1000'
            }
            with open(os.path.join(folder, 'image_info.json'), 'w', encoding='utf-8') as f_meta:
                json.dump(meta, f_meta, ensure_ascii=False, indent=2)
            fixed_count += 1
        else:
            print(f"   ❌ خطا در دانلود/تبدیل: {res}")
    except Exception as e:
        print(f"   ❌ خطای استثنایی: {e}")

print(f"\n✓ جمع کل اقلام اصلاح و جایگزین شده با موفقیت: {fixed_count} از {len(FIX_MAP)}")
