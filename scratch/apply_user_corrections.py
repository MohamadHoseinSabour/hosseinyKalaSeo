import pickle
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/target_data.pkl', 'rb') as f:
    target = pickle.load(f)

# 1. Check Clover in laundry
clover_washers = target['شستشو و نظافت']['کلور']
print("Clover blocks in laundry before fix:")
for idx, b in enumerate(clover_washers):
    print(f"  {idx}: {b['name']} ({b.get('status_r')})")

# Remove 'ماشین لباسشویی 8 کیلویی کلور مدل 8vw1 سفید'
target['شستشو و نظافت']['کلور'] = [b for b in clover_washers if '8vw1' not in b['name']]
print(f"Clover blocks after removing 8vw1: {len(target['شستشو و نظافت']['کلور'])}")

# 2. Check Electrosteel and متفرقه in یخچال و فریزر
fridge_electro = target['یخچال و فریزر']['الکترواستیل']
print("\nElectrosteel blocks in fridge before fix:")
for idx, b in enumerate(fridge_electro):
    print(f"  {idx}: {b['name']} ({b.get('status_r')})")

# Remove 'متفرقه' from یخچال و فریزر completely
if 'متفرقه' in target['یخچال و فریزر']:
    del target['یخچال و فریزر']['متفرقه']
    print("Removed 'متفرقه' brand completely from یخچال و فریزر.")

# Remove any existing 27 or 35 foot if already added under electrosteel, then add correctly
target['یخچال و فریزر']['الکترواستیل'] = [
    b for b in target['یخچال و فریزر']['الکترواستیل'] 
    if '27 فوت تیتانیوم' not in b['name'] and '35 فوت' not in b['name'] and '34 فوت' not in b['name']
]

# Add the two corrected Electrosteel fridges:
# 1. یخچال و فریزر 27 فوت الکترواستیل تیتانیوم
target['یخچال و فریزر']['الکترواستیل'].append({
    'section': '📂 یخچال و فریزر  ◀  الکترواستیل',
    'name': 'یخچال و فریزر 27 فوت الکترواستیل تیتانیوم',
    'price_b': None,
    'price_d': None,
    'status_r': 'در سایت تعریف نشده',
    'in_stock': '✓ موجود',
    'variations': []
})

# 2. یخچال و فریزر 34 فوت هوم بار الکترواستیل سفید (corrected from 35 to 34)
target['یخچال و فریزر']['الکترواستیل'].append({
    'section': '📂 یخچال و فریزر  ◀  الکترواستیل',
    'name': 'یخچال و فریزر 34 فوت هوم بار الکترواستیل سفید',
    'price_b': None,
    'price_d': None,
    'status_r': 'در سایت تعریف نشده',
    'in_stock': '✓ موجود',
    'variations': []
})

print("\nElectrosteel blocks in fridge after fix:")
for idx, b in enumerate(target['یخچال و فریزر']['الکترواستیل']):
    print(f"  {idx}: {b['name']} ({b.get('status_r')})")

with open('scratch/target_data.pkl', 'wb') as f:
    pickle.dump(target, f)

print("\n✓ target_data.pkl updated successfully with all user corrections!")
