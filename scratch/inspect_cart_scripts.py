import requests
import re

r = requests.get('https://hosseinykala.ir/cart/', headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
text = r.text

matches = [m.start() for m in re.finditer(r'wp\.i18n', text)]
print("wp.i18n matches in cart:", len(matches))
for idx in matches:
    print("\n--- Context ---")
    print(text[max(0, idx-100):min(len(text), idx+250)])

# Also search for wp-i18n script tag
m_sc = re.findall(r'<script[^>]*wp-i18n[^>]*>', text)
print("\nwp-i18n script tags:", m_sc)
m_wp = re.findall(r'<script[^>]*wp-polyfill[^>]*>', text)
print("wp-polyfill script tags:", m_wp)
m_hooks = re.findall(r'<script[^>]*wp-hooks[^>]*>', text)
print("wp-hooks script tags:", m_hooks)
