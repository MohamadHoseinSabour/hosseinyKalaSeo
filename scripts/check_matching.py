import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/matching_pass1.json', 'r', encoding='utf-8') as f:
    m1 = json.load(f)

print("matching_pass1 keys:", list(m1.keys()))
for idx in [0, 1, 34, 35, 38]:
    if idx < len(m1.get('items', [])):
        print(f"Item {idx}:", m1['items'][idx])
    else:
        # maybe dict by index
        print(f"Index {idx} in m1:", m1.get(str(idx)))

with open('scratch/final_classified_audit.json', 'r', encoding='utf-8') as f:
    fc = json.load(f)

print("\nfinal_classified_audit keys:", list(fc.keys()))
for k, v in fc.items():
    if isinstance(v, list):
        for item in v:
            t = str(item)
            if 'L2300EE' in t or 'هایسنس' in t:
                print(f"Found in {k}:", item)
