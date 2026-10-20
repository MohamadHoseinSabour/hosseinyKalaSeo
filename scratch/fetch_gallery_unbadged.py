import requests
import json
import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# Let's search and get product IDs, then fetch gallery images
queries = [
    ('daewoo_silver', 'ماشین لباسشویی دوو LM-990S'),
    ('pakshoma_15kg', 'لباسشویی دوقلو پاکشوما FA15'),
    ('pakshoma_21kg', 'لباسشویی دوقلو پاکشوما FA21')
]

for label, q in queries:
    r = requests.get('https://api.digikala.com/v1/search/', params={'q': q}, headers=headers, timeout=6)
    if r.status_code == 200:
        prods = r.json().get('data', {}).get('products', [])
        if prods:
            pid = prods[0].get('id')
            title = prods[0].get('title_fa')
            print(f"\nProduct: {label} -> ID {pid}: {title}")
            
            # Fetch details via v2
            r_det = requests.get(f'https://api.digikala.com/v2/product/{pid}/', headers=headers, timeout=6)
            if r_det.status_code == 200:
                p_data = r_det.json().get('data', {}).get('product', {})
                images_list = p_data.get('images', {}).get('list', [])
                print(f"Gallery images count: {len(images_list)}")
                for idx, im_info in enumerate(images_list[:4]):
                    raw_url = im_info.get('url', [''])[0].split('?')[0]
                    print(f"  Img {idx+1}: {raw_url}")
                    
                    # Download to test
                    dest_file = f"scratch/test_download/{label}_gallery_{idx+1}.jpg"
                    os.makedirs('scratch/test_download', exist_ok=True)
                    r_img = requests.get(raw_url, timeout=10)
                    if r_img.status_code == 200:
                        with open(dest_file, 'wb') as f_out:
                            f_out.write(r_img.content)
                        im = Image.open(dest_file)
                        print(f"     Saved: {dest_file} ({im.size[0]}x{im.size[1]})")
