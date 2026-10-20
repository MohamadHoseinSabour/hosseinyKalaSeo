import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/posts/3851', auth=AUTH, headers=HEADERS)
data = r.json()
content = data.get('content', {}).get('raw') or data.get('content', {}).get('rendered', '')

with open('data/post_3851_current_content.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Post 3851 length: {len(content)} characters. Saved to data/post_3851_current_content.html")
