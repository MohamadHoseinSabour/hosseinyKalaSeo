import sys
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

html_path = r'c:\Users\mmhhs\Downloads\rp_cu_5.html'
with open(html_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

rows = soup.find_all('tr')
all_items = []
for r in rows:
    cols = [c.get_text(strip=True) for c in r.find_all(['td', 'th'])]
    if len(cols) >= 2:
        all_items.append(cols)

print(f'Total valid table rows: {len(all_items)}')

keywords = ['توشیبا', 'ایکس', 'xvision', 'toshiba', 'x.visjon', 'x-vision', 'سونی', 'sony', 'سامسونگ', 'samsung', 'ال جی', 'lg', 'تی سی ال', 'tcl', 'اسنوا', 'دوو', 'شهاب', 'جی پلاس', 'gplus', 'هایسنس', 'hisense', 'پارس', 'پانورامیک', 'ال ای دی', 'led', 'lcd', 'oled', 'qled', 'اینچ', 'اینج', 'tv', 'TV', 'مانیتور', 'پلاسما']

matched = []
for item in all_items:
    joined = ' '.join(item)
    for kw in keywords:
        if kw.lower() in joined.lower():
            matched.append((kw, item))
            break

print(f'Total matched items: {len(matched)}')
for kw, it in matched:
    print(f'[{kw}]', ' | '.join(it))
