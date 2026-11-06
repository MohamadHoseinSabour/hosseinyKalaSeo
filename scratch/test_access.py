import requests
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 1. Test WordPress API
print("=== Testing WordPress API with 'agent' ===")
auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
wp_headers = {'User-Agent': 'Mozilla/5.0'}

r_plug = requests.get('https://hosseinykala.ir/wp-json/wp/v2/plugins', auth=auth, headers=wp_headers, timeout=15)
print('Plugins endpoint status:', r_plug.status_code)
if r_plug.status_code == 200:
    plugins = r_plug.json()
    print(f'Total plugins returned: {len(plugins)}')
    for p in plugins:
        print(f"  [{p.get('status')}] {p.get('plugin')} -> {p.get('name')}")
else:
    print('Plugins response:', r_plug.text[:200])

r_settings = requests.get('https://hosseinykala.ir/wp-json/wp/v2/settings', auth=auth, headers=wp_headers, timeout=15)
print('\nSettings endpoint status:', r_settings.status_code)
if r_settings.status_code == 200:
    print('Site title:', r_settings.json().get('title'))
    print('Site url:', r_settings.json().get('url'))

# 2. Test DirectAdmin Session
print("\n=== Testing DirectAdmin Session ===")
da_url = "https://server152c.irwebspace.com:2223/CMD_SHOW_DOMAIN?domain=hosseinykala.ir"
da_cookies = {
    'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'
}
da_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

r_da = requests.get(da_url, cookies=da_cookies, headers=da_headers, timeout=15, verify=False)
print('DirectAdmin status:', r_da.status_code)
print('DirectAdmin final URL:', r_da.url)
print('DirectAdmin response length:', len(r_da.text))
if 'login' in r_da.url.lower() or 'login' in r_da.text.lower()[:300]:
    print('DirectAdmin returned login page (session might need refresh or specific path).')
else:
    print('DirectAdmin authenticated successfully!')
    print('Sample DA title/content:', r_da.text[:300])
