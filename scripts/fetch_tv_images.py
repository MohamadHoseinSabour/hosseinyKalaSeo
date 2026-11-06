import requests
import re
import urllib.parse
from PIL import Image
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 1. X-Vision from ITBazar
try:
    r = requests.get('https://www.itbazar.com/p_62328.aspx', headers=headers, timeout=10)
    # find images on itbazar
    imgs = re.findall(r'https?://[^\s"\'<>]+\.(?:jpg|png|webp)', r.text)
    prod_imgs = [im for im in imgs if 'images' in im and 'itbazar' in im and 'logo' not in im.lower()]
    print('ITBazar prod imgs:', prod_imgs[:3])
    if prod_imgs:
        r_img = requests.get(prod_imgs[0], headers=headers, timeout=10)
        with open('scratch/new_tvs_raw/xvision_43.jpg', 'wb') as f:
            f.write(r_img.content)
        im = Image.open('scratch/new_tvs_raw/xvision_43.jpg')
        print(f"X-Vision downloaded: {im.size}")
except Exception as e:
    print('Error X-Vision:', e)

# 2. Toshiba 50L2300 / 50L2300EE
try:
    # let's search via Emalls or directly
    q = urllib.parse.quote('توشیبا-50L2300')
    r = requests.get(f'https://emalls.ir/محصولات~search~{q}', headers=headers, timeout=10)
    imgs = re.findall(r'https://files\.emalls\.ir/files/Products/[^"\'\s]+\.(?:jpg|png|webp)', r.text)
    print('Toshiba 50 imgs:', imgs[:2])
    if imgs:
        r_img = requests.get(imgs[0], headers=headers, timeout=10)
        with open('scratch/new_tvs_raw/toshiba_50.jpg', 'wb') as f:
            f.write(r_img.content)
        im = Image.open('scratch/new_tvs_raw/toshiba_50.jpg')
        print(f"Toshiba 50 downloaded: {im.size}")
    else:
        # fallback search toshiba 50 inch
        q2 = urllib.parse.quote('تلویزیون-توشیبا-50-اینچ')
        r2 = requests.get(f'https://emalls.ir/محصولات~search~{q2}', headers=headers, timeout=10)
        imgs2 = re.findall(r'https://files\.emalls\.ir/files/Products/[^"\'\s]+\.(?:jpg|png|webp)', r2.text)
        if imgs2:
            r_img = requests.get(imgs2[0], headers=headers, timeout=10)
            with open('scratch/new_tvs_raw/toshiba_50.jpg', 'wb') as f:
                f.write(r_img.content)
            print(f"Toshiba 50 fallback downloaded: {Image.open('scratch/new_tvs_raw/toshiba_50.jpg').size}")
except Exception as e:
    print('Error Toshiba 50:', e)

# 3. Toshiba 55 inch
try:
    q = urllib.parse.quote('تلویزیون-توشیبا-55-اینچ')
    r = requests.get(f'https://emalls.ir/محصولات~search~{q}', headers=headers, timeout=10)
    imgs = re.findall(r'https://files\.emalls\.ir/files/Products/[^"\'\s]+\.(?:jpg|png|webp)', r.text)
    print('Toshiba 55 imgs:', imgs[:2])
    if imgs:
        r_img = requests.get(imgs[0], headers=headers, timeout=10)
        with open('scratch/new_tvs_raw/toshiba_55.jpg', 'wb') as f:
            f.write(r_img.content)
        im = Image.open('scratch/new_tvs_raw/toshiba_55.jpg')
        print(f"Toshiba 55 downloaded: {im.size}")
except Exception as e:
    print('Error Toshiba 55:', e)

# 4. Toshiba 43 inch
try:
    q = urllib.parse.quote('تلویزیون-توشیبا-43-اینچ')
    r = requests.get(f'https://emalls.ir/محصولات~search~{q}', headers=headers, timeout=10)
    imgs = re.findall(r'https://files\.emalls\.ir/files/Products/[^"\'\s]+\.(?:jpg|png|webp)', r.text)
    print('Toshiba 43 imgs:', imgs[:2])
    if imgs:
        r_img = requests.get(imgs[0], headers=headers, timeout=10)
        with open('scratch/new_tvs_raw/toshiba_43.jpg', 'wb') as f:
            f.write(r_img.content)
        im = Image.open('scratch/new_tvs_raw/toshiba_43.jpg')
        print(f"Toshiba 43 downloaded: {im.size}")
except Exception as e:
    print('Error Toshiba 43:', e)

# 5. Hisense 43 inch 4K
try:
    q = urllib.parse.quote('تلویزیون-هایسنس-43-اینچ-4k')
    r = requests.get(f'https://emalls.ir/محصولات~search~{q}', headers=headers, timeout=10)
    imgs = re.findall(r'https://files\.emalls\.ir/files/Products/[^"\'\s]+\.(?:jpg|png|webp)', r.text)
    print('Hisense 43 imgs:', imgs[:2])
    if imgs:
        r_img = requests.get(imgs[0], headers=headers, timeout=10)
        with open('scratch/new_tvs_raw/hisense_43.jpg', 'wb') as f:
            f.write(r_img.content)
        im = Image.open('scratch/new_tvs_raw/hisense_43.jpg')
        print(f"Hisense 43 downloaded: {im.size}")
except Exception as e:
    print('Error Hisense 43:', e)
