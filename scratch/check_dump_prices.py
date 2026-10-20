import openpyxl
from parse_dump_sequential import sheets

# In parse_dump_sequential, `sheets` has every block with its exact name, price_b, price_d, variations (each with name, price_b, price_d)
# Let's verify how many priced items each sheet in dump had:
for sname, blist in sheets.items():
    priced = sum((1 if b['price_b'] else 0) + sum(1 if v['price_b'] else 0 for v in b['variations']) for b in blist)
    print(f"Sheet '{sname}': {len(blist)} blocks, {priced} priced items.")
