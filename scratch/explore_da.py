import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

da_url_base = "https://server152c.irwebspace.com:2223"
cookies = {
    'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

endpoints = [
    '/CMD_FILE_MANAGER?path=/domains/hosseinykala.ir/public_html',
    '/CMD_TERMINAL',
    '/CMD_SHOW_USER?user=hosseiny',
    '/CMD_DB',
    '/CMD_SITE_BACKUP',
    '/CMD_API_FILE_MANAGER?path=/domains/hosseinykala.ir/public_html'
]

for ep in endpoints:
    url = da_url_base + ep
    r = requests.get(url, cookies=cookies, headers=headers, verify=False, timeout=10)
    print(f"{ep.split('?')[0]} -> Status {r.status_code} | Len {len(r.text)} | URL: {r.url}")
