import os
import io
import time
import requests
from PIL import Image

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
BRAIN_DIR = r'C:\Users\mmhhs\.gemini\antigravity\brain\a254ee85-ba68-4053-b5cb-81ee7084ef3f'

IMAGES = [
    {
        'file': 'refah_beta_cover_1789795362674.jpg',
        'target_slug': 'refah-bank-beta-installment-guide',
        'title': 'راهنمای طرح بتا بانک رفاه برای بازنشستگان',
        'alt': 'خرید اقساطی لوازم خانگی با طرح بتا بانک رفاه برای بازنشستگان تأمین اجتماعی'
    },
    {
        'file': 'bajet_appliances_cover_1789795377843.jpg',
        'target_slug': 'bajet-tejarat-refah-300m-appliances',
        'title': 'خرید اقساطی با طرح باجت و کارت رفاهی ۳۰۰ میلیونی',
        'alt': 'طرح باجت کالانو بانک تجارت و کارت رفاهی خرید لوازم خانگی تا ۳۰۰ میلیون'
    },
    {
        'file': 'mellat_loan_cover_1789795394493.jpg',
        'target_slug': 'mellat-bank-200m-appliances-loan-guide',
        'title': 'وام ۲۰۰ میلیونی خرید لوازم خانگی بانک ملت',
        'alt': 'راهنمای دریافت وام ۲۰۰ میلیونی خرید لوازم خانگی بانک ملت فرابانک و حامی کارت'
    },
    {
        'file': 'sayadi_cheque_cover_1789795414139.jpg',
        'target_slug': 'sayadi-cheque-installment-buying-guide',
        'title': 'خرید اقساطی لوازم خانگی با چک صیادی در اهواز',
        'alt': 'شرایط خرید اقساطی لوازم خانگی با چک صیادی در اهواز فروشگاه حسینی کالا'
    },
    {
        'file': 'mehr_bnpl_cover_1789795433300.jpg',
        'target_slug': 'mehr-iran-kalacard-bnpl-appliances-guide',
        'title': 'کالا کارت مهر ایران و روش های خرید اقساطی BNPL',
        'alt': 'مقایسه کالا کارت قرض الحسنه مهر ایران و روش های قسطی اسنپ پی و دیجی پی'
    }
]

def upload_all():
    results = {'home-appliances-installment-buying-guide': 3845}
    for item in IMAGES:
        src_path = os.path.join(BRAIN_DIR, item['file'])
        if not os.path.exists(src_path):
            print(f"File not found: {src_path}")
            continue

        img = Image.open(src_path).convert('RGB')
        img = img.resize((1599, 900), Image.Resampling.LANCZOS)

        # Optimize targeting 90-110 KB
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=82, optimize=True)
        size_kb = len(buf.getvalue()) / 1024
        if size_kb > 120:
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=74, optimize=True)
            size_kb = len(buf.getvalue()) / 1024
        elif size_kb < 80:
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=88, optimize=True)
            size_kb = len(buf.getvalue()) / 1024

        print(f"Uploading {item['target_slug']}.jpg (Size: {size_kb:.1f} KB)...")
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'image/jpeg',
            'Content-Disposition': f'attachment; filename="{item["target_slug"]}.jpg"'
        }
        r = requests.post(
            'https://hosseinykala.ir/wp-json/wp/v2/media',
            auth=AUTH,
            headers=headers,
            data=buf.getvalue(),
            timeout=30
        )
        if r.status_code in [200, 201]:
            m_id = r.json().get('id')
            results[item['target_slug']] = m_id
            print(f"  [SUCCESS] Media ID: {m_id}")
            requests.post(
                f'https://hosseinykala.ir/wp-json/wp/v2/media/{m_id}',
                auth=AUTH,
                json={'alt_text': item['alt'], 'title': item['title']}
            )
        else:
            print(f"  [FAIL] HTTP {r.status_code}: {r.text[:150]}")
        time.sleep(1)

    print("\nAll Media IDs:")
    import json
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    upload_all()
