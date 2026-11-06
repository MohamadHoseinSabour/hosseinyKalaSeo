import requests
import re

r = requests.get('https://hosseinykala.ir/', headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
text = r.text

for target in ['wp-i18n-js-after', 'elementor-common-js-translations', 'jQuery']:
    matches = [m.start() for m in re.finditer(target, text)]
    print(f"Target '{target}': {len(matches)} occurrences")
    for idx in matches[:3]:
        print(f"\n--- Context for '{target}' ---")
        print(text[max(0, idx-100):min(len(text), idx+250)])
