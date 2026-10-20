import os
import sys
import json
import re
import requests
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

SHEET_FOLDER_MAP = {
    'یخچال و فریزر': 'refrigerators',
    'شستشو و نظافت': 'washing_and_cleaning',
    'لوازم برقی و پخت و پز': 'cooking_appliances',
    'نوشیدنی ساز': 'beverage_makers',
    'سرمایش و گرمایش': 'cooling_heating',
    'تصفیه کننده آب': 'water_purifiers',
    'زیبایی و سلامت فردی': 'beauty_health'
}

def clean_text(s):
    if not s:
        return ""
    return re.sub(r'[📂◀↳]', '', str(s)).strip()

def generate_english_slug(item):
    brand = item.get('brand') or ''
    name = item.get('name') or ''
    
    # Common mappings
    brand_map = {
        'هیمالیا': 'himalia',
        'کلور': 'clover',
        'دیپوینت': 'depoint',
        'الکترواستیل': 'electrosteel',
        'ایستکول': 'eastcool',
        'بست': 'bost',
        'تکنوسان': 'technosan',
        'ریگور': 'rigor',
        'نیکسان': 'niksan',
        'پارس خزر': 'parskhazar',
        'اسنوا': 'snowa',
        'دوو': 'daewoo',
        'آلتون': 'alton',
        'پاکشوما': 'pakshoma',
        'سران': 'saran',
        'سیماران': 'simaran',
        'فریدولین': 'feridolin',
        'پاکیزان': 'pakizan',
        'دونالکس': 'donalex',
        'ساپر': 'saper',
        'ویلز': 'willez',
        'زامروتی': 'zamrooti',
        'بوتان': 'butan',
        'پلار': 'polar',
        'پاناسونیک': 'panasonic',
        'پرومارون': 'promaron',
        'پروامگا': 'proomega',
        'وست واتر': 'westwater'
    }
    
    brand_en = brand_map.get(brand, 'brand')
    clean = clean_text(name).lower()
    
    # Model extraction
    tokens = []
    tokens.append(brand_en)
    
    # Extract model codes like 60MW, SG518, RF84102E2, DN-970, etc.
    model_match = re.findall(r'[a-zA-Z0-9]+-?[a-zA-Z0-9]+', name)
    for m in model_match:
        if len(m) >= 2 and not m.isdigit():
            tokens.append(m.lower())
            
    # Add key descriptors
    if 'دوقلو' in name:
        tokens.append('twin')
    elif 'کمبی' in name:
        tokens.append('combi')
    elif 'ساید' in name:
        tokens.append('side-by-side')
    elif 'صندوقی' in name:
        tokens.append('chest-freezer')
    elif 'هوم بار' in name or 'هومبار' in name:
        tokens.append('homebar')
    elif 'آبریز' in name:
        tokens.append('water-dispenser')
    elif 'جاروبرقی' in name:
        tokens.append('vacuum')
    elif 'لباسشویی' in name:
        tokens.append('washing-machine')
    elif 'سرخ کن' in name:
        tokens.append('airfryer')
    elif 'کتری' in name:
        tokens.append('kettle')
    elif 'اسپرسو' in name:
        tokens.append('espresso')
    elif 'پنکه' in name:
        tokens.append('fan')
    elif 'بخاری' in name:
        tokens.append('heater')
    elif 'آبگرمکن' in name:
        tokens.append('water-heater')
        
    # Color or variant
    if 'استیل' in name or 'سیلور' in name:
        tokens.append('steel')
    elif 'سفید' in name:
        tokens.append('white')
    elif 'مشکی' in name:
        tokens.append('black')
    elif 'تیتانیوم' in name:
        tokens.append('titanium')
        
    slug = '-'.join(dict.fromkeys(tokens))
    if len(tokens) <= 1:
        slug = f"{brand_en}-row-{item.get('row')}"
    return slug

def search_digikala_for_product(item):
    name = clean_text(item.get('name'))
    brand = item.get('brand') or ''
    parent_name = clean_text(item.get('parent_name')) if item.get('is_variation') else ''
    
    queries = []
    if parent_name:
        queries.append(f"{brand} {parent_name} {name}")
        queries.append(f"{brand} {parent_name}")
    else:
        # Extract model numbers if any
        model_codes = re.findall(r'[a-zA-Z0-9-]{3,}', name)
        if model_codes:
            queries.append(f"{brand} {' '.join(model_codes)}")
        queries.append(f"{brand} {name}")
        queries.append(name)
        
    candidates = []
    seen = set()
    
    for q in queries:
        try:
            url = "https://api.digikala.com/v1/search/"
            r = requests.get(url, params={'q': q}, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                products = r.json().get('data', {}).get('products', [])
                for p in products:
                    imgs = p.get('images', {}).get('main', {}).get('url', [])
                    if imgs:
                        raw_url = imgs[0].split('?')[0]
                        if raw_url not in seen:
                            seen.add(raw_url)
                            candidates.append({
                                'matched_id': p.get('id'),
                                'matched_title': p.get('title_fa'),
                                'query_used': q,
                                'image_url': raw_url
                            })
                    if len(candidates) >= 4:
                        break
        except Exception as e:
            pass
        if len(candidates) >= 4:
            break
            
    return candidates

def download_candidates_batch(items, max_per_item=3):
    results = []
    for item in items:
        sheet = item.get('sheet')
        sheet_folder = SHEET_FOLDER_MAP.get(sheet, 'misc')
        slug = generate_english_slug(item)
        target_dir = os.path.join('scratch', 'candidates', sheet_folder, slug)
        os.makedirs(target_dir, exist_ok=True)
        
        cands = search_digikala_for_product(item)
        downloaded = []
        
        for idx, c in enumerate(cands[:max_per_item], 1):
            dest = os.path.join(target_dir, f"cand_{idx}.jpg")
            try:
                r = requests.get(c['image_url'], headers=HEADERS, timeout=12)
                if r.status_code == 200 and len(r.content) > 5000:
                    with open(dest, 'wb') as f:
                        f.write(r.content)
                    img = Image.open(dest)
                    w, h = img.size
                    downloaded.append({
                        'index': idx,
                        'file_path': dest,
                        'width': w,
                        'height': h,
                        'matched_id': c['matched_id'],
                        'matched_title': c['matched_title'],
                        'query_used': c['query_used'],
                        'image_url': c['image_url']
                    })
            except Exception as e:
                pass
                
        results.append({
            'item': item,
            'slug': slug,
            'sheet_folder': sheet_folder,
            'candidates': downloaded
        })
        print(f"Processed: [{item.get('brand')}] {item.get('name')} -> {len(downloaded)} candidates staged")
    return results

if __name__ == '__main__':
    sheet_to_run = sys.argv[1] if len(sys.argv) > 1 else 'یخچال و فریزر'
    with open('scratch/missing_products.json', encoding='utf-8') as f:
        all_missing = json.load(f)
        
    filtered = [p for p in all_missing if p.get('sheet') == sheet_to_run]
    print(f"Starting batch search for sheet '{sheet_to_run}': {len(filtered)} items...")
    res = download_candidates_batch(filtered)
    out_file = f"scratch/candidates_summary_{sheet_to_run}.json".replace(' ', '_')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"Summary written to {out_file}")
