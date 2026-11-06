import sys
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/matching_pass1.json', 'r', encoding='utf-8') as f:
    d = json.load(f)['unmatched']

print(f"=== UNMATCHED ITEMS ({len(d)}) ===")
for it in d:
    print(f"[{it['index']:3d}] {it['raw_title']} (تعداد: {it['qty']})")
