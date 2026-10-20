import openpyxl
import pickle
import copy
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from collections import OrderedDict
import sys

# 1. Load target_data.pkl
with open('scratch/target_data.pkl', 'rb') as f:
    target = pickle.load(f)

# 2. Modify target according to user answers:

# --- In شستشو و نظافت ---
# Remove draft 3840 (this completely eliminates 'متفرقه' from laundry!)
if 'متفرقه' in target['شستشو و نظافت']:
    del target['شستشو و نظافت']['متفرقه']

# --- In لوازم برقی و پخت و پز ---
# Find KST kettle, remove duplicate 4101 and duplicate toaster 60L
kst_cooking_block = None
filtered_cooking_motafareghe = []
if 'متفرقه' in target['لوازم برقی و پخت و پز']:
    for b in target['لوازم برقی و پخت و پز']['متفرقه']:
        name = b['name']
        if '604' in name:
            b['name'] = 'کتری و قوری روگازی هرمی ۵ لیتری کی اس تی مدل 604 استیل طلا'
            kst_cooking_block = b
        elif 'سرویس قابلمه استیل 10 پارچه' in name:
            # Duplicate of 3354 -> delete
            print("Deleting duplicate 4101 block from cooking")
        elif 'توستر نان و شیرینی 60 لیتر' in name:
            # Duplicate of Vegatronix -> delete
            print("Deleting duplicate toaster 60L from cooking")
        else:
            filtered_cooking_motafareghe.append(b)
    
    if filtered_cooking_motafareghe:
        target['لوازم برقی و پخت و پز']['متفرقه'] = filtered_cooking_motafareghe
    else:
        del target['لوازم برقی و پخت و پز']['متفرقه']

if kst_cooking_block:
    target['لوازم برقی و پخت و پز']['کی اس تی (KST)'] = [kst_cooking_block]

# Also update Dasti Luxe block name
if 'دستی لوکس' in target['لوازم برقی و پخت و پز']:
    for b in target['لوازم برقی و پخت و پز']['دستی لوکس']:
        b['name'] = 'سرویس پخت و پز ۱۰ پارچه تمام استیل دستی لوکس اینداکشن'

# --- In نوشیدنی ساز ---
# Move KST 604 from متفرقه to 'کی اس تی (KST)'
if 'متفرقه' in target['نوشیدنی ساز']:
    kst_bev_block = None
    rem_bev = []
    for b in target['نوشیدنی ساز']['متفرقه']:
        if '604' in b['name']:
            b['name'] = 'ست کتری و قوری هرمی کی اس تی مدل 604 تمام طلا'
            kst_bev_block = b
        else:
            rem_bev.append(b)
    if rem_bev:
        target['نوشیدنی ساز']['متفرقه'] = rem_bev
    else:
        del target['نوشیدنی ساز']['متفرقه']
        
    if kst_bev_block:
        target['نوشیدنی ساز']['کی اس تی (KST)'] = [kst_bev_block]

# Re-save target_data.pkl
with open('scratch/target_data.pkl', 'wb') as f:
    pickle.dump(target, f)

print("Updated target data successfully!")
for sname, bdict in target.items():
    print(f"Sheet '{sname}': {len(bdict)} brand sections, brands: {list(bdict.keys())}")
