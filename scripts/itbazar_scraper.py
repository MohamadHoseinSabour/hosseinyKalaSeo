import os
import sys
import requests
import re
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for kw in ['توشیبا', 'هایسنس']:
    r = requests.get(f'https://www.itbazar.com/search.aspx?q={kw}', headers=headers, timeout=10)
    print(f'ITBazar search {kw} status: {r.status_code}')
    imgs = re.findall(r'src="(https://images\.itbazar\.com/multimedia/[^"]+)"\s+alt="([^"]+)"', r.text)
    print(f'Found {len(imgs)} images for {kw}:')
    for img_url, alt in imgs:
        if 'تلویزیون' in alt or 'tv' in alt.lower():
            print(f"  {alt} -> {img_url}")
            if kw == 'توشیبا':
                if '50' in alt and not os.path.exists('scratch/new_tvs_raw/toshiba_50.jpg'):
                    r_im = requests.get(img_url, headers=headers, timeout=10)
                    with open('scratch/new_tvs_raw/toshiba_50.jpg', 'wb') as f:
                        f.write(r_im.content)
                    print('  ✓ Saved toshiba_50.jpg')
                elif '55' in alt and not os.path.exists('scratch/new_tvs_raw/toshiba_55.jpg'):
                    r_im = requests.get(img_url, headers=headers, timeout=10)
                    with open('scratch/new_tvs_raw/toshiba_55.jpg', 'wb') as f:
                        f.write(r_im.content)
                    print('  ✓ Saved toshiba_55.jpg')
                elif '43' in alt and not os.path.exists('scratch/new_tvs_raw/toshiba_43.jpg'):
                    r_im = requests.get(img_url, headers=headers, timeout=10)
                    with open('scratch/new_tvs_raw/toshiba_43.jpg', 'wb') as f:
                        f.write(r_im.content)
                    print('  ✓ Saved toshiba_43.jpg')
            elif kw == 'هایسنس':
                if '43' in alt and not os.path.exists('scratch/new_tvs_raw/hisense_43.jpg'):
                    r_im = requests.get(img_url, headers=headers, timeout=10)
                    with open('scratch/new_tvs_raw/hisense_43.jpg', 'wb') as f:
                        f.write(r_im.content)
                    print('  ✓ Saved hisense_43.jpg')
