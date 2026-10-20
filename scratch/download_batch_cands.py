import os
import requests
import json
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

candidates_to_download = [
    {
        'category': 'washing_and_cleaning',
        'slug': 'pakizan-blanket-washer-30kg',
        'target_name': 'پتوشور صنعتی و خانگی پاکیزان مدل 30 کیلوگرم',
        'cand_title': 'پتو شوی پاکیزان مدل 30',
        'url': 'https://dkstatics-public.digikala.com/digikala-products/40cae9f1a60f3d1701976f052e8a17730d1a702d_1672687325.jpg'
    },
    {
        'category': 'washing_and_cleaning',
        'slug': 'pakizan-blanket-washer-40kg',
        'target_name': 'پتوشور صنعتی و خانگی پاکیزان مدل 40 کیلوگرم',
        'cand_title': 'پتو شوی پاکیزان کد 40',
        'url': 'https://dkstatics-public.digikala.com/digikala-products/21f315b164dde851b1f983ec6bb3197d2df30b59_1757236354.jpg'
    },
    {
        'category': 'cooling_heating',
        'slug': 'parskhazar-fh2000p-heater',
        'target_name': 'بخاری پارس خزر فن دار مدل FH-2000P',
        'cand_title': 'فن هیتر پارس خزر مدل FH2000P',
        'url': 'https://dkstatics-public.digikala.com/digikala-products/36d16a652782552ff27f8b534fc7459febd55801_1786910151.jpg'
    },
    {
        'category': 'cooling_heating',
        'slug': 'polar-3pn-new-heater',
        'target_name': 'بخاری پلار مدل 3PN-NEW ماشینی',
        'cand_title': 'بخاری گازی پلار مدل 3PN',
        'url': 'https://dkstatics-public.digikala.com/digikala-products/4677383.jpg'
    },
    {
        'category': 'beverage_makers',
        'slug': 'korkmaz-a331-tea-maker',
        'target_name': 'چای ساز کورکماز مدل A331',
        'cand_title': 'چای ساز کرکماز مدل A331-09',
        'url': 'https://dkstatics-public.digikala.com/digikala-products/0aed1d8282708a1867f3fca8bc2dddc9c76ffb38_1786910225.jpg'
    }
]

downloaded = []
for item in candidates_to_download:
    dest_dir = os.path.join('scratch', 'batch_eval', item['category'])
    os.makedirs(dest_dir, exist_ok=True)
    dest_file = os.path.join(dest_dir, f"{item['slug']}.jpg")
    
    try:
        r = requests.get(item['url'], timeout=15)
        if r.status_code == 200:
            with open(dest_file, 'wb') as f:
                f.write(r.content)
            img = Image.open(dest_file)
            w, h = img.size
            item['file_path'] = os.path.abspath(dest_file)
            item['dimensions'] = f"{w}x{h}"
            downloaded.append(item)
            print(f"Downloaded: {item['slug']} -> {w}x{h}")
    except Exception as e:
        print(f"Error downloading {item['slug']}: {e}")

with open('scratch/batch_eval_items.json', 'w', encoding='utf-8') as f:
    json.dump(downloaded, f, ensure_ascii=False, indent=2)
