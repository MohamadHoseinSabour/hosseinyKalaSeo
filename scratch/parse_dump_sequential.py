# Parse sequential blocks from scratch/catalog_full_dump.txt

dump_lines = open('scratch/catalog_full_dump.txt', encoding='utf-8').readlines()

sheets = {}
cur_sheet = None
cur_block = None
cur_section = None

for line in dump_lines:
    if 'SHEET:' in line:
        cur_sheet = line.split('SHEET:')[1].split()[0].strip()
        sheets[cur_sheet] = []
        continue
    if '| A: ' in line and '| B: ' in line:
        parts = line.split('|')
        name = parts[1].replace('A:', '').strip()
        price_b = parts[2].replace('B:', '').strip()
        price_d = parts[3].replace('D:', '').strip()
        status_r = parts[4].replace('R:', '').strip()
        
        b_val = int(price_b) if price_b != 'None' and price_b.isdigit() else None
        d_val = int(price_d) if price_d != 'None' and price_d.isdigit() else (b_val if b_val else None)
        
        if '📂' in name:
            cur_section = name
            continue
            
        if name.startswith('↳'):
            if cur_block:
                cur_block['variations'].append({
                    'name': name,
                    'price_b': b_val,
                    'price_d': d_val,
                    'status_r': status_r
                })
        else:
            cur_block = {
                'section': cur_section,
                'name': name,
                'price_b': b_val,
                'price_d': d_val,
                'status_r': status_r,
                'variations': []
            }
            sheets[cur_sheet].append(cur_block)

total_blocks = sum(len(b) for b in sheets.values())
total_variations = sum(sum(len(b['variations']) for b in s_blocks) for s_blocks in sheets.values())
total_priced = sum(
    sum((1 if b['price_b'] else 0) + sum(1 if v['price_b'] else 0 for v in b['variations']) for b in s_blocks)
    for s_blocks in sheets.values()
)

print(f"Parsed from dump:")
print(f"Total blocks: {total_blocks}")
print(f"Total variations: {total_variations}")
print(f"Total priced items: {total_priced}")
