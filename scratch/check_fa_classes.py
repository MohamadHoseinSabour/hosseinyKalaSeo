import re

with open('scratch/live_page.html', 'r', encoding='utf-8') as f:
    text = f.read()

fa_classes = re.findall(r'class=["\'][^"\']*(?:fa-[a-z0-9-]+|fab |fas |far )[^"\']*["\']', text)
print(f"Total FA occurrences in HTML: {len(fa_classes)}")
for c in set(fa_classes[:20]):
    print("  ", c)
