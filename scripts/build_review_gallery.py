import os
import sys
import json
import base64

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_NEW_PRODS = os.path.join(PROJECT_DIR, 'data', 'new_products')
OUT_HTML = os.path.join(PROJECT_DIR, 'scratch', 'new_products_review_gallery.html')

folders = [f for f in os.listdir(DATA_NEW_PRODS) if os.path.isdir(os.path.join(DATA_NEW_PRODS, f))]
print(f"Scanning {len(folders)} product folders...")

products_data = []
for folder_name in sorted(folders):
    info_file = os.path.join(DATA_NEW_PRODS, folder_name, 'info.json')
    if os.path.exists(info_file):
        with open(info_file, 'r', encoding='utf-8') as f:
            p = json.load(f)
            
        img_path = os.path.join(DATA_NEW_PRODS, folder_name, 'images', 'featured.webp')
        img_exists = os.path.exists(img_path) and os.path.getsize(img_path) > 1000
        p['has_image'] = img_exists
        p['img_size_kb'] = (os.path.getsize(img_path) / 1024) if img_exists else 0
        p['img_rel_path'] = f"../data/new_products/{folder_name}/images/featured.webp" if img_exists else ""
        
        # Base64 data URI for inline display in standalone HTML
        if img_exists:
            with open(img_path, 'rb') as f_img:
                b64 = base64.b64encode(f_img.read()).decode('utf-8')
                p['img_data_uri'] = f"data:image/webp;base64,{b64}"
        else:
            p['img_data_uri'] = ""
            
        products_data.append(p)

# Build HTML Gallery
cards_html = ""
for idx, p in enumerate(products_data):
    img_html = f"<img src='{p['img_data_uri']}' alt='{p['name']}' style='max-width: 100%; max-height: 240px; object-fit: contain; border-radius: 8px;' />" if p['has_image'] else "<div style='height: 200px; display: flex; align-items: center; justify-content: center; background: #f0f0f0; color: #999; border-radius: 8px;'>تصویر در دست تامین</div>"
    
    img_badge = f"<span style='background: #d4edda; color: #155724; padding: 4px 8px; border-radius: 4px; font-size: 12px;'>✓ عکس آماده ({p['img_size_kb']:.1f} KB)</span>" if p['has_image'] else "<span style='background: #f8d7da; color: #721c24; padding: 4px 8px; border-radius: 4px; font-size: 12px;'>✗ فاقد عکس</span>"
    
    attrs_html = "".join([f"<li style='margin-bottom: 4px;'><strong>{a['name']}:</strong> {', '.join(a['options'])}</li>" for a in p['attributes'][:6]])
    
    cards_html += f"""
    <div style='background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin-bottom: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);'>
      <div style='display: flex; gap: 24px; flex-wrap: wrap;'>
        <div style='flex: 0 0 260px; text-align: center; background: #fafafa; padding: 12px; border-radius: 8px; border: 1px solid #eee;'>
          {img_html}
          <div style='margin-top: 10px;'>{img_badge}</div>
        </div>
        <div style='flex: 1; min-width: 320px;'>
          <div style='display: flex; justify-content: space-between; align-items: center;'>
            <span style='background: #ebf1f5; color: #1f4e79; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: bold;'>محصول #{idx+1} | {p['category_slug']}</span>
            <span style='color: #666; font-size: 13px;'>موجودی انبار: <strong>{p['qty']} عدد</strong> ({p['stock_status']})</span>
          </div>
          <h2 style='font-size: 18px; color: #1a202c; margin: 10px 0 6px 0;'>{p['name']}</h2>
          <div style='color: #718096; font-size: 13px; font-family: monospace; direction: ltr; text-align: right; margin-bottom: 12px;'>Slug: <strong>{p['slug']}</strong></div>
          
          <div style='background: #f8fafc; border-right: 4px solid #3182ce; padding: 10px 14px; margin-bottom: 12px; font-size: 13px; color: #4a5568;'>
            <strong>توضیحات متا (Google SERP):</strong> {p['meta_description']}
          </div>

          <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 16px; font-size: 13px;'>
            <div>
              <h4 style='margin: 0 0 6px 0; color: #2d3748;'>ویژگی‌های کوتاه:</h4>
              {p['short_description']}
            </div>
            <div>
              <h4 style='margin: 0 0 6px 0; color: #2d3748;'>مشخصات فنی کلیدی:</h4>
              <ul style='margin: 0; padding-right: 20px; color: #4a5568;'>
                {attrs_html}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
    """

total_images = sum(1 for p in products_data if p['has_image'])

html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>گالری ممیزی و پیش‌نمایش ۴۴ محصول جدید — فروشگاه لوازم خانگی حسینی</title>
  <style>
    body {{
      font-family: Tahoma, 'Segoe UI', Arial, sans-serif;
      background: #f1f5f9;
      color: #333;
      margin: 0;
      padding: 30px;
      line-height: 1.6;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
    }}
    .header {{
      background: #1f4e79;
      color: #fff;
      padding: 24px 30px;
      border-radius: 12px;
      margin-bottom: 30px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div>
        <h1 style="margin: 0 0 6px 0; font-size: 22px;">گالری بازبینی و ممیزی ۴۴ محصول جدید انبار</h1>
        <div style="font-size: 14px; opacity: 0.9;">فروشگاه لوازم خانگی حسینی — بررسی تصاویر، عناوین سئو و مشخصات فنی پیش از انتشار در سایت</div>
      </div>
      <div style="text-align: left; background: rgba(255,255,255,0.15); padding: 10px 18px; border-radius: 8px;">
        <div style="font-size: 20px; font-weight: bold;">{total_images} / {len(products_data)}</div>
        <div style="font-size: 12px;">تصاویر تامین‌شده</div>
      </div>
    </div>

    {cards_html}

  </div>
</body>
</html>
"""

with open(OUT_HTML, 'w', encoding='utf-8') as f_out:
    f_out.write(html)

print(f"Generated review gallery at {OUT_HTML} with {total_images}/{len(products_data)} images!")
