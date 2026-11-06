import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/live_page.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = [m.start() for m in re.finditer(r'square-banner', text)]
print(f"Total occurrences of square-banner: {len(matches)}")
for i, idx in enumerate(matches[:5]):
    print(f"\n--- Occurrence {i+1} ---")
    snippet = text[max(0, idx-250):min(len(text), idx+350)]
    print(snippet)
