import requests
from bs4 import BeautifulSoup

r = requests.get('https://kahler.ir/product-category/%d8%a7%d8%aa%d9%88/', headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
print("Irons category status:", r.status_code)
if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'html.parser')
    for item in soup.find_all(['h2', 'h3', 'a']):
        text = item.get_text(strip=True)
        href = item.get('href', '')
        if '81' in text or 'اتو' in text:
            print(f"Title: {text} | Link: {href}")
            img = item.find('img')
            if img:
                print(f"  Img: {img.get('src')}")
