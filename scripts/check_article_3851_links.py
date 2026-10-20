import requests
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/posts/3851', auth=AUTH, headers=headers)
if r.status_code == 200:
    content = r.json().get('content', {}).get('rendered', '')
    links = re.findall(r'href=[\'"]([^\'"]+)[\'"]', content)
    print(f"Article 3851 has {len(links)} links:")
    for l in links:
        # test HTTP status
        rl = requests.get(l, headers=headers, timeout=15)
        print(f"  [{rl.status_code}] {l}")
