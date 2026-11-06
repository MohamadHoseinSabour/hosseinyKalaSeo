import requests
import re
from PIL import Image

headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get('https://fullspecs.net/compare/toshiba-43l2163db-vs-hisense-43a6gx/', headers=headers, timeout=10)
print('Status:', r.status_code)
imgs = re.findall(r'https://fullspecs\.net/images/products/[^"\'\s]+\.jpg', r.text)
print('Found images:', imgs)
if len(imgs) >= 2:
    r_tosh = requests.get(imgs[0], headers=headers, timeout=10)
    with open('scratch/new_tvs_raw/toshiba_43.jpg', 'wb') as f:
        f.write(r_tosh.content)
    r_his = requests.get(imgs[1], headers=headers, timeout=10)
    with open('scratch/new_tvs_raw/hisense_43.jpg', 'wb') as f:
        f.write(r_his.content)
    print('Toshiba 43:', Image.open('scratch/new_tvs_raw/toshiba_43.jpg').size)
    print('Hisense 43:', Image.open('scratch/new_tvs_raw/hisense_43.jpg').size)
