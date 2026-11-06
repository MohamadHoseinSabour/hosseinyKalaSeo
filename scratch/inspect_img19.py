import requests
from bs4 import BeautifulSoup
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://hosseinykala.ir/', headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'html.parser')

imgs = soup.find_all('img')
img19 = imgs[18] # index 18 is 19th img
print("Attributes of Img #19:")
for k, v in img19.attrs.items():
    print(f"  {k}: {v}")

parent = img19.parent
print("\nParent:", parent.name, parent.attrs)
gp = parent.parent
print("Grandparent:", gp.name, gp.attrs)
ggp = gp.parent
print("Great-grandparent:", ggp.name, ggp.attrs)
