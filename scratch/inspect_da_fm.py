import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER/domains/hosseinykala.ir/public_html/wp-content/mu-plugins'

r = requests.get(url, cookies=cookies, verify=False)
print("CMD_FILE_MANAGER status:", r.status_code)
# Search for delete form or action in html
for line in r.text.splitlines():
    if 'delete' in line.lower() or 'select' in line.lower() or 'action=' in line.lower():
        print(line[:150])
