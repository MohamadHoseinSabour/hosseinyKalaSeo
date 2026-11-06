import urllib.request
import re

req = urllib.request.Request('https://pagespeed.web.dev/analysis/https-hosseinykala-ir/p31vkp5f3e?form_factor=mobile', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode('utf-8')

for s in re.finditer(r'<script[^>]*>(.*?)</script>', html, re.DOTALL):
    text = s.group(1)
    if 'lighthouseResult' in text:
        idx = text.find('lighthouseResult')
        print("Snippet around lighthouseResult:")
        print(text[max(0, idx - 50):idx + 250])
