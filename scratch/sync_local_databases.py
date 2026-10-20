# -*- coding: utf-8 -*-
"""
sync_local_databases.py
=======================
همگام‌سازی دیتابیس‌های محلی پروژه (data/id_mappings.json و data/products.json)
با محصولات جدید ایجاد شده در سایت.
"""

import os
import sys
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROGRESS_FILE = 'scratch/creation_progress.json'
PLAN_FILE = 'scratch/all_61_products.json'
ID_MAPPINGS_FILE = 'data/id_mappings.json'
PRODUCTS_FILE = 'data/products.json'

def sync_dbs():
    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        progress = json.load(f)
        
    with open(PLAN_FILE, 'r', encoding='utf-8') as f:
        plan = json.load(f)
        
    # 1. Update id_mappings.json
    id_mappings = {}
    if os.path.exists(ID_MAPPINGS_FILE):
        with open(ID_MAPPINGS_FILE, 'r', encoding='utf-8') as f:
            id_mappings = json.load(f)
            
    # 2. Update products.json
    products = []
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            products = json.load(f)
            
    existing_pids = {p.get('id') for p in products}
    
    plan_dict = {p['name']: p for p in plan}
    
    added_count = 0
    for name, pinfo in progress.items():
        pid = pinfo.get('product_id')
        if not pid:
            continue
            
        slug = pinfo.get('slug')
        ptype = pinfo.get('type')
        meta = plan_dict.get(name, {})
        
        # Add to id_mappings
        id_mappings[str(pid)] = {
            'name': name,
            'slug': slug,
            'type': ptype,
            'url': f"https://hosseinykala.ir/product/{slug}/",
            'price': meta.get('price_rial')
        }
        
        # Add to products.json if not present
        if pid not in existing_pids:
            new_prod_obj = {
                'product_id': pid,
                'id': pid,
                'name': name,
                'slug': slug,
                'url': f"https://hosseinykala.ir/product/{slug}/",
                'shortlink': f"https://hosseinykala.ir/?p={pid}",
                'type': ptype,
                'price': str(meta.get('price_rial') or ''),
                'price_regular': str(meta.get('price_rial') or ''),
                'price_sale': '',
                'in_stock': False,
                'stock_status': 'outofstock',
                'category': meta.get('primary_cat_name', ''),
                'categories': [meta.get('primary_cat_name', '')],
                'sku': '',
                'variations_count': len(pinfo.get('variations', [])),
                'variations': pinfo.get('variations', [])
            }
            products.append(new_prod_obj)
            existing_pids.add(pid)
            added_count += 1
            
    with open(ID_MAPPINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(id_mappings, f, ensure_ascii=False, indent=2)
        
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
        
    print(f"==================================================")
    print(f"همگام‌سازی دیتابیس‌های محلی با موفقیت انجام شد:")
    print(f"  ✓ به روزرسانی {ID_MAPPINGS_FILE}")
    print(f"  ✓ افزودن {added_count} محصول جدید به {PRODUCTS_FILE}")
    print(f"==================================================")

if __name__ == '__main__':
    sync_dbs()
