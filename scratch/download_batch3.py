import os
import requests
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

items = [
    {
        'category': 'washing_and_cleaning',
        'slug': 'feridolin-sw35-mini-wash',
        'url': 'https://dkstatics-public.digikala.com/digikala-products/ac14ba28798fe6f41b6f0add14f4c636164662f6_1754219851.jpg'
    },
    {
        'category': 'washing_and_cleaning',
        'slug': 'saper-4025-ceramic-steam-iron',
        'url': 'https://dkstatics-public.digikala.com/digikala-products/a2038a33ef13a2518236dd0a033ee7e8fb4285e4_1737183845.jpg'
    },
    {
        'category': 'cooking_appliances',
        'slug': 'alton-v303bn-built-in-oven',
        'url': 'https://dkstatics-public.digikala.com/digikala-products/a4de25416d09513f107df0ba0198200a19fc5fae_1733907386.jpg'
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
