import sys
import json
import pickle
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('data/raw_parsed_new_list.json', 'r', encoding='utf-8') as f:
    raw_list = json.load(f)

# Let's verify every single item in raw_list
# We will define the exact classification map
ACCOUNTING_IDXS = [17] # wait, which index is 'کسرواضافات کالا'?

for idx, it in enumerate(raw_list, 1):
    if 'کسرواضافات' in it['desc']:
        print(f"Accounting index: #{idx} -> {it['desc']}")
