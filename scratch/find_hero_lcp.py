import requests
from bs4 import BeautifulSoup
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}
r = requests.get('https://hosseinykala.ir/', headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

print("=== Search for ds1.webp in body ===")
found = soup.find_all(lambda tag: 'ds1.webp' in str(tag.attrs.values()) or ('src' in tag.attrs and 'ds1.webp' in tag['src']) or ('data-src' in tag.attrs and 'ds1.webp' in tag['data-src']))
print(f"Tags with ds1.webp: {len(found)}")
for t in found:
    print(t.name, t.get('class'), t.get('src', '')[:60], t.get('data-src', '')[:60])
    print("Parent:", t.parent.name if t.parent else None, t.parent.get('class') if t.parent else None)

print("\n=== Main Slider / Hero Section ===")
slider = soup.find(class_=lambda c: c and ('slider' in c.lower() or 'hero' in c.lower() or 'banner' in c.lower() or 'rev_slider' in c.lower() or 'elementor-section' in c.lower()))
if slider:
    print("Top section tag:", slider.name, slider.get('class'))
    section_imgs = slider.find_all('img')
    print(f"Images in top section: {len(section_imgs)}")
    for si in section_imgs[:5]:
        print("  img:", si.get('class'), si.get('src', '')[:70], "width:", si.get('width'), "height:", si.get('height'))
