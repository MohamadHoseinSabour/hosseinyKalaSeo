import requests
from bs4 import BeautifulSoup
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://hosseinykala.ir/', headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
soup = BeautifulSoup(r.text, 'html.parser')

links = soup.find_all('a')
print(f"Total links on page: {len(links)}")

empty_links = []
for i, l in enumerate(links):
    text = l.get_text(strip=True)
    aria_label = l.get('aria-label')
    aria_labelledby = l.get('aria-labelledby')
    title = l.get('title')
    img = l.find('img')
    img_alt = img.get('alt') if img else None
    
    has_accessible_name = bool(text or aria_label or aria_labelledby or title or (img and img_alt))
    if not has_accessible_name:
        empty_links.append((i, l.get('href'), l.get('class'), str(l)[:150]))

print(f"Links without accessible name: {len(empty_links)}")
for idx, href, cls, snippet in empty_links:
    print(f"\nLink #{idx}: href={href} | class={cls}")
    print(f"  Snippet: {snippet}")
