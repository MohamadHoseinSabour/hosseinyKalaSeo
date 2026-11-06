import requests
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
r = requests.get('https://hosseinykala.ir/', headers=headers, timeout=15)
for m in re.finditer(r'<link[^>]*rel=["\']stylesheet["\'][^>]*>', r.text):
    print(m.group(0))
