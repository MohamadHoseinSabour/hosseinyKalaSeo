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
    """Resizes, optimizes, and uploads an image to WordPress Media Library."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Image not found: {file_path}")
        
    img = Image.open(file_path).convert('RGB')
    # Resize if larger than 1200x1200
    max_dim = 1200
    w, h = img.size
    if w > max_dim or h > max_dim:
        scale = max_dim / max(w, h)
        new_w, new_h = int(w * scale), int(h * scale)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
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
        media_url = data.get('source_url')
        print(f"  ✓ Image uploaded successfully: ID {media_id} ({len(img_bytes)/1024:.1f} KB)")
        
        # Set alt text & title
        try:
            requests.post(
                f'https://hosseinykala.ir/wp-json/wp/v2/media/{media_id}',
                auth=AUTH,
                headers=HEADERS,
                json={'alt_text': alt_text, 'title': title},
                timeout=15
            )
        except Exception as e:
            print(f"  Warning: failed to update alt text: {e}")
            
        return media_id, media_url
    else:
        raise Exception(f"Failed to upload image {filename}: Status {r.status_code} - {r.text[:200]}")

# Test on Kenwood hand mixer HM430
test_prod = {
    'name': 'همزن برقی کنوود مدل HM430',
    'slug': 'kenwood-hm430-hand-mixer',
    'type': 'simple',
    'category_ids': [240],
    'primary_cat_name': 'نوشیدنی ساز',
    'primary_cat_url': 'https://hosseinykala.ir/product-category/drink-makers/',
    'image_path': 'product_images_2026-10-05/beverage_makers/kenwood-hm430-hand-mixer.jpg',
    'short_desc': """<ul>
<li><strong>توان مصرفی موتور:</strong> موتور بهینه ۴۰۰ وات قدرتمند با قابلیت توربو (Turbo)</li>
<li><strong>تعداد سرعت:</strong> تنظیم در ۵ سطح سرعت مختلف متناسب با انواع خمیر و کرم</li>
<li><strong>سری‌ها:</strong> مجهز به دو پره همزن استیل ضدزنگ و دو قلاب خمیرزن مقاوم</li>
<li><strong>طراحی ارگونومیک:</strong> بدنه سبک و خوش‌دست با سیستم خنک‌کننده هوشمند موتور</li>
<li><strong>گارانتی و اصالت:</strong> ضمانت اصالت ۱۰۰٪ کالا از فروشگاه لوازم خانگی حسینی</li>
</ul>
<p>اگر برای پخت کیک، شیرینی‌پزی خانگی و آماده‌سازی انواع دسر به دنبال همزنی پرقدرت و بادوام هستید، همزن کنوود HM430 انتخابی مطمئن و خوش‌دست برای آشپزخانه شماست.</p>""",
    'full_desc': """<h2>بررسی تخصصی همزن برقی کنوود مدل HM430</h2>
<p>پخت یک کیک اسفنجی خوش‌بافت یا هم زدن خامه قنادی به ابزاری نیاز دارد که در کارکرد مداوم کم نیاورد و دست را خسته نکند. <strong>همزن برقی کنوود مدل HM430</strong> یکی از دستیارهای همیشگی و قابل اعتماد در آشپزخانه‌های ایرانی است که با موتور ۴۰۰ وات واقعی، ۵ حالت تنظیم سرعت و طراحی ارگونومیک ساخته شده است. این دستگاه به راحتی از پس مخلوط کردن تخم‌مرغ تا ورز دادن خمیرهای سبک برمی‌آید.</p>

<h2>جدول مشخصات فنی همزن کنوود HM430</h2>
<table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
  <tbody>
    <tr style="background-color: #f8f9fa;">
      <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">برند و سازنده</td>
      <td style="padding: 10px; border: 1px solid #ddd;">کنوود (Kenwood)</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">مدل دستگاه</td>
      <td style="padding: 10px; border: 1px solid #ddd;">HM430</td>
    </tr>
    <tr style="background-color: #f8f9fa;">
      <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">توان مصرفی موتور</td>
      <td style="padding: 10px; border: 1px solid #ddd;">۴۰۰ وات واقعی با حالت توربو</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">تعداد تنظیمات سرعت</td>
      <td style="padding: 10px; border: 1px solid #ddd;">۵ سرعت متغیر</td>
    </tr>
    <tr style="background-color: #f8f9fa;">
      <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">جنس پره‌ها و قلاب‌ها</td>
      <td style="padding: 10px; border: 1px solid #ddd;">استیل ضدزنگ با مقاومت بالا در برابر رطوبت</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">قابلیت شستشوی قطعات</td>
      <td style="padding: 10px; border: 1px solid #ddd;">پره‌ها قابل شستشو در ماشین ظرفشویی</td>
    </tr>
  </tbody>
