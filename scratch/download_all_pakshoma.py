import requests
import json
import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

pid = 20061256 # Pakshoma FA15
r = requests.get(f'https://api.digikala.com/v2/product/{pid}/', headers=headers)
if r.status_code == 200:
    data = r.json().get('data', {}).get('product', {})
    images = data.get('images', {}).get('list', [])
    print(f"Total gallery images: {len(images)}")
    for idx, im in enumerate(images):
        url = im.get('url', [''])[0].split('?')[0]
        dest = f"scratch/test_download/pakshoma_full_gallery_{idx+1}.jpg"
        r_img = requests.get(url)
        with open(dest, 'wb') as f:
            f.write(r_img.content)
        img = Image.open(dest)
        print(f"Img {idx+1}: {url} -> {img.size[0]}x{img.size[1]}")
