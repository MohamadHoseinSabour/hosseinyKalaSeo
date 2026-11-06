import requests
from bs4 import BeautifulSoup
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
})

# Add product
session.post('https://hosseinykala.ir/?add-to-cart=4294', data={'quantity': 1}, verify=False)

r = session.get('https://hosseinykala.ir/checkout/', verify=False)
soup = BeautifulSoup(r.text, 'html.parser')

print('Title:', soup.title.string if soup.title else 'No title')
print('H1:', soup.find('h1').text if soup.find('h1') else 'No H1')

# Check what forms exist
forms = soup.find_all('form')
print(f'Forms found: {len(forms)}')
for f in forms:
    print('  Form class:', f.get('class'), 'action:', f.get('action'))

entry = soup.find('div', class_='entry-content')
if entry:
    print('Entry snippet:\n', entry.text[:400].strip())
