import requests
import urllib3
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER'

temp_files = [
    'check_rev.php',
    'clean_rev.php',
    'db_audit.php',
    'find_session.php',
    'inspect_env.php',
    'inspect_litespeed.php',
    'run_db_opt.php'
]

data = {
    'action': 'multiple',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'button': 'delete'
}
for idx, f in enumerate(temp_files):
    data[f'select{idx}'] = f'/domains/hosseinykala.ir/public_html/wp-content/mu-plugins/{f}'

r = requests.post(url, cookies=cookies, data=data, verify=False)
print("Bulk delete status:", r.status_code)

# Check what remains in mu-plugins
r_list = requests.get('https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER', cookies=cookies, params={'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins'}, verify=False)
for item in r_list.text.split('&'):
    if '=' in item:
        key, _ = item.split('=', 1)
        import urllib.parse
        print("Remaining in mu-plugins:", urllib.parse.unquote(key))
