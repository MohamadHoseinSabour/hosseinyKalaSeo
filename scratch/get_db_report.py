import requests
import urllib3
import json
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

params = {
    'action': 'view',
    'path': '/domains/hosseinykala.ir/public_html/wp-content',
    'filename': 'db_audit_report.json'
}

r = requests.get(url, cookies=cookies, params=params, verify=False)
print("Status:", r.status_code)
if r.status_code == 200:
    try:
        data = json.loads(r.text)
        print(json.dumps(data, indent=2, ensure_ascii=False)[:3000])
        with open('scratch/audit_results/db_report.json', 'w', encoding='utf-8') as f:
            f.write(r.text)
    except Exception as e:
        print("Parse error:", e)
        print("Raw text preview:", r.text[:500])
