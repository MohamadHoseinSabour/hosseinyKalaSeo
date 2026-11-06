import re, sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/site_backup_page.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for m in re.finditer(r'<form action="([^"]+)"[^>]*method="([^"]+)"', text, re.I):
    print('Action:', m.group(1), 'Method:', m.group(2))

inputs = re.findall(r'<input[^>]+>', text)
for inp in inputs:
    print('Input:', inp)
