import urllib.request
import gzip
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

for u in ['https://hosseinykala.ir/contact', 'https://hosseinykala.ir/contact/']:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Accept-Encoding': 'gzip'})
    with urllib.request.urlopen(req) as r:
        data = r.read()
        if r.headers.get('content-encoding') == 'gzip':
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        print(f"\nURL: {u}")
        print("Length:", len(text))
        print("Canonical link:", re.findall(r'<link[^>]*rel=[\'"]canonical[\'"][^>]*>', text))
        print("Body classes:", re.findall(r'<body[^>]*class=[\'"]([^\'"]+)[\'"]', text))
        print("First 300 chars of body:", re.search(r'<body[^>]*>(.*?)', text, re.DOTALL).group(0)[:300] if '<body' in text else "No body")
