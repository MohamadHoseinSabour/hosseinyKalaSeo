import requests
import urllib3
import urllib.parse
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

params = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html',
    'filename': '.htaccess'
}
r = requests.get(url, cookies=cookies, params=params, verify=False)
parsed = urllib.parse.parse_qs(r.text)
text = parsed.get('text', [''])[0]
print("=== .htaccess ===")
print(text[:1500])
