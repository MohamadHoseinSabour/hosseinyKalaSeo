import requests
from bs4 import BeautifulSoup
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}
r = requests.get('https://hosseinykala.ir/', headers=headers)
html = r.text

print(f"Total HTML Characters: {len(html)}")

# Inline scripts
scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', html, re.DOTALL)
total_inline_js = sum(len(s) for s in scripts)
print(f"Inline Scripts count: {len(scripts)}, Total Size: {total_inline_js/1024:.1f} KB")

# Inline styles
styles = re.findall(r'<style\b[^>]*>(.*?)</style>', html, re.DOTALL)
total_inline_css = sum(len(s) for s in styles)
print(f"Inline Styles count: {len(styles)}, Total Size: {total_inline_css/1024:.1f} KB")

# SVGs
svgs = re.findall(r'<svg\b[^>]*>(.*?)</svg>', html, re.DOTALL)
total_svg = sum(len(s) for s in svgs)
print(f"Inline SVGs count: {len(svgs)}, Total Size: {total_svg/1024:.1f} KB")

# Largest inline scripts
print("\nTop 5 Largest Inline Scripts:")
sorted_scripts = sorted(scripts, key=len, reverse=True)[:5]
for idx, s in enumerate(sorted_scripts):
    print(f"Script #{idx+1}: {len(s)/1024:.1f} KB | Preview: {s[:150].strip()}...")

# Largest inline styles
print("\nTop 5 Largest Inline Styles:")
sorted_styles = sorted(styles, key=len, reverse=True)[:5]
for idx, s in enumerate(sorted_styles):
    print(f"Style #{idx+1}: {len(s)/1024:.1f} KB | Preview: {s[:150].strip()}...")
