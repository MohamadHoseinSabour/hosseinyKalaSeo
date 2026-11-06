import requests
import urllib3
import urllib.parse
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

files = ['db_audit.php', 'clean_rev.php', 'run_db_opt.php']
for f in files:
    params = {
        'action': 'edit',
        'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
        'filename': f
    }
    r = requests.get(url, cookies=cookies, params=params, verify=False)
    parsed = urllib.parse.parse_qs(r.text)
    text = parsed.get('text', [''])[0]
    print(f"=== {f} ===")
    print(text[:300])
    print()
