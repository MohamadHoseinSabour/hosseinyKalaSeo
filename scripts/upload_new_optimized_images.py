import os
import sys
import io
import time
import requests
from PIL import Image

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
BRAIN_DIR = r'C:\Users\mmhhs\.gemini\antigravity\brain\5af16dc4-2462-419a-b5e9-e6648d6bd5d0'

IMAGES_TO_UPLOAD = [
    {
        'post_id': 3214,
        'src_file': 'purifier_ref_cover_1787225273235.jpg',
        'target_name': 'home-water-purifier-buying-guide.jpg',
        'title': 'راهنمای خرید دستگاه تصفیه آب خانگی',
        'alt': 'راهنمای خرید دستگاه تصفیه آب خانگی سافت واتر'
    },
    {
        'post_id': 3215,
        'src_file': 'depoint_ref_cover_1787225285388.jpg',
        'target_name': 'depoint-refrigerator-brand-review.jpg',
        'title': 'بررسی تخصصی برند دیپوینت',
        'alt': 'بررسی تخصصی و کیفیت یخچال فریزر دیپوینت'
    },
    {
        'post_id': 3217,
        'src_file': 'air_fryer_ref_cover_1787225386534.jpg',
        'target_name': 'air-fryer-buying-guide.jpg',
        'title': 'راهنمای خرید سرخ کن بدون روغن ایرفرایر',
        'alt': 'راهنمای خرید سرخ کن بدون روغن ایرفرایر دونالکس'
    },
    {
        'post_id': 3218,
        'src_file': 'espresso_pure_ref_cover_1787225471125.jpg',
        'target_name': 'home-espresso-maker-buying-guide.jpg',
        'title': 'راهنمای خرید اسپرسوساز خانگی',
        'alt': 'راهنمای خرید اسپرسوساز خانگی دونالکس'
    },
    {
        'post_id': 3219,
        'src_file': 'hair_clipper_pure_1787223607304.jpg',
        'target_name': 'hair-clipper-buying-guide.jpg',
        'title': 'راهنمای خرید ماشین اصلاح موی سر و صورت',
        'alt': 'راهنمای خرید ماشین اصلاح موی سر و صورت پرو امگا'
    },
    {
        'post_id': 3220,
        'src_file': 'appliances_protection_1787223579171.jpg',
        'target_name': 'home-appliances-maintenance-khuzestan.jpg',
        'title': 'محافظت از لوازم خانگی در برابر نوسان برق و گرما',
        'alt': 'محافظت و نگهداری از لوازم خانگی برقی در خوزستان'
    }
]

def safe_post(url, **kwargs):
    for attempt in range(4):
        try:
            return requests.post(url, **kwargs)
        except Exception as e:
            print(f"    [Retry {attempt+1}/4] {e}")
            time.sleep(3)
    return None

def compress_and_upload():
    print("=== Compressing Images to Low File Size (50-80 KB) and Uploading to WP ===")
    
    for item in IMAGES_TO_UPLOAD:
        src_path = os.path.join(BRAIN_DIR, item['src_file'])
        if not os.path.exists(src_path):
            print(f"File not found: {src_path}")
            continue

        img = Image.open(src_path).convert('RGB')
        img = img.resize((1599, 900), Image.Resampling.LANCZOS)
        
        # Iterative compression to hit 55-80 KB
        quality = 70
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=quality, optimize=True)
        size_kb = len(buf.getvalue()) / 1024
        
        while size_kb > 80 and quality > 35:
            quality -= 5
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=quality, optimize=True)
            size_kb = len(buf.getvalue()) / 1024

        print(f"\nProcessing {item['target_name']}:")
        print(f"  Dimensions: 1599x900 | Final Size: {size_kb:.1f} KB (Quality: {quality})")
        
        upload_headers = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'image/jpeg',
            'Content-Disposition': f'attachment; filename="{item["target_name"]}"'
        }
        
        # Upload media with safe_post
        r = safe_post(
            'https://hosseinykala.ir/wp-json/wp/v2/media',
            auth=AUTH,
            headers=upload_headers,
            data=buf.getvalue(),
            timeout=35
        )
        
        if r and r.status_code in [200, 201]:
            media_data = r.json()
            media_id = media_data.get('id')
            source_url = media_data.get('source_url')
            print(f"  [UPLOAD OK] Media ID: {media_id} | URL: {source_url}")
            
            # Set Alt text and Title
            safe_post(
                f'https://hosseinykala.ir/wp-json/wp/v2/media/{media_id}',
                auth=AUTH,
                json={'alt_text': item['alt'], 'title': item['title']},
                timeout=20
            )
            
            # Update post's featured_media
            post_update_url = f"https://hosseinykala.ir/wp-json/wp/v2/posts/{item['post_id']}"
            r_post = safe_post(
                post_update_url,
                auth=AUTH,
                headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
                json={'featured_media': media_id},
                timeout=20
            )
            if r_post and r_post.status_code == 200:
                print(f"  [POST UPDATED] Post {item['post_id']} featured_media set to {media_id}")
            else:
                print(f"  [POST UPDATE FAIL] Post {item['post_id']}: HTTP {r_post.status_code if r_post else 'No Resp'}")
        else:
            print(f"  [UPLOAD FAIL] HTTP {r.status_code if r else 'No Resp'}")
            
        time.sleep(1)

if __name__ == '__main__':
    compress_and_upload()
