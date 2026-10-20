import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

try:
    with open('data/thin_live_products.json', 'r', encoding='utf-8') as f:
        prods = json.load(f)
    print(f'Total in thin_live_products.json: {len(prods)}')
    for p in prods:
        name = p.get('name', '')
        for kw in ['فر', 'الکترواستیل', 'وگاترونیکس', 'توستر', '290', '۲۹۰', 'دونالکس', 'هواپز', 'سرخکن', 'سرخ کن', 'اپولاتور', 'اپیلاتور', 'شیور', 'پتوشور', 'پاکیزان']:
            if kw in name:
                print(f"ID {p.get('id')} | kw={kw} | {name}")
                break
except Exception as e:
    print('Error:', e)
