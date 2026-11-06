import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
headers = {'User-Agent': 'Mozilla/5.0'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

files_to_delete = [
    'init_callbacks.txt',
    'init_start.txt',
    'first_active.txt',
    'session_exact.json',
    'session_p_trace.txt',
    'session_contents.json',
    'reflection_info.json',
    'trace_19.txt',
    'culprit_10.txt',
    'litespeed_db_options.json',
    'session_culprit.json'
]

for i, f in enumerate(files_to_delete):
    data = {
        'action': 'delete',
        'path': '/domains/hosseinykala.ir/public_html/wp-content',
        'select0': f
    }
    r = requests.post(url, cookies=cookies, headers=headers, data=data, verify=False, timeout=10)
    print(f"Deleted {f}: {r.status_code}")
