import requests
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
r = requests.get('https://hosseinykala.ir/', headers=headers, timeout=25)
print("Status:", r.status_code)
links = re.findall(r'<link[^>]*stylesheet[^>]*>', r.text)
print("Stylesheet links count:", len(links))
for l in links:
    print(l)
