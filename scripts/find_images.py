import requests
import re
from PIL import Image

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 1. Tolostar Olive URL
red_url = 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFJ6-e3d2Cl-NbqE2n9JyHNzDj3Go6ARRFP56NIejr2XEHnUcDyGEmoxaBWZ6ceFhCEPY9EHcqq_iBHYqMKWTzK7nWRKoKpVl34Y5TVBBmXHC9IWmfkazQborLB66klmQ=='
try:
    res = requests.get(red_url, allow_redirects=True, headers=headers, timeout=10)
    print('Tolostar URL:', res.url)
    og = re.search(r'property="og:image"\s+content="([^"]+)"', res.text)
    if og:
        print('Tolostar og:image:', og.group(1))
        r_img = requests.get(og.group(1), headers=headers, timeout=10)
        if r_img.status_code == 200:
            with open('scratch/new_2_prods/olive_raw.jpg', 'wb') as f:
                f.write(r_img.content)
            print('Saved olive_raw.jpg!')
except Exception as e:
    print('Tolostar error:', e)

# 2. Bahamshop Olive URL
red_url2 = 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGU2mKSsegsysEbREsfqNZnUd6ajWZeGffb8t1nNVJoLbYKqZ6EhkR9oEkxBte7NrD8GZmfQ2DyYaC_JK0WXooFlGO6gijBcmV7zplnqcSFWim6Lj7PGWJ5W0Msb6i5JA=='
try:
    res2 = requests.get(red_url2, allow_redirects=True, headers=headers, timeout=10)
    print('Bahamshop URL:', res2.url)
    og2 = re.search(r'property="og:image"\s+content="([^"]+)"', res2.text)
    if og2:
        print('Bahamshop og:image:', og2.group(1))
        if not os.path.exists('scratch/new_2_prods/olive_raw.jpg'):
            r_img = requests.get(og2.group(1), headers=headers, timeout=10)
            if r_img.status_code == 200:
                with open('scratch/new_2_prods/olive_raw.jpg', 'wb') as f:
                    f.write(r_img.content)
                print('Saved olive_raw.jpg from Bahamshop!')
except Exception as e:
    print('Bahamshop error:', e)
