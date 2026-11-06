import os
import sys
import json
import re
import openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"

wb = openpyxl.load_workbook(os.path.join(PROJECT_DIR, 'hosseiny_kala_catalog.xlsx'), data_only=True)
prods = json.load(open(os.path.join(PROJECT_DIR, 'data', 'products.json'), encoding='utf-8'))

print("=== CHECKING FOR TYPOS IN CATALOG ===")
catalog_issues = []
for s in wb.sheetnames[1:9]:
    ws = wb[s]
    for r in range(2, ws.max_row + 1):
        if type(ws.cell(r, 2)).__name__ == 'MergedCell' or type(ws.cell(r, 3)).__name__ == 'MergedCell':
            continue
        name = str(ws.cell(r, 1).value or '').strip()
        brand = str(ws.cell(r, 11).value or '').strip()
        sku = str(ws.cell(r, 17).value or '').strip()
        pid = ws.cell(r, 14).value
        vid = ws.cell(r, 15).value

        # Checks
        if 'baby3383a' in name.lower():
            catalog_issues.append((s, r, 'baby3383a در نام محصول', name, pid, vid))
        if 'دیپونت' in name or 'دیپونت' in brand:
            catalog_issues.append((s, r, 'دیپونت به جای دیپوینت', name, pid, vid))
        if 'فلیپس' in name or 'فلیپس' in brand:
            catalog_issues.append((s, r, 'فلیپس به جای فیلیپس', name, pid, vid))
        if 'وستینگهوس' in name or 'وستینگهوس' in brand:
            catalog_issues.append((s, r, 'وستینگهوس به جای وستینگهاوس', name, pid, vid))
        if 'افریزر' in name:
            catalog_issues.append((s, r, 'افریزر به جای فریزر', name, pid, vid))
        if 'ایخچال' in name:
            catalog_issues.append((s, r, 'ایخچال به جای یخچال', name, pid, vid))
        if 'اینج' in name:
            catalog_issues.append((s, r, 'اینج به جای اینچ', name, pid, vid))
        if 'r)re01(' in name.lower() or 'r)re01(' in str(ws.cell(r, 13).value or '').lower():
            catalog_issues.append((s, r, 'r)re01( کد مدل اشتباه', name, pid, vid))
        if '&amp;' in name:
            catalog_issues.append((s, r, '&amp; کاراکتر HTML خام', name, pid, vid))
        if 'BOOS' in name or 'boos' in sku.lower():
            catalog_issues.append((s, r, 'BOOS به جای Boss', name, pid, vid))

print(f"Catalog issues found: {len(catalog_issues)}")
for ci in catalog_issues:
    print(f"  [{ci[0]} R{ci[1]}] {ci[2]} -> Name: \"{ci[3]}\" (PID: {ci[4]}, VID: {ci[5]})")

print("\n=== CHECKING FOR TYPOS ON SITE (products.json) ===")
site_issues = []
for p in prods:
    pid = p['id']
    name = p['name']
    slug = p['slug']
    
    if 'baby3383a' in name.lower() or 'baby3383a' in slug.lower():
        site_issues.append((pid, 'baby3383a در عنوان یا اسلاگ', name, slug))
    if 'دیپونت' in name or 'دیپونت' in slug:
        site_issues.append((pid, 'دیپونت به جای دیپوینت', name, slug))
    if 'فلیپس' in name or 'فلیپس' in slug:
        site_issues.append((pid, 'فلیپس به جای فیلیپس', name, slug))
    if 'وستینگهوس' in name or 'وستینگهوس' in slug:
        site_issues.append((pid, 'وستینگهوس به جای وستینگهاوس', name, slug))
    if 'افریزر' in name:
        site_issues.append((pid, 'افریزر به جای فریزر', name, slug))
    if 'ایخچال' in name:
        site_issues.append((pid, 'ایخچال به جای یخچال', name, slug))
    if 'اینج' in name:
        site_issues.append((pid, 'اینج به جای اینچ', name, slug))
    if '&amp;' in name or '&quot;' in name:
        site_issues.append((pid, 'کاراکتر HTML خام در عنوان', name, slug))
    if '44 فوت' in name and '54 فوت' in name:
        site_issues.append((pid, 'تناقض ۴۴ فوت و ۵۴ فوت در عنوان', name, slug))
    if 'BOOS' in name or 'boos' in slug.lower():
        site_issues.append((pid, 'BOOS به جای Boss', name, slug))

print(f"Site issues found: {len(site_issues)}")
for si in site_issues:
    print(f"  [Site PID {si[0]}] {si[1]} -> Name: \"{si[2]}\" (Slug: {si[3]})")
