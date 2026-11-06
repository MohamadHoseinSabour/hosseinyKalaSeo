import requests
from bs4 import BeautifulSoup
import sys
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}
r = requests.get('https://hosseinykala.ir/', headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

container = soup.find('div', attrs={'data-id': 'e82e234'})
if container:
    widgets = container.find_all('div', class_=lambda c: c and 'elementor-widget' in c)
    print(f"Widgets in hero container e82e234 ({len(widgets)} total):")
    for w in widgets:
        print(f"Widget data-id={w.get('data-id')} type={w.get('data-widget_type')} classes={w.get('class')}")
        imgs = w.find_all('img')
        for img in imgs:
            print(f"  img: src={img.get('src')[:70]} | data-xts-src={img.get('data-xts-src', '')[:70]} | w={img.get('width')} | h={img.get('height')}")
