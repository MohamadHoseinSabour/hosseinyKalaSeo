import json
import openpyxl

with open('data/raw_parsed_new_list.json', 'r', encoding='utf-8') as f:
    raw_list = json.load(f)

import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from scratch.inspect_all_255_matches import find_match

actions = []
for idx, it in enumerate(raw_list):
    m_type, data = find_match(it)
    if m_type not in ['EXISTING', 'ACCOUNTING']:
        actions.append((idx + 1, m_type, it['desc'], it['qty'], data))

print(f"Total new action items: {len(actions)}")
for idx, m_type, desc, qty, data in actions:
    print(f"#{idx} [{m_type}] Qty={qty} | {desc}")
    print(f"    --> {data}")
