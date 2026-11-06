import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Total products in data/products.json: {len(products)}")

with_price = []
sale_prods = []

for p in products:
    p_price = p.get('price')
    try:
        p_val = float(p_price) if p_price else 0
    except:
        p_val = 0
    if p_val > 0:
        with_price.append(p)
    
    p_sale = p.get('sale_price')
    try:
        s_val = float(p_sale) if p_sale else 0
    except:
        s_val = 0
    if s_val > 0:
        sale_prods.append((p, s_val))

print(f"Products with price > 0: {len(with_price)}")
print(f"Products with sale_price > 0: {len(sale_prods)}")

for p, s_val in sale_prods[:15]:
    reg = float(p.get('regular_price') or 0)
    ratio = (reg - s_val) / reg if reg > 0 else 0
    print(f"PID {p['id']}: reg={reg:,.0f}, sale={s_val:,.0f}, discount={ratio*100:.1f}%, name={p['name']}")
