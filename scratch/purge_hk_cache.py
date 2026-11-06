import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER'

data = {
    'action': 'multiple',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/cache',
    'select0': '/domains/hosseinykala.ir/public_html/wp-content/cache/hk_fastcache',
    'button': 'delete'
}
r = requests.post(url, cookies=cookies, data=data, verify=False)
print("Delete hk_fastcache status:", r.status_code)
