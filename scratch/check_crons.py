import requests
import urllib3
import urllib.parse
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_CRON_JOBS'

r = requests.get(url, cookies=cookies, verify=False)
print("Cron Jobs API status:", r.status_code)
for item in r.text.split('&'):
    if '=' in item:
        k, v = item.split('=', 1)
        print(urllib.parse.unquote(k), ":", urllib.parse.unquote(v))
