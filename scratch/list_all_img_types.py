import requests
from bs4 import BeautifulSoup
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://hosseinykala.ir/', headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'html.parser')

imgs = soup.find_all('img')
print(f"Total img tags on page: {len(imgs)}")

# Let's see the unique parents or sections where images appear
seen_classes = set()
for idx, img in enumerate(imgs):
    parent = img.parent
    p_class = tuple(parent.get('class', [])) if parent else ()
    gp = parent.parent if parent else None
    gp_class = tuple(gp.get('class', [])) if gp else ()
    
    src = img.get('src', '')
    data_src = img.get('data-src', '')
    actual_url = data_src if 'base64' in src else src
    
    if (p_class, gp_class) not in seen_classes:
        seen_classes.add((p_class, gp_class))
        print(f"\n[Img #{idx+1}]:")
        print(f"  Parent: {parent.name} | class: {parent.get('class')}")
        print(f"  Grandparent: {gp.name if gp else None} | class: {gp.get('class') if gp else None}")
        print(f"  Actual URL: {actual_url[:90]}")
        print(f"  w={img.get('width')}, h={img.get('height')}, loading={img.get('loading')}")
