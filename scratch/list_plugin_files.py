import requests
import urllib3
import urllib.parse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
headers = {'User-Agent': 'Mozilla/5.0'}

def list_files(rel_path):
    url = f'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER?path=/domains/hosseinykala.ir/public_html/{rel_path}'
    r = requests.get(url, cookies=cookies, headers=headers, verify=False)
    parsed = urllib.parse.parse_qs(r.text)
    files = []
    for k in sorted(parsed.keys()):
        if not k.startswith('/domains'): continue
        files.append(k.split('/')[-1])
    return files

print("ClubCore files:", list_files("wp-content/plugins/ClubCoreWP-main"))
print("RTL-CareUnit files:", list_files("wp-content/plugins/RTL-CareUnit"))
print("Luman Plus files:", list_files("wp-content/plugins/luman-plus"))
