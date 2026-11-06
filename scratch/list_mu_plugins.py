import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

params = {
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins'
}
r = requests.get(url, cookies=cookies, params=params, verify=False)
for item in r.text.split('&'):
    if '=' in item:
        key, val = item.split('=', 1)
        import urllib.parse
        print(urllib.parse.unquote(key))
