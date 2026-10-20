import pickle
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/target_data.pkl', 'rb') as f:
    target = pickle.load(f)

# 1. Split Electrosteel from Vegatronix in 'لوازم برقی و پخت و پز'
cooking_brands = target['لوازم برقی و پخت و پز']
veg_blocks = cooking_brands.get('وگاترونیکس', [])
new_veg = []
electrosteel_blocks = []

for blk in veg_blocks:
    if 'الکترواستیل' in blk['name']:
        electrosteel_blocks.append(blk)
    else:
        new_veg.append(blk)

# Reorder cooking brands: وگاترونیکس, الکترواستیل, then the rest
new_cooking = {}
new_cooking['وگاترونیکس'] = new_veg
if electrosteel_blocks:
    new_cooking['الکترواستیل'] = electrosteel_blocks

for b, blks in cooking_brands.items():
    if b != 'وگاترونیکس':
        new_cooking[b] = blks

target['لوازم برقی و پخت و پز'] = new_cooking

# 2. Rename 'متفرقه' in 'زیبایی و سلامت فردی' to 'بای بابلیس نانو'
beauty_brands = target['زیبایی و سلامت فردی']
new_beauty = {}
for b, blks in beauty_brands.items():
    if b == 'متفرقه':
        new_beauty['بای بابلیس نانو'] = blks
    else:
        new_beauty[b] = blks
target['زیبایی و سلامت فردی'] = new_beauty

with open('scratch/target_data.pkl', 'wb') as f:
    pickle.dump(target, f)

print("✓ Successfully updated target_data.pkl with separate brand sections!")
