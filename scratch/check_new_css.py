import requests
import re

r = requests.get('https://hosseinykala.ir/', headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
m = re.findall(r'href=[\'"](https://hosseinykala\.ir/wp-content/[^\'"]+\.css[^\'"]*)[\'"]', r.text)
print("Current CSS links in HTML:")
for u in m:
    print(' ', u)
    try:
        r_css = requests.get(u, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Encoding': 'gzip'}, timeout=15)
        print('    Status:', r_css.status_code, 'Size:', len(r_css.content), 'bytes')
    except Exception as e:
        print('    Error:', e)
