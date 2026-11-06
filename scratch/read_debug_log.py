import requests
import urllib3
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

# Read wp-content/debug.log
r = requests.get(url, cookies=cookies, params={
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content',
    'filename': 'debug.log'
}, verify=False)

import urllib.parse
parsed = urllib.parse.parse_qs(r.text)
text = parsed.get('text', [''])[0]
print("Last lines of debug.log:\n", text[-2000:])
