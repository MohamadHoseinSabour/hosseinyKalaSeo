import requests
import urllib3
import re
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_SITE_BACKUP'
data = {
    'form_version': '2',
    'domain': 'hosseinykala.ir',
    'action': 'backup',
    'select10': 'database',
    'select11': 'database_data'
}
r = requests.post(url, cookies=cookies, data=data, verify=False)
m = re.search(r'<div id="main_contents">(.*?)</div>', r.text, re.DOTALL)
if m:
    clean = re.sub(r'<[^>]+>', ' ', m.group(1)).strip()
    print('Message:', ' '.join(clean.split()))
else:
    print('Raw:', r.text[:300])
