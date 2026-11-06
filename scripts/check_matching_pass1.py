import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/matching_pass1.json', 'r', encoding='utf-8') as f:
    m1 = json.load(f)

for item in m1.get('matched', []):
    t = str(item)
    if any(w in t for w in ['TOSHIBA', 'توشیبا', 'X.VISJON', 'L2300EE', 'هایسنس']):
        print("Matched:", item)

for item in m1.get('unmatched', []):
    t = str(item)
    if any(w in t for w in ['TOSHIBA', 'توشیبا', 'X.VISJON', 'L2300EE', 'هایسنس']):
        print("Unmatched:", item)
