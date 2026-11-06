import re

with open('divar_test.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'src="(https://[^"]+\.js[^"]*)"', html)
print(f"Found {len(scripts)} scripts:")
for s in scripts:
    print(s)
