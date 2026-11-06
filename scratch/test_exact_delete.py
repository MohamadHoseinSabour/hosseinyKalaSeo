import requests
import urllib3
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER'

data = {
    'action': 'multiple',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'select0': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins/temp_test.txt',
    'button': 'delete'
}
r = requests.post(url, cookies=cookies, data=data, verify=False)
print("Delete with 'delete':", r.status_code, "temp_test" in r.text)

# Also test if 'حذف' is needed
if "temp_test" in r.text:
    data['button'] = 'حذف'
    r2 = requests.post(url, cookies=cookies, data=data, verify=False)
    print("Delete with 'حذف':", r2.status_code, "temp_test" in r2.text)
