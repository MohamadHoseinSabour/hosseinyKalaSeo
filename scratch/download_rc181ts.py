import requests
import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

url_ts181 = 'https://dkstatics-public.digikala.com/digikala-products/120490961.jpg'
dest_ts181 = 'scratch/batch_eval/cooking_appliances/parskhazar-rc181ts-silver-rice-cooker.jpg'

r = requests.get(url_ts181)
if r.status_code == 200:
    with open(dest_ts181, 'wb') as f:
        f.write(r.content)
    img = Image.open(dest_ts181)
    w, h = img.size
    print(f"Downloaded RC-181TS: {w}x{h}")
