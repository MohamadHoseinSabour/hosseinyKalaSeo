import urllib.request
import gzip
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request('https://hosseinykala.ir/contact/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Accept-Encoding': 'gzip'})
with urllib.request.urlopen(req) as r:
    data = r.read()
    if r.headers.get('content-encoding') == 'gzip':
        data = gzip.decompress(data)
    text = data.decode('utf-8', errors='ignore')

with open('scratch/contact_raw.txt', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved scratch/contact_raw.txt, length:", len(text))
print("First 500 chars:")
print(repr(text[:500]))
