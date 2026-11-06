import urllib.request
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

url = 'https://hosseinykala.ir/contact'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'fa,en-US;q=0.7,en;q=0.3'
})
with urllib.request.urlopen(req, timeout=15) as r:
    final_url = r.geturl()
    html = r.read().decode('utf-8', errors='ignore')
    print('Requested:', url)
    print('Final URL:', final_url)
    print('Status:', r.status)
    print('Cache header:', r.headers.get('x-hosseinykala-cache'))
    
    title = re.search(r'<title>(.*?)</title>', html)
    print('Title:', title.group(1) if title else 'No title')
    
    body_class = re.search(r'<body[^>]*class=[\'"]([^\'"]+)[\'"]', html)
    if body_class:
        classes = body_class.group(1).split()
        print('Is home in body class:', 'home' in classes)
        print('Page classes:', [c for c in classes if 'page' in c or 'home' in c])
