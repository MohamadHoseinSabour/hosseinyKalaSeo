import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('data/raw_parsed_new_list.json', 'r', encoding='utf-8') as f:
    raw_list = json.load(f)
valid = [x for x in raw_list if x.get('name')]
print('Valid count:', len(valid))
for idx, item in enumerate(valid, 1):
    print(f"{idx}. {item.get('name')} -> ID: {item.get('site_id')}")
