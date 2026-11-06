import requests
import urllib3
import urllib.parse
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url_base = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

def check_dir(rel_path):
    url = f"{url_base}?path=/domains/hosseinykala.ir/public_html/{rel_path}"
    r = requests.get(url, cookies=cookies, verify=False)
    parsed = urllib.parse.parse_qs(r.text)
    items = []
    for k, v in parsed.items():
        if not k.startswith('/domains'): continue
        name = k.split('/')[-1]
        raw_info = v[0]
        # parse size
        size_match = urllib.parse.parse_qs(raw_info)
        size = size_match.get('size', ['0'])[0]
        items.append((name, size))
    return items

print("wp-content items with sizes:")
for name, size in check_dir('wp-content'):
    print(f"  {name}: {size}")

print("\nduplicator-backups items:")
for name, size in check_dir('wp-content/duplicator-backups'):
    print(f"  {name}: {size}")
