from bs4 import BeautifulSoup
import re

with open('scratch/live_page.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

inline_scripts = soup.find_all('script', src=False)
print(f"Total inline scripts: {len(inline_scripts)}")

has_direct_jquery = []
for i, s in enumerate(inline_scripts):
    code = s.get_text()
    if ('jQuery(' in code or '$(' in code) and 'document.addEventListener' not in code and 'window.addEventListener' not in code:
        has_direct_jquery.append((i, code[:200].strip()))

print(f"Inline scripts with immediate jQuery/dollar: {len(has_direct_jquery)}")
for idx, snippet in has_direct_jquery[:10]:
    print(f"\nScript #{idx}:")
    print(snippet)
