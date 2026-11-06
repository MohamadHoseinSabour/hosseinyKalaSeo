import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

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
    'delete': 'Delete'
}
for idx, f in enumerate(temp_files):
    data[f'select{idx}'] = f

r = requests.post(url, cookies=cookies, data=data, verify=False)
print("Bulk delete status:", r.status_code, r.text)
