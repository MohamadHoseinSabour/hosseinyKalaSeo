import requests
from bs4 import BeautifulSoup
import sys
import time

if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'fa-IR,fa;q=0.9,en-US;q=0.8',
}

for attempt in range(3):
    try:
        r = requests.get('https://hosseinykala.ir/', headers=headers, timeout=20)
        break
    except Exception as e:
        print(f"Attempt {attempt+1} failed: {e}")
        time.sleep(2)
else:
    print("Could not connect.")
    sys.exit(1)

soup = BeautifulSoup(r.text, 'html.parser')

carousel = soup.find('div', class_='xts-iimage-carousel')
if carousel:
    curr = carousel
    for depth in range(6):
        curr = curr.parent
        if not curr: break
        print(f"Parent L{depth+1}: <{curr.name}> class={curr.get('class')} id={curr.get('id')} data-id={curr.get('data-id')}")
