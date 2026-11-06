import requests
from bs4 import BeautifulSoup
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://hosseinykala.ir/', headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'html.parser')

el = soup.find('div', class_='elementor-1705')
containers = el.find_all('div', class_=lambda c: c and 'e-parent' in c)
print(f"Total top containers (e-parent): {len(containers)}")

for idx, c in enumerate(containers[:5]):
    c_id = c.get('data-id')
    classes = c.get('class', [])
    imgs = c.find_all('img')
    headings = c.find_all(['h1', 'h2', 'h3', 'span'], class_=lambda cl: cl and 'elementor-heading-title' in cl)
    print(f"\n--- Container #{idx+1} (data-id={c_id}) ---")
    print(f"  Classes: {classes}")
    print(f"  Headings ({len(headings)}): {[h.text.strip()[:40] for h in headings]}")
    print(f"  Images ({len(imgs)}):")
    for img in imgs:
        src = img.get('src') or ''
        data_src = img.get('data-src') or ''
        w = img.get('width')
        h = img.get('height')
        loading = img.get('loading')
        print(f"    - img class={img.get('class')}")
        print(f"      src={src[:60]}")
        print(f"      data-src={data_src[:80]}")
        print(f"      w={w}, h={h}, loading={loading}")
