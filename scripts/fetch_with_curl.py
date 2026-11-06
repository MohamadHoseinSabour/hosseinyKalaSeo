import subprocess
import re
import requests
from PIL import Image

dkp_dict = {
    'toshiba_50.jpg': 'https://www.digikala.com/product/dkp-21409192/',
    'toshiba_43.jpg': 'https://www.digikala.com/product/dkp-21409131/',
    'hisense_43.jpg': 'https://www.digikala.com/product/dkp-22123037/'
}

for fname, url in dkp_dict.items():
    tmp_file = f'scratch/tmp_{fname}.html'
    subprocess.run(['curl.exe', '-sL', '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)', url, '-o', tmp_file], check=False)
    with open(tmp_file, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    imgs = list(set(re.findall(r'https://dkstatics-public\.digikala\.com/digikala-products/[^"\'\s]+\.jpg', text)))
    print(f'{fname}: found {len(imgs)} imgs')
    if imgs:
        img_url = imgs[0]
        # remove any query parameters
        img_url = img_url.split('?')[0]
        print(f'  Downloading: {img_url}')
        r = requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            with open(f'scratch/new_tvs_raw/{fname}', 'wb') as out_f:
                out_f.write(r.content)
            im = Image.open(f'scratch/new_tvs_raw/{fname}')
            print(f'  ✓ Saved {fname}: {im.size}')
