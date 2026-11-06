import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/perfect_audit_summary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('Keys in data:', list(data.keys()))

for k in data.keys():
    val = data[k]
    if isinstance(val, list):
        for item in val:
            item_str = str(item)
            if any(w in item_str for w in ['TOSHIBA', 'توشیبا', 'X.VISJON', 'XVISION', 'ایکس', 'LED', 'ال ای دی']):
                print(f'Found in key "{k}": {item}')
