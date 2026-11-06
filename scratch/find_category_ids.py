import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/categories.json', 'r', encoding='utf-8') as f:
    cats = json.load(f)

for c in cats:
    slug = c.get('slug', '')
    if any(x in slug for x in ['bost', 'electrosteel', 'eastcool', 'clover', 'donallex', 'pro-omega', 'reyton']):
        print(f"ID: {c.get('id')} | Slug: {slug} | Name: {c.get('name')}")
