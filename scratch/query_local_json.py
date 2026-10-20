import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print('=== 1. OVEN / TOASTER / VEGATRONIX / ELECTROSTEEL ===')
for p in products:
    text = (p.get('name', '') + ' ' + p.get('description', '') + ' ' + p.get('short_description', '')).lower()
    if 'وگاترونیکس' in text or 'vegatronix' in text or 'توستر' in text or 'فر برقی' in text or 'الکترواستیل' in text or 'آون' in text:
        cats = [c.get('name') for c in p.get('categories', [])]
        print(f"ID: {p.get('id')} | Name: {p.get('name')} | Slug: {p.get('slug')} | Cats: {cats}")

print('\n=== 2. 290 / DONALEX ===')
for p in products:
    name = p.get('name', '')
    if '290' in name or '۲۹۰' in name:
        print(f"ID: {p.get('id')} | Name: {p.get('name')} | Slug: {p.get('slug')}")

print('\n=== 3. AIR FRYER / HAVAPAZ ===')
for p in products:
    name = p.get('name', '')
    if 'هواپز' in name or 'سرخ' in name:
        print(f"ID: {p.get('id')} | Name: {p.get('name')} | Slug: {p.get('slug')}")

print('\n=== 4. EPILATOR / SHAVER ===')
for p in products:
    name = p.get('name', '')
    if 'اپیلاتور' in name or 'اپولاتور' in name or 'شیور' in name:
        print(f"ID: {p.get('id')} | Name: {p.get('name')} | Slug: {p.get('slug')}")

print('\n=== 5. BLANKET WASHER / PAKIZAN ===')
for p in products:
    name = p.get('name', '')
    if 'پتوشور' in name or 'پاکیزان' in name:
        print(f"ID: {p.get('id')} | Name: {p.get('name')} | Slug: {p.get('slug')} | Price: {p.get('price')} | Reg: {p.get('regular_price')} | Stock: {p.get('stock_status')}")
