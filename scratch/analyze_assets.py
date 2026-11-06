import requests
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://hosseinykala.ir/', headers={'User-Agent': 'Mozilla/5.0'})

# Fonts in HTML
font_pattern = r'https?://[^\s\"\'\(\)]+\.(?:woff2?|ttf|eot)'
fonts = re.findall(font_pattern, r.text, re.IGNORECASE)
print('Fonts referenced directly in HTML:', len(fonts))
for f in sorted(set(fonts)):
    print(' ', f)

# Domains referenced in HTML
domains = re.findall(r'https?://([a-zA-Z0-9\.\-]+)/', r.text)
domain_counts = {}
for d in domains:
    domain_counts[d] = domain_counts.get(d, 0) + 1
print('\nTop domains referenced in HTML:')
for d, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f'  {d}: {count}')

# Check combined CSS file size and contents
combined_css_match = re.search(r'https://hosseinykala.ir/wp-content/litespeed/css/[a-zA-Z0-9]+\.css[^\"]*', r.text)
if combined_css_match:
    css_url = combined_css_match.group(0)
    print(f'\nFound combined CSS: {css_url}')
    rcss = requests.get(css_url, headers={'User-Agent': 'Mozilla/5.0'})
    print(f'CSS Status: {rcss.status_code}, Size: {len(rcss.content)/1024:.1f} KB (raw), Headers Content-Encoding: {rcss.headers.get("content-encoding")}')
    css_fonts = re.findall(font_pattern, rcss.text, re.IGNORECASE)
    print(f'Fonts referenced inside combined CSS: {len(set(css_fonts))}')
    for cf in sorted(set(css_fonts))[:10]:
        print('   ', cf)

# Check combined JS file size
combined_js_match = re.search(r'https://hosseinykala.ir/wp-content/litespeed/js/[a-zA-Z0-9]+\.js[^\"]*', r.text)
if combined_js_match:
    js_url = combined_js_match.group(0)
    print(f'\nFound combined JS: {js_url}')
    rjs = requests.get(js_url, headers={'User-Agent': 'Mozilla/5.0'})
    print(f'JS Status: {rjs.status_code}, Size: {len(rjs.content)/1024:.1f} KB (raw), Headers Content-Encoding: {rjs.headers.get("content-encoding")}')
