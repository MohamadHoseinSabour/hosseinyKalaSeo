import urllib.request
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request('https://hosseinykala.ir/contact', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})
with urllib.request.urlopen(req, timeout=15) as r:
    print('Final URL:', r.geturl())
    print('Status:', r.status)
    html = r.read().decode('utf-8', errors='ignore')
    print('HTML length:', len(html))
    title = re.search(r'<title>(.*?)</title>', html)
    print('Title:', title.group(1) if title else None)
    body_class = re.search(r'<body[^>]*class=[\'"]([^\'"]+)[\'"]', html)
    if body_class:
        classes = body_class.group(1).split()
        print('Is home in body class:', 'home' in classes)
        print('Page ID in body class:', [c for c in classes if 'page-id' in c])
        print('Classes sample:', classes[:10])
