import requests
import re
from PIL import Image

r = requests.get('https://fullspecs.net/compare/hisense-43a6gx-vs-toshiba-43ul2163db/', headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
imgs = list(set(re.findall(r'https://fullspecs\.net/images/products/[^"\'\s]+\.jpg', r.text)))
print('Found:', imgs)
for img in imgs:
    if 'hisense' in img.lower():
        print('Hisense img:', img)
        r_img = requests.get(img, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        with open('scratch/new_tvs_raw/hisense_43.jpg', 'wb') as f:
            f.write(r_img.content)
        print('Saved hisense_43.jpg:', Image.open('scratch/new_tvs_raw/hisense_43.jpg').size)
        break
