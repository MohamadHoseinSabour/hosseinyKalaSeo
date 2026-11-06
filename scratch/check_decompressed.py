import gzip
import re

with open('scratch/contact_raw.txt', 'rb') as f:
    raw = f.read()

try:
    decompressed = gzip.decompress(raw).decode('utf-8', errors='ignore')
    print("Decompressed length:", len(decompressed))
    title = re.search(r'<title>(.*?)</title>', decompressed)
    print("Title:", title.group(1) if title else "NO TITLE")
    h1 = re.search(r'<h[1-2][^>]*>(.*?)</h[1-2]>', decompressed)
    print("H1/H2:", h1.group(1) if h1 else "NO H1")
    body_class = re.search(r'<body[^>]*class=[\'"]([^\'"]+)[\'"]', decompressed)
    print("Body classes:", body_class.group(1) if body_class else "NO CLASS")
except Exception as e:
    print("Decompress error:", e)
