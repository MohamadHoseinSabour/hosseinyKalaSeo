import requests
import urllib3
from bs4 import BeautifulSoup
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER/domains/hosseinykala.ir/public_html/wp-content/mu-plugins'

r = requests.get(url, cookies=cookies, verify=False)
soup = BeautifulSoup(r.text, 'html.parser')
form = soup.find('form', {'name': 'tableform'})
if form:
    print("Form action:", form.get('action'))
    inputs = form.find_all('input')
    for inp in inputs:
        print(inp.get('type'), inp.get('name'), inp.get('value'))
else:
    print("Form not found!")
