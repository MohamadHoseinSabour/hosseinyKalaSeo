import requests
from bs4 import BeautifulSoup
import sys
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://hosseinykala.ir/', headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
soup = BeautifulSoup(r.text, 'html.parser')

links = soup.find_all('a')
for idx in [118, 122]:
    if idx < len(links):
        print(f"\n--- Link {idx} ---")
        print(str(links[idx])[:250])
