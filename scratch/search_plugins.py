import requests
import urllib3
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

da_url_base = "https://server152c.irwebspace.com:2223"
cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
headers = {'User-Agent': 'Mozilla/5.0'}

plugins_to_check = [
    'ClubCoreWP-main/clubcore.php',
    'emalls-extraction-api-official/emalls-extraction-api-official.php',
    'products-extractor-for-woocommerce/wcpe.php',
    'sync-basalam/sync-basalam.php',
    'sync-basalam-plugin-pro/sync-basalam-pro.php',
    'RTL-CareUnit/RTL-CareUnit.php',
    'luman-plus/luman-plus.php',
    'wp-parsidate/wp-parsidate.php',
    'zibal-payment-gateway-for-woocommerce-master/index.php'
]

for p in plugins_to_check:
    url = f"{da_url_base}/CMD_FILE_MANAGER/domains/hosseinykala.ir/public_html/wp-content/plugins/{p}"
    r = requests.get(url, cookies=cookies, headers=headers, verify=False, timeout=10)
    if r.status_code == 200:
        found = re.findall(r'session_start\s*\(', r.text, re.IGNORECASE)
        found_cookie = re.findall(r'setcookie\s*\(', r.text, re.IGNORECASE)
        print(f"Plugin [{p}]: status 200 (len {len(r.text)}) | session_start: {len(found)} | setcookie: {len(found_cookie)}")
        if found:
            # show surrounding lines
            for match in re.finditer(r'session_start\s*\(', r.text, re.IGNORECASE):
                start = max(0, match.start() - 100)
                end = min(len(r.text), match.end() + 100)
                print("   Context:", repr(r.text[start:end]))
    else:
        print(f"Plugin [{p}]: HTTP {r.status_code}")
