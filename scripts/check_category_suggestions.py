import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/live_products_check.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

with open('data/categories.json', 'r', encoding='utf-8') as f:
    cats = json.load(f)

cat_map = {c['id']: c for c in cats}

print("=== Checking all 96 products for category consistency ===")

suggestions = []

for p in sorted(products, key=lambda x: x['id']):
    pid = p['id']
    title = p['title']['rendered']
    p_cats = p.get('product_cat', [])
    cat_names = [f"{cid}:{cat_map.get(cid, {}).get('name', str(cid))}" for cid in p_cats]
    
    # 1. Check ID 2972: Refrigerator in Vacuum Cleaner
    if pid == 2972:
        suggestions.append({
            'id': pid,
            'title': title,
            'current': cat_names,
            'target': [92, 153],
            'target_names': ['یخچال فریزر', 'یخچال فریزر کلور'],
            'reason': 'یخچال کلور به اشتباه در جاروبرقی قرار گرفته است'
        })
        
    # 2. Check ID 3551: Washing Machine in Vacuum Cleaner
    if pid == 3551:
        suggestions.append({
            'id': pid,
            'title': title,
            'current': cat_names,
            'target': [93],
            'target_names': ['ماشین لباسشویی'],
            'reason': 'لباسشویی ریتون به اشتباه در جاروبرقی قرار گرفته است'
        })

    # 3. Check ID 3453: Electrosteel Refrigerator
    if pid == 3453 and 156 not in p_cats:
        suggestions.append({
            'id': pid,
            'title': title,
            'current': cat_names,
            'target': [92, 156],
            'target_names': ['یخچال فریزر', 'یخچال فریزر الکترواستیل'],
            'reason': 'یخچال الکترواستیل باید در دسته برند الکترواستیل (156) نیز باشد'
        })

    # 4. Check ID 3285: Pro Omega Hair Dryer
    if pid == 3285 and 174 not in p_cats:
        suggestions.append({
            'id': pid,
            'title': title,
            'current': cat_names,
            'target': [124, 174],
            'target_names': ['سشوار', 'سشوار پرو امگا'],
            'reason': 'سشوار پرو امگا باید علاوه بر سشوار در دسته برند پرو امگا (174) نیز باشد'
        })

    # 5. Check other Donallex products: do they have donallex subcategories?
    # Donallex categories:
    # 165: آبمیوه گیری دونالکس (parent: 120)
    # 166: اتو بخار دونالکس (parent: 118)
    # 167: اسپرسو ساز دونالکس (parent: 119)
    # 168: سرخ کن دونالکس (parent: 121)
    # 169: گوشت کوب برقی دونالکس (parent: 122)
    # 170: مخلوط کن دونالکس (parent: 123)
    
    # Check 3510 (جاروبرقی دونالکس) -> no donallex vacuum cat exists, so [21] is fine
    # Check 3647 (سرخ‌کن گرنویک) -> [121] is fine
    # Check 3711 (آبمیوه‌گیری دونالکس) -> has [120], should it also have 165?
    if pid == 3711 and 165 not in p_cats:
        suggestions.append({
            'id': pid,
            'title': title,
            'current': cat_names,
            'target': [120, 165],
            'target_names': ['آبمیوه گیری', 'آبمیوه گیری دونالکس'],
            'reason': 'آبمیوه‌گیری دونالکس باید در دسته آبمیوه‌گیری دونالکس (165) نیز باشد'
        })

for s in suggestions:
    print(f"\nID: {s['id']} | {s['title']}")
    print(f"  Current: {s['current']}")
    print(f"  Target: {s['target']} ({s['target_names']})")
    print(f"  Reason: {s['reason']}")