</table>

<h2>ویژگی‌ها و مزایای برجسته برای آشپزی روزمره</h2>
<p>موتور ۴۰۰ واتی کنوود نسبت به جثه جمع‌وجورش گشتاور بسیار خوبی تولید می‌کند. دکمه خروج پره‌ها (Eject) تعویض سری‌ها را کاملاً ایمن و بدون کثیف شدن دست‌ها ممکن می‌سازد. همچنین به لطف طراحی بالانس دستگیره، حتی در بالاترین سرعت لرزش آزاردهنده‌ای به مچ دست منتقل نمی‌شود.</p>

<h2>نکات استفاده و افزایش طول عمر دستگاه</h2>
<p>هنگام هم زدن مواد سفت مانند خمیر نان غلیظ، سرعت را از درجه‌های پایین شروع کنید تا به چرخ‌دنده‌ها فشار نیاید. پس از هر چند دقیقه کار مداوم، ۳۰ ثانیه به موتور استراحت دهید تا جریان هوای داخلی حرارت سیم‌پیچ را دفع کند.</p>

<h2>خرید و ضمانت اصالت کالا</h2>
<p>شما می‌توانید برای بررسی و خرید سایر محصولات آشپزخانه به بخش <a href="https://hosseinykala.ir/product-category/drink-makers/">نوشیدنی ساز</a> حسینی کالا مراجعه فرمایید. <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> با شعب فعال در شهر <strong>اهواز</strong>، ضمانت اصالت ۱۰۰ درصدی کلیه کالاها و ارسال مطمئن به سراسر کشور را تضمین می‌نماید.</p>"""
}

print(f"Starting test pipeline for: {test_prod['name']}")
print("Step 1: Uploading image...")
media_id, media_url = upload_image(
    test_prod['image_path'],
    title=f"خرید و قیمت {test_prod['name']}",
    alt_text=f"همزن برقی کنوود HM430 - فروشگاه لوازم خانگی حسینی اهواز"
)

print("\nStep 2: Creating product via WooCommerce REST API...")
payload = {
    'name': test_prod['name'],
    'slug': test_prod['slug'],
    'type': 'simple',
    'status': 'publish',
    'catalog_visibility': 'visible',
    'manage_stock': False,
    'stock_status': 'outofstock',
    'categories': [{'id': cid} for cid in test_prod['category_ids']],
    'images': [{'id': media_id}],
    'short_description': test_prod['short_desc'],
    'description': test_prod['full_desc']
}

r_prod = requests.post(
    'https://hosseinykala.ir/wp-json/wc/v3/products',
    auth=AUTH,
    headers=HEADERS,
    json=payload,
    timeout=60
)

print(f"Product creation status: {r_prod.status_code}")
if r_prod.status_code in [200, 201]:
    prod_data = r_prod.json()
    new_pid = prod_data.get('id')
    created_slug = prod_data.get('slug')
    permalink = prod_data.get('permalink')
    print(f"  ✓ SUCCESS! Created Product ID: {new_pid}")
    print(f"  ✓ Slug: {created_slug}")
    print(f"  ✓ Permalink: {permalink}")
    print(f"  ✓ Stock status: {prod_data.get('stock_status')}")
    
    # Step 3: Verify live page
    print("\nStep 3: Verifying live product page...")
    r_live = requests.get(permalink, headers=HEADERS, timeout=30)
    print(f"  Live HTTP Status: {r_live.status_code}")
    if r_live.status_code == 200:
        print("  ✓ Live page loaded successfully (200 OK)!")
else:
    print(f"  Error: {r_prod.text[:300]}")
