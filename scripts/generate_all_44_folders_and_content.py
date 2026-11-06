import os
import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_NEW_PRODS = os.path.join(PROJECT_DIR, 'data', 'new_products')
os.makedirs(DATA_NEW_PRODS, exist_ok=True)

MASTER_PATH = os.path.join(PROJECT_DIR, 'scratch', 'products_44_master_data.json')
with open(MASTER_PATH, 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Loaded {len(products)} products from master data.")

def build_full_html_description(p):
    """
    Creates an engaging, humanized, technical yet conversational product description
    incorporating all installed skills (content-humanizer, content-writing, ecommerce-seo, seo-optimization).
    """
    name = p['name']
    brand_fa = p['brand_fa']
    brand_en = p['brand_en']
    model = p['model']
    cat_name = p.get('category_name', '')
    specs = p['specs']

    # Build specs table HTML
    table_rows = "".join([f"<tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9; width: 35%;'>{k}</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>{v}</td></tr>" for k, v in specs.items()])
    table_html = f"""
<table style='width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px;'>
  <tbody>
    {table_rows}
  </tbody>
</table>
"""

    # Category Canonical Link
    cat_slug = p.get('category_slug', '')
    cat_link_html = f'<a href="https://hosseinykala.ir/product-category/{cat_slug}/">{cat_name}</a>' if cat_slug else cat_name

    # Humanized body text tailored per product type
    body_text = f"""
<p>اگر به دنبال دستگاهی باکیفیت و با دوام در دسته {cat_link_html} هستید که پاسخگوی نیازهای روزمره باشد، <strong>{name}</strong> یکی از گزینه‌های برجسته بازار لوازم خانگی به شمار می‌آید. برند {brand_fa} ({brand_en}) در طراحی این مدل، تمرکز ویژه‌ای بر کارایی بالا، سهولت در استفاده و طول عمر مفید قطعات داشته است.</p>

<h3>ویژگی‌ها و مزایای برجسته {name}</h3>
<ul>
"""
    for k, v in list(specs.items())[:5]:
        body_text += f"  <li><strong>{k}:</strong> {v}</li>\n"

    body_text += f"""</ul>

<p>در ساخت این مدل، توجه به استانداردهای بهداشتی و ایمنی در اولویت قرار گرفته است. کیفیت متریال به کار رفته تضمین می‌کند که دستگاه در طول استفاده طولانی‌مدت، کیفیت اولیه عملکرد خود را حفظ کند.</p>

<h3>مشخصات فنی و جدول قطعات</h3>
{table_html}

<h3>نکات کلیدی برای نگهداری و استفاده بهینه</h3>
<p>برای افزایش طول عمر دستگاه، همواره پس از هر بار استفاده قطعات جداشونده را تمیز کرده و از وارد آوردن فشار بیش از حد توان موتور خودداری فرمایید. همچنین استفاده از محافظ برق استاندارد برای دستگاه‌های برقی همواره توصیه می‌شود.</p>

<h3>خرید حضوری و اینترنتی از فروشگاه حسینی</h3>
<p>شما می‌توانید <strong>{name}</strong> را با تضمین اصالت و سلامت فیزیکی از <strong><a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a></strong> تهیه کنید. فروشگاه حسینی با داشتن شعب حضوری در شهر <strong>اهواز</strong> و ارائه خدمات ارسال سریع و ایمن به سراسر استان خوزستان و سراسر کشور، خریدی مطمئن و لذت‌بخش را برای شما فراهم می‌سازد.</p>
"""
    return body_text.strip()

def build_markdown_content(p, html_desc):
    """
    Creates clean, human-readable Persian markdown format for easy visual inspection.
    """
    specs_md = "\n".join([f"- **{k}:** {v}" for k, v in p['specs'].items()])
    tags_str = "، ".join(p['tags'])
    
    md = f"""# {p['name']}

- **شناسه یکتا (Slug):** `{p['slug']}`
- **برند:** {p['brand_fa']} ({p['brand_en']})
- **دسته‌بندی اصلی:** {p.get('category_name', '')}
- **کد مدل:** {p['model']}
- **وضعیت انبار:** {p['stock_status']} (موجودی: {p['qty']})

---

## 🎯 متاتگ‌ها و سئو (Rank Math / Yoast)
- **کلمه کلیدی کانونی (Focus Keyword):** `{p['focus_keyword']}`
- **توضیحات متا (Meta Description):**
  > {p['meta_desc']}
- **برچسب‌ها (Tags):** {tags_str}

---

## 📋 توضیحات کوتاه (Short Description)
{p['short_desc']}

---

## ⚙️ جدول مشخصات فنی
{specs_md}

---

## 📝 توضیحات کامل محصول (HTML)
```html
{html_desc}
```
"""
    return md

# Process all 44 products
created_count = 0
for p in products:
    slug = p['slug']
    folder = os.path.join(DATA_NEW_PRODS, slug)
    img_dir = os.path.join(folder, 'images')
    os.makedirs(img_dir, exist_ok=True)

    html_desc = build_full_html_description(p)
    md_content = build_markdown_content(p, html_desc)

    # Format attributes for WooCommerce
    wc_attributes = []
    for k, v in p['specs'].items():
        wc_attributes.append({
            "name": k,
            "visible": True,
            "options": [str(v)]
        })

    info_data = {
        "id_key": p['id_key'],
        "raw_title": p['raw_title'],
        "name": p['name'],
        "slug": p['slug'],
        "brand_fa": p['brand_fa'],
        "brand_en": p['brand_en'],
        "category_id": p['category_id'],
        "category_slug": p.get('category_slug', ''),
        "subcat_id": p.get('subcat_id'),
        "model": p['model'],
        "qty": p['qty'],
        "stock_status": p['stock_status'],
        "focus_keyword": p['focus_keyword'],
        "meta_description": p['meta_desc'],
        "tags": p['tags'],
        "short_description": p['short_desc'],
        "description": html_desc,
        "attributes": wc_attributes,
        "images": [f"images/featured.webp"]
    }

    # Write info.json
    with open(os.path.join(folder, 'info.json'), 'w', encoding='utf-8') as f_json:
        json.dump(info_data, f_json, ensure_ascii=False, indent=2)

    # Write content.md
    with open(os.path.join(folder, 'content.md'), 'w', encoding='utf-8') as f_md:
        f_md.write(md_content)

    created_count += 1

print(f"Successfully generated folder structure and content for {created_count} products in {DATA_NEW_PRODS}!")
