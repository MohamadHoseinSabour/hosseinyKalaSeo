import requests
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/posts/3851', auth=AUTH, headers=headers)
if r.status_code == 200:
    content = r.json().get('content', {}).get('rendered', '')
    links = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', content, re.DOTALL)
    print(f"Article 3851 currently has {len(links)} links:\n")
    for i, (l, text) in enumerate(links, 1):
        clean_text = re.sub(r'<[^>]+>', '', text).strip()
        print(f"#{i:<2} | {clean_text:<35} | {l}")
