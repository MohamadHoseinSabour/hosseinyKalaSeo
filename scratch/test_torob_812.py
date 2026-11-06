import sys
import requests

sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {'User-Agent': 'Mozilla/5.0'}
url = 'https://api.torob.com/v4/base-product/search/?sort=popularity&page=0&size=5&query=%D8%A7%D8%AA%D9%88%20%DA%A9%D8%A7%D8%AE%D9%84%D8%B1%20812'
r = requests.get(url, headers=HEADERS, timeout=10)
print('Torob status:', r.status_code)
if r.status_code == 200:
    for item in r.json().get('results', []):
        print(item.get('name1'), item.get('image_url'))
