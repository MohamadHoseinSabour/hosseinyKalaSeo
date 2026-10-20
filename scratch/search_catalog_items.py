import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('scratch/catalog_current_rows.json', encoding='utf-8') as f:
    rows = json.load(f)

def find_item(kw):
    found = [r for r in rows if kw.lower() in r['name'].lower()]
    for r in found:
        sheet = r['sheet']
        row = r['row']
        brand = r['brand']
        name = r['name']
        status = r['status']
        is_var = r['is_variation']
        print(f"[{sheet} | Row {row}] [{brand}] {name} --> Status: {status}, is_var: {is_var}")

for term in ['امگا', '5 کاره', '850', '990', '770', '181', 'بوتان', 'سانی', 'آیس پول', 'اکونومی', 'روسو']:
    print(f"--- Search: {term} ---")
    find_item(term)
