import urllib.request
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

for name, url in [('Product', 'https://hosseinykala.ir/product/depoint-decent-combi-refrigerator-freezer/'), ('Contact', 'https://hosseinykala.ir/contact/')]:
    print(f"\n--- Scripts on {name} ---")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone)'})
    with urllib.request.urlopen(req, timeout=15) as r:
        html = r.read().decode('utf-8', errors='ignore')
        
    scripts = re.findall(r'<script([^>]*)>', html)
    for s in scripts:
        src = re.search(r'src=[\'"]([^\'"]+)[\'"]', s)
        if src:
            src_val = src.group(1).split('/')[-1].split('?')[0]
            is_defer = 'defer' in s
            is_async = 'async' in s
            print(f"  {src_val:<35} | defer={is_defer} | async={is_async}")
