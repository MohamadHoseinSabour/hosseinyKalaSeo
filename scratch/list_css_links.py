import requests
import re
from bs4 import BeautifulSoup

r = requests.get('https://hosseinykala.ir/', headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
soup = BeautifulSoup(r.text, 'html.parser')

links = soup.find_all('link', rel=lambda x: x and 'stylesheet' in x)
print(f"Total stylesheet links: {len(links)}")
for l in links:
    print(f"  id={l.get('id')} | href={l.get('href')} | media={l.get('media')}")
