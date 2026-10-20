import os
import sys
import json
import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
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

BRAND_MAP = {
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
    'وست واتر': 'westwater',
    'هانو': 'hano',
    'لاوان': 'lavan',
    'اوریکس': 'oryx',
    'تفال': 'tefal',
    'جنرال': 'general',
    'رانکو': 'ranko',
    'سانی': 'sunny',
    'ونتو': 'vento',
    'وولگا': 'volga',
    'پروکس': 'prox',
    'ژمبو': 'jumbo',
    'کاستلو': 'castello',
    'کنوود': 'kenwood',
    'کورکماز': 'korkmaz',
    'گرنویک': 'grenwic',
    'وستینگهاوس': 'westinghouse',
    'الکترا': 'electra',
    'اوجنرال': 'ogeneral',
    'اوناکس': 'onax',
    'گلدن لوکس': 'goldenlux',
    'امگا': 'omega',
    'اویز': 'aviz',
    'اویزپلاس': 'avizplus',
    'نیاک': 'niak'
}

def clean_text(s):
    if not s:
        return ""
    return re.sub(r'[📂◀↳]', '', str(s)).strip()

def build_english_slug(item):
    brand = item.get('brand') or ''
    name = item.get('name') or ''
    parent_name = item.get('parent_name') or ''
    
    brand_en = BRAND_MAP.get(brand, 'item')
    tokens = [brand_en]
    
    # Model codes (e.g. 60MW, SG518, B3115, DN-970, RF84102E2, etc.)
    combined_name = f"{parent_name} {name}" if parent_name else name
    models = re.findall(r'[a-zA-Z0-9]+-?[a-zA-Z0-9]+', combined_name)
    for m in models:
        m_lower = m.lower()
        if len(m) >= 2 and not m.isdigit() and m_lower not in tokens:
            tokens.append(m_lower)
            
    # Key descriptors
    descriptors = [
        ('دوقلو', 'twin'),
        ('کمبی', 'combi'),
        ('صندوقی', 'chest-freezer'),
        ('فریزر', 'freezer'),
        ('یخچال', 'fridge'),
        ('هوم بار', 'homebar'),
        ('آبریز', 'water-dispenser'),
        ('اکونومی', 'economy'),
        ('روسو', 'rosso'),
        ('امگا', 'omega'),
        ('مینی', 'mini'),
        ('جاروبرقی', 'vacuum'),
        ('لباسشویی', 'washing-machine'),
        ('مینی واش', 'mini-wash'),
        ('پتوشور', 'blanket-washer'),
        ('اتو', 'iron'),
        ('سرخ کن', 'airfryer'),
        ('هواپز', 'airfryer'),
        ('غذاساز', 'food-processor'),
        ('ساندویچ ساز', 'sandwich-maker'),
        ('گاز صفحه ای', 'gas-hob'),
        ('فر توکار', 'built-in-oven'),
        ('فر گاز', 'gas-cooker'),
        ('هود', 'hood'),
        ('قابلمه', 'pot'),
        ('تابه', 'pan'),
        ('سرویس قابلمه', 'cookware-set'),
        ('خردکن', 'chopper'),
        ('چرخ گوشت', 'meat-grinder'),
        ('پلوپز', 'rice-cooker'),
        ('همزن', 'mixer'),
        ('اسپرسو', 'espresso'),
        ('کتری', 'kettle'),
        ('چای ساز', 'tea-maker'),
        ('مخلوط کن', 'blender'),
        ('آسیاب', 'grinder'),
        ('آبسردکن', 'water-dispenser'),
        ('تصفیه آب', 'water-purifier'),
        ('کولر گازی', 'air-conditioner'),
        ('کولر آبی', 'evaporative-cooler'),
        ('پنکه', 'fan'),
        ('بخاری', 'heater'),
        ('آبگرمکن', 'water-heater'),
        ('سشوار', 'hair-dryer'),
        ('اتو مو', 'hair-straightener'),
        ('ریش تراش', 'shaver'),
        ('ماشین اصلاح', 'clipper')
    ]
    
    for fa, en in descriptors:
        if fa in combined_name and en not in tokens:
            tokens.append(en)
            
    # Colors & Specs
    colors = [
        ('استیل', 'steel'),
        ('سیلور', 'silver'),
        ('سفید چرمی', 'white-leather'),
        ('سفید', 'white'),
        ('مشکی', 'black'),
        ('تیتانیوم', 'titanium'),
        ('زرد', 'yellow'),
        ('سبز', 'green'),
        ('آبی', 'blue'),
        ('کرم', 'cream'),
        ('طلا', 'gold')
    ]
    for fa_c, en_c in colors:
        if fa_c in name or fa_c in combined_name:
            if en_c not in tokens:
                tokens.append(en_c)
            break
            
    slug = '-'.join(tokens)
    return slug

def search_item(item):
    name = clean_text(item.get('name'))
    brand = item.get('brand') or ''
    parent_name = clean_text(item.get('parent_name')) if item.get('is_variation') else ''
    
    queries = []
    if parent_name:
        queries.append(f"{brand} {parent_name} {name}")
        queries.append(f"{brand} {parent_name}")
    else:
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
                    if len(candidates) >= 3:
                        break
        except Exception:
            pass
        if len(candidates) >= 3:
            break
            
    return candidates

def process_single_item(item):
    sheet = item.get('sheet')
    sheet_folder = SHEET_FOLDER_MAP.get(sheet, 'misc')
    slug = build_english_slug(item)
    target_dir = os.path.join('scratch', 'candidates', sheet_folder, slug)
    os.makedirs(target_dir, exist_ok=True)
    
    candidates = search_item(item)
    downloaded = []
    
    for idx, c in enumerate(candidates, 1):
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
        except Exception:
            pass
            
    return {
        'row': item.get('row'),
        'name': item.get('name'),
        'parent_name': item.get('parent_name'),
        'brand': item.get('brand'),
        'sheet': sheet,
        'sheet_folder': sheet_folder,
        'slug': slug,
        'candidates': downloaded
    }

def run_fast_harvester():
    with open('scratch/missing_products.json', encoding='utf-8') as f:
        all_missing = json.load(f)
        
    print(f"Total missing products to harvest: {len(all_missing)}")
    results = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        future_to_item = {executor.submit(process_single_item, item): item for item in all_missing}
        completed = 0
        for future in as_completed(future_to_item):
            completed += 1
            res = future.result()
            results.append(res)
            if completed % 10 == 0 or completed == len(all_missing):
                print(f"Progress: {completed}/{len(all_missing)} processed (Latest: {res['slug']} -> {len(res['candidates'])} cands)")
                
    output_summary = 'scratch/all_candidates_harvested.json'
    with open(output_summary, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Done! All harvested candidates saved to {output_summary}")

if __name__ == '__main__':
    run_fast_harvester()
