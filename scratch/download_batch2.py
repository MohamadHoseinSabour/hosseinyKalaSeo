import os
import requests
import json
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

items = [
    {
        'category': 'refrigerators',
        'slug': 'niksan-rf8410-combi-fridge-steel',
        'url': 'https://dkstatics-public.digikala.com/digikala-products/329dbe967b5f109f40ad31a75dafcbdba60a28c7_1777371297.jpg'
    },
    {
        'category': 'cooking_appliances',
        'slug': 'parskhazar-rc181-silver-rice-cooker',
        'url': 'https://dkstatics-public.digikala.com/digikala-products/f1026fc567efea81f71027ef6dbee82349e0aca4_1785874562.jpg'
    },
    {
        'category': 'washing_and_cleaning',
        'slug': 'panda-80l-industrial-vacuum',
        'url': 'https://dkstatics-public.digikala.com/digikala-products/e045365d2f21ca1f9dd56d0b351d0090efc40b34_1688217164.jpg'
    },
    {
        'category': 'washing_and_cleaning',
        'slug': 'hitachi-cv950f-vacuum',
        'url': 'https://dkstatics-public.digikala.com/digikala-products/d2129a02e93636aa3c569c608967cfa7c9e48dc0_1786910212.jpg'
    }
]

for it in items:
    dest_dir = os.path.join('scratch', 'batch_eval', it['category'])
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, f"{it['slug']}.jpg")
    try:
        r = requests.get(it['url'], timeout=15)
        if r.status_code == 200:
            with open(dest_path, 'wb') as f:
                f.write(r.content)
            img = Image.open(dest_path)
            w, h = img.size
            print(f"Downloaded {it['slug']}: {w}x{h}")
    except Exception as e:
        print(f"Error {it['slug']}: {e}")
