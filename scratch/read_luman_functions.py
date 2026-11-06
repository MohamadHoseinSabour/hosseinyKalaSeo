import requests
import urllib3
import re
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER/domains/hosseinykala.ir/public_html/wp-content/plugins/luman-plus/Includes/Web/functions.php'
r = requests.get(url, cookies=cookies, verify=False)

with open('scratch/luman_functions.php', 'w', encoding='utf-8') as f:
    f.write(r.text)

print(f"Downloaded luman functions.php ({len(r.text)} bytes).")

for i, line in enumerate(r.text.splitlines()):
    if 'session' in line.lower():
        print(f"Line {i+1}: {line.strip()}")
    if 'add_action' in line and 'init' in line:
        print(f"Init hook at line {i+1}: {line.strip()}")
