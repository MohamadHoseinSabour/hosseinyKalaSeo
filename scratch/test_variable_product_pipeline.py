import os
import sys
import io
import time
import json
import requests
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

def upload_image(file_path, title, alt_text):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Image not found: {file_path}")
    img = Image.open(file_path).convert('RGB')
    max_dim = 1200
    w, h = img.size
    if w > max_dim or h > max_dim:
        scale = max_dim / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=85, optimize=True)
    img_bytes = buf.getvalue()
    filename = os.path.basename(file_path)
    if not filename.lower().endswith(('.jpg', '.jpeg')):
        filename = os.path.splitext(filename)[0] + '.jpg'
    upload_headers = {
        'User-Agent': HEADERS['User-Agent'],
        'Content-Type': 'image/jpeg',
        'Content-Disposition': f'attachment; filename="{filename}"'
    }
    r = requests.post(
        'https://hosseinykala.ir/wp-json/wp/v2/media',
        auth=AUTH,
        headers=upload_headers,
        data=img_bytes,
        timeout=45
    )
    if r.status_code in [200, 201]:
        data = r.json()
        media_id = data.get('id')
        requests.post(
            f'https://hosseinykala.ir/wp-json/wp/v2/media/{media_id}',
            auth=AUTH,
            headers=HEADERS,
            json={'alt_text': alt_text, 'title': title},
            timeout=15
        )
        return media_id
    raise Exception(f"Failed to upload: {r.status_code}")

# Test variable product
img_path = 'product_images_2026-10-05/beverage_makers/کتری برقی ساپر مدل 1031/hzdWyjIz_ukeNHuL.jpg'
media_id = upload_image(img_path, 'کتری برقی ساپر مدل 1031', 'کتری برقی ساپر مدل 1031 حسینی کالا')

parent_payload = {
    'name': 'کتری برقی ساپر مدل 1031',
    'slug': 'saper-1031-electric-kettle',
    'type': 'variable',
    'status': 'publish',
    'catalog_visibility': 'visible',
    'manage_stock': False,
    'stock_status': 'outofstock',
    'categories': [{'id': 240}],
    'images': [{'id': media_id}],
    'attributes': [
        {
            'name': 'رنگ',
            'position': 0,
            'visible': True,
            'variation': True,
            'options': ['سبز', 'کرم']
        }
    ],
    'short_description': """<ul>
<li><strong>توان دستگاه:</strong> توان گرمایشی ۱۸۵۰ تا ۲۲۰۰ وات جهت جوش‌آوری فوق‌العاده سریع</li>
<li><strong>گنجایش کتری:</strong> ۱.۷ لیتر، مناسب مصرف روزانه خانواده و پذیرایی</li>
<li><strong>جنس بدنه:</strong> استیل ضدزنگ و پلاستیک باکیفیت بهداشتی فاقد BPA</li>
<li><strong>سیستم ایمنی:</strong> قطع‌کن خودکار پس از جوش آمدن و محافظت در برابر کارکرد خشک</li>
<li><strong>رنگ‌بندی:</strong> عرضه شده در دو رنگ جذاب سبز پاستلی و کرم کلاسیک</li>
</ul>""",
    'description': """<h2>بررسی تخصصی کتری برقی ساپر مدل 1031</h2>
<p>یک فنجان چای یا قهوه فوری در آغاز روز نباید معطل جوش آمدن آب بماند. <strong>کتری برقی ساپر مدل 1031</strong> با ترکیب طراحی کلاسیک و توان ۲۲۰۰ واتی، آب را در کمتر از چند دقیقه به نقطه جوش می‌رساند. این مدل با گنجایش ۱.۷ لیتری انتخابی عالی برای مصارف خانگی و محیط‌های کاری است.</p>

<h2>جدول مشخصات فنی کتری ساپر 1031</h2>
<table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
  <tbody>
    <tr style="background-color: #f8f9fa;"><td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">برند</td><td style="padding: 10px; border: 1px solid #ddd;">ساپر (Saper)</td></tr>
    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">مدل</td><td style="padding: 10px; border: 1px solid #ddd;">1031</td></tr>
    <tr style="background-color: #f8f9fa;"><td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">توان مصرفی</td><td style="padding: 10px; border: 1px solid #ddd;">۱۸۵۰ - ۲۲۰۰ وات</td></tr>
    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">ظرفیت مخزن</td><td style="padding: 10px; border: 1px solid #ddd;">۱.۷ لیتر</td></tr>
    <tr style="background-color: #f8f9fa;"><td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">پایه ۳۶۰ درجه</td><td style="padding: 10px; border: 1px solid #ddd;">دارد (چرخش بدون سیم)</td></tr>
  </tbody>
</table>

<h2>ویژگی‌ها و نقاط قوت</h2>
<p>المنت پنهان استیل کتری مانع از تجمع سریع رسوب شده و تمیزکاری دیواره‌ها را فوق‌العاده ساده می‌کند. نشانگر شفاف سطح آب و قطع‌کن ایمنی اتوماتیک از گرم شدن بدون آب جلوگیری می‌نماید.</p>

<h2>خرید و ضمانت از حسینی کالا</h2>
<p>شما می‌توانید برای بررسی سایر کالاها به بخش <a href="https://hosseinykala.ir/product-category/drink-makers/">نوشیدنی ساز</a> حسینی کالا سر بزنید. همچنین <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> اهواز اصالت تمامی کالاها را با بهترین قیمت و ارسال سریع تضمین می‌کند.</p>"""
}

print("Creating variable parent product...")
r_par = requests.post('https://hosseinykala.ir/wp-json/wc/v3/products', auth=AUTH, headers=HEADERS, json=parent_payload, timeout=60)
print("Parent status:", r_par.status_code)
if r_par.status_code in [200, 201]:
    par_data = r_par.json()
    parent_id = par_data.get('id')
    print(f"Parent created successfully! ID: {parent_id}")
    
    # Create variations
    vars_to_create = [
        {'name': 'رنگ', 'option': 'سبز'},
        {'name': 'رنگ', 'option': 'کرم'}
    ]
    
    for v in vars_to_create:
        var_payload = {
            'stock_status': 'outofstock',
            'manage_stock': False,
            'attributes': [{'name': v['name'], 'option': v['option']}]
        }
        r_var = requests.post(f'https://hosseinykala.ir/wp-json/wc/v3/products/{parent_id}/variations', auth=AUTH, headers=HEADERS, json=var_payload, timeout=30)
        print(f"Variation {v['option']} status: {r_var.status_code}, ID: {r_var.json().get('id')}")
        
    # Verify live page
    r_live = requests.get(f'https://hosseinykala.ir/product/{parent_payload["slug"]}/', headers=HEADERS, timeout=30)
    print(f"Live page status: {r_live.status_code}")
else:
    print("Error creating parent:", r_par.text[:300])
