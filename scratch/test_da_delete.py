import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

# Test creating and deleting a temp file
r1 = requests.post(url, cookies=cookies, data={
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'temp_test.txt',
    'text': 'hello'
}, verify=False)
print("Create test file:", r1.status_code, r1.text[:200])

# Try delete method 1:
# In DirectAdmin, action=multiple with delete=Delete
r2 = requests.post(url, cookies=cookies, data={
    'action': 'multiple',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'select0': 'temp_test.txt',
    'delete': 'Delete'
}, verify=False)
print("Delete method 1 (action=multiple):", r2.status_code, r2.text[:200])
