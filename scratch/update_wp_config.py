import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

# Read current wp-config
r = requests.get('https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER/domains/hosseinykala.ir/public_html/wp-config.php', cookies=cookies, verify=False)
content = r.text

if 'WP_POST_REVISIONS' not in content:
    target = "define( 'WP_MEMORY_LIMIT', '256M' );"
    replacement = "define( 'WP_MEMORY_LIMIT', '512M' );\ndefine( 'WP_POST_REVISIONS', 5 );\ndefine( 'EMPTY_TRASH_DAYS', 7 );"
    if target in content:
        new_content = content.replace(target, replacement, 1)
        data = {
            'action': 'edit',
            'path': '/domains/hosseinykala.ir/public_html',
            'filename': 'wp-config.php',
            'text': new_content
        }
        r2 = requests.post(url, cookies=cookies, data=data, verify=False)
        print('Updated wp-config.php with revision limits & 512M memory:', r2.status_code)
    else:
        print('Target string not found in wp-config.php')
else:
    print('WP_POST_REVISIONS already present in wp-config.php')
