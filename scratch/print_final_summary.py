import sys
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/final_classified_audit.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print('=== 29 EXISTING ITEMS WITH DISCREPANCIES ===')
for e in d['existing_errors']:
    print(f"[#{e['index']}] {e['raw_title']}")
    for disc in e['discrepancies']:
        print(f"    - {disc[0]}: '{disc[1]}' -> اصلاح استاندارد: '{disc[2]}'")

print(f"\n=== 48 NEW PRODUCTS (BY CATEGORY) ===")
by_cat = {}
for n in d['new_items']:
    by_cat.setdefault(n['category'], []).append(n)

for cat, items in by_cat.items():
    print(f"\n📁 دسته‌بندی: {cat} ({len(items)} محصول)")
    for n in items:
        print(f"  [#{n['index']:3d}] {n['raw_title']:<40} | برند: {n['brand']:<12} | موجودی: {n['qty']}")
