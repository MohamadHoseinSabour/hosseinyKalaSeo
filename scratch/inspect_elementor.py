import requests
from bs4 import BeautifulSoup
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}
r = requests.get('https://hosseinykala.ir/', headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

el = soup.find('div', class_='elementor-1705')
if el:
    print("Direct children of elementor-1705:")
    sections = el.find_all('section', recursive=False)
    print(f"Total top sections: {len(sections)}")
    for idx, sec in enumerate(sections[:5]):
        sec_id = sec.get('id', '')
        sec_classes = sec.get('class', [])
        # Find all images or background images inside this section
        imgs = sec.find_all('img')
        print(f"Section #{idx+1}: class={sec_classes} | id={sec_id} | img_count={len(imgs)}")
        # Check background image in style
        style = sec.get('style', '')
        if 'background' in style:
            print("  Inline style background:", style[:100])
        # Check first column or widget
        widgets = sec.find_all('div', class_=lambda c: c and 'elementor-widget' in c)
        print(f"  Widgets count: {len(widgets)}")
        for w in widgets[:3]:
            print("    Widget type:", w.get('data-widget_type'))
