import os
import sys
import io
import requests
from PIL import Image

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
BRAIN_DIR = r'C:\Users\mmhhs\.gemini\antigravity\brain\5af16dc4-2462-419a-b5e9-e6648d6bd5d0'

images_info = [
    {
        'file': 'water_purifier_kitchen_1787223492063.jpg',
        'target_name': 'home-water-purifier-buying-guide.jpg',
        'title': 'راهنمای خرید دستگاه تصفیه آب خانگی',
        'alt': 'راهنمای خرید دستگاه تصفیه آب خانگی سافت واتر'
    },
    {
        'file': 'depoint_refrigerator_kitchen_1787223515067.jpg',
        'target_name': 'depoint-refrigerator-brand-review.jpg',
        'title': 'بررسی تخصصی برند دیپوینت',
        'alt': 'بررسی تخصصی و کیفیت یخچال فریزر دیپوینت'
    },
    {
        'file': 'air_fryer_kitchen_1787223537065.jpg',
        'target_name': 'air-fryer-buying-guide.jpg',
        'title': 'راهنمای خرید سرخ کن بدون روغن ایرفرایر',
        'alt': 'راهنمای خرید سرخ کن بدون روغن ایرفرایر'
    },
    {
        'file': 'espresso_machine_kitchen_1787223546519.jpg',
        'target_name': 'home-espresso-maker-buying-guide.jpg',
        'title': 'راهنمای خرید اسپرسوساز خانگی',
        'alt': 'راهنمای خرید اسپرسوساز خانگی دونالکس'
    },
    {
        'file': 'hair_clipper_pure_1787223607304.jpg',
        'target_name': 'hair-clipper-buying-guide.jpg',
        'title': 'راهنمای خرید ماشین اصلاح موی سر و صورت',
        'alt': 'راهنمای خرید ماشین اصلاح موی سر و صورت پرو امگا'
    },
    {
        'file': 'appliances_protection_1787223579171.jpg',
        'target_name': 'home-appliances-maintenance-khuzestan.jpg',
        'title': 'محافظت از لوازم خانگی در برابر نوسان برق و گرما',
        'alt': 'محافظت و نگهداری از لوازم خانگی برقی در خوزستان'
    }
]

def upload_all():
    media_ids = {}
    for item in images_info:
        src_path = os.path.join(BRAIN_DIR, item['file'])
        if not os.path.exists(src_path):
            print(f"File not found: {src_path}")
            continue

        img = Image.open(src_path).convert('RGB')
        img = img.resize((1599, 900), Image.Resampling.LANCZOS)
        
        # Optimize to target 80-120 KB
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=85, optimize=True)
        size_kb = len(buf.getvalue()) / 1024
        
        if size_kb > 130:
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=75, optimize=True)
            size_kb = len(buf.getvalue()) / 1024
        elif size_kb < 80:
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=90, optimize=True)
            size_kb = len(buf.getvalue()) / 1024
            
        print(f"Uploading {item['target_name']} (Size: {size_kb:.1f} KB)...")
        
        upload_headers = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'image/jpeg',
            'Content-Disposition': f'attachment; filename="{item["target_name"]}"'
        }
        
        r = requests.post(
            'https://hosseinykala.ir/wp-json/wp/v2/media',
            auth=AUTH,
            headers=upload_headers,
            data=buf.getvalue(),
            timeout=30
        )
        
        if r.status_code in [200, 201]:
            data = r.json()
            m_id = data.get('id')
            media_ids[item['target_name']] = m_id
            print(f"  [SUCCESS] Media ID: {m_id}, URL: {data.get('source_url')}")
            
            # Set Alt and Title
            requests.post(
                f'https://hosseinykala.ir/wp-json/wp/v2/media/{m_id}',
                auth=AUTH,
                json={'alt_text': item['alt'], 'title': item['title']},
                timeout=15
            )
        else:
            print(f"  [FAIL] Status {r.status_code}: {r.text[:150]}")

    print("\nFinal Uploaded Media IDs:")
    import json
    print(json.dumps(media_ids, indent=2))
    return media_ids

if __name__ == '__main__':
    upload_all()
