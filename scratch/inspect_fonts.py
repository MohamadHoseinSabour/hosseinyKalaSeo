import requests
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Check the combined CSS file
css_url = 'https://hosseinykala.ir/wp-content/litespeed/css/c325ba86cf3ddb9dfc1aa8a7ac7eafbe.css?ver=60de8'
r = requests.get(css_url)
print("CSS Size:", len(r.text) / 1024, "KB")

font_faces = re.findall(r'@font-face\s*\{([^}]+)\}', r.text)
print(f"Total @font-face rules found in combined CSS: {len(font_faces)}")
for idx, ff in enumerate(font_faces[:10]):
    print(f"\nFont #{idx+1}:")
    for line in ff.split(';'):
        line = line.strip()
        if any(k in line for k in ['font-family', 'font-display', 'font-weight', 'src']):
            print("  ", line[:100])
