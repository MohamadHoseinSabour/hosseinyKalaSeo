import sys
import pickle
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/target_data.pkl', 'rb') as f:
    target = pickle.load(f)

with open('data/raw_parsed_new_list.json', 'r', encoding='utf-8') as f:
    raw_list = json.load(f)

def to_en(t):
    for f, e in zip('۰۱۲۳۴۵۶۷۸۹', '0123456789'):
        t = t.replace(f, e)
    return t

def norm(t):
    if not t: return ''
    t = to_en(str(t).lower())
    t = t.replace('ي', 'ی').replace('ك', 'ک').replace('‌', ' ').replace('-', ' ').replace('_', ' ')
    t = re.sub(r'[\(\)\[\]\.\,\/\+\:]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

# Build a flattened searchable list from target
catalog_items = []
for sname, brands in target.items():
    for bname, blocks in brands.items():
        for b in blocks:
            b_name = b['name']
            catalog_items.append({
                'sheet': sname,
                'brand': bname,
                'block': b,
                'name': b_name,
                'norm_name': norm(b_name),
                'is_variation': False,
                'parent': None
            })
            for v in b['variations']:
                v_name = v['name']
                catalog_items.append({
                    'sheet': sname,
                    'brand': bname,
                    'block': b,
                    'name': f"{b_name} | {v_name}",
                    'norm_name': norm(f"{b_name} {v_name}"),
                    'is_variation': True,
                    'parent': b,
                    'variation': v
                })

print(f"Total catalog entries (parents + variations): {len(catalog_items)}")

matched_indices = {}
unmatched_items = []
accounting_items = []

for idx, it in enumerate(raw_list, start=1):
    desc = it['desc']
    qty = it['qty']
    if 'کسرواضافات' in desc:
        accounting_items.append((idx, it))
        continue
    
    nd = norm(desc)
    
    # 1. Exact or very strong heuristic matching
    best_match = None
    
    # Custom known rules
    # Daewoo 7000
    if 'دوو' in nd and '7000' in nd:
        pass # NEW
    # General Fit
    elif 'جنرال فیت' in nd:
        pass # NEW
    # Bach
    elif 'باخ' in nd and '1454' in nd:
        pass # NEW
    # Clever 8vw1
    elif 'کلور' in nd and '8vw1' in nd:
        pass # NEW
    # Panasonic 650 iron
    elif 'پاناسونیک' in nd and '650' in nd:
        pass # NEW
    # Kenwood citrus juicer
    elif 'کنوود' in nd and 'مرکبات' in nd:
        pass # NEW
    # Iran Shargh
    elif 'ایران شرق' in nd:
        pass # NEW
    # Absal 405
    elif 'آبسال' in nd and '405' in nd:
        pass # NEW
    # Polar stone
    elif 'پلار' in nd and 'سنگ' in nd:
        pass # NEW
    # Maier grinder
    elif 'مایر' in nd and 'آسیاب' in nd:
        pass # NEW
    # Maier dehydrator 5959
    elif 'مایر' in nd and '5959' in nd:
        pass # NEW
    # Ziko
    elif 'زیکو' in nd and any(k in nd for k in ['6501', '6502', '4038', '70028', '5020']):
        pass # NEW
    # Bosch chopper
    elif 'بوش' in nd and 'خردکن' in nd:
        pass # NEW
    # Mebashi
    elif 'مباشی' in nd:
        pass # NEW
    # Westinghouse 1663 espresso
    elif 'وستینگهوس' in nd and '1663' in nd:
        pass # NEW
    # Westinghouse Red kettle
    elif ('وستینگهوس' in nd or 'وستینگ هوس' in nd) and 'کتری' in nd and 'قرمز' in nd:
        pass # NEW
    # Westinghouse Red meat grinder / hand blender
    elif ('وستینگهوس' in nd or 'وستینگ هوس' in nd) and 'گوشت کوب' in nd and 'قرمز' in nd:
        pass # NEW
    # Welles 6033
    elif 'ویلز' in nd and '6033' in nd:
        pass # NEW
    # BUVCK steamer
    elif 'buvck' in nd or 'بخارگر' in nd:
        pass # NEW
    # Alton 900 hood
    elif ('التون' in nd or 'آلتون' in nd) and '900' in nd:
        pass # NEW
    # Oویز pot size 28
    elif 'اویز' in nd and '28' in nd:
        pass # NEW
    # Depoint Explore
    elif 'دیپونت' in nd and 'اکسپلور' in nd:
        pass # NEW
    # Depoint Decent
    elif ('دیپونت' in nd or 'dipoent' in nd) and 'دیسنت' in nd:
        pass # NEW
    # Electrosteel series 10
    elif 'الکترواستیل' in nd and '10' in nd:
        pass # NEW
    # Electrosteel 14 foot
    elif '14' in nd and ('الکتروسفید' in nd or 'الکترواستیل' in nd):
        pass # NEW
    # Electrosteel compact
    elif 'کمپکت' in nd and ('الکتروسفید' in nd or 'الکترواستیل' in nd):
        pass # NEW
    # 27 foot titanium
    elif '27' in nd and 'تیتانیوم' in nd and 'کلور' not in nd and 'هیمالیا' not in nd:
        pass # NEW
    # 35 foot home bar
    elif '35' in nd and ('درب بار' in nd or 'هوم بار' in nd):
        pass # NEW
    # Tefal 2.2L kettle
    elif 'تفال' in nd and '2.2' in nd:
        pass # NEW
    # Clover Mini Pastel Green / Red
    elif 'کلور' in nd and 'مینی' in nd and ('سبزپاستیلی' in nd or 'سبز پاستیلی' in nd or 're01' in nd or 'قرمز' in nd):
        pass # NEW
    else:
        # Search in catalog_items
        candidates = []
        for c in catalog_items:
            cn = c['norm_name']
            # direct check
            if 'aversen' in nd or 'هاورسن' in nd:
                for sz in ['85', '75', '65', '55', '32']:
                    if sz in nd and sz in cn and 'صوتی و تصویری' == c['sheet']:
                        candidates.append((100, c))
            elif 'افترون' in nd and 'افترون' in cn:
                candidates.append((90, c))
            elif 'نیکائی' in nd or 'نیکایی' in nd:
                if 'نیکایی' in cn or 'نیکائی' in cn:
                    candidates.append((90, c))
            elif 'وست واتر' in nd and 'وست واتر' in cn:
                candidates.append((90, c))
            elif 'بوتان' in nd and 'بوتان' in cn:
                candidates.append((90, c))
            elif 'پارس خزر' in nd and 'پارس خزر' in cn:
                if ('بلند' in nd and 'بلند' in cn) or ('کوتاه' in nd and 'کوتاه' in cn):
                    candidates.append((90, c))
            elif 'پاناسونیک' in nd and 'پاناسونیک' in cn:
                if 'پنکه' in nd and 'پنکه' in cn:
                    candidates.append((90, c))
                elif '715' in nd and '715' in cn:
                    candidates.append((90, c))
                elif 'hv11' in nd and 'hv11' in cn:
                    candidates.append((90, c))
            elif 'دونالکس' in nd and 'دونالکس' in cn:
                for code in ['120', '110', '815', '125', '200', '250', '205', '300', '950', '980', '500', '710', '960', '800']:
                    if code in nd and code in cn:
                        candidates.append((90, c))
            elif 'ساپر' in nd and 'ساپر' in cn:
                for code in ['4025', '4035', '1710', '4040']:
                    if code in nd and code in cn:
                        candidates.append((90, c))
            elif 'کلور' in nd and 'کلور' in cn:
                # check fridge or washer
                if 'اکونومی' in nd and 'اکونومی' in cn:
                    if ('استیل' in nd and 'استیل' in cn) or ('سفید' in nd and 'سفید' in cn):
                        candidates.append((80, c))
                elif 'روسو' in nd and 'روسو' in cn:
                    if '60' in nd and '60' in cn:
                        if ('استیل' in nd and 'استیل' in cn) or ('سفید' in nd and 'سفید' in cn) or ('مشکی' in nd and 'مشکی' in cn):
                            candidates.append((80, c))
                    elif '70' in nd and '70' in cn:
                        if ('استیل' in nd and 'استیل' in cn) or ('سفید' in nd and 'سفید' in cn):
                            candidates.append((80, c))
                elif 'گلوری' in nd and 'گلوری' in cn:
                    if ('استیل' in nd and 'استیل' in cn) or ('سفید' in nd and 'سفید' in cn):
                        candidates.append((80, c))
                elif 'مینی' in nd and 'مینی' in cn:
                    if ('آبی' in nd and 'آبی' in cn) or ('سبز' in nd and 'سبز' in cn) or ('سفید' in nd and 'سفید' in cn) or ('مشکی' in nd and 'مشکی' in cn):
                        candidates.append((80, c))
                elif '101' in nd and '101' in cn:
                    if ('استیل' in nd and 'استیل' in cn) or ('سفید' in nd and 'سفید' in cn):
                        candidates.append((80, c))
            elif 'ایستکول' in nd and 'ایستکول' in cn:
                if '9' in nd and '9' in cn:
                    if ('سفید' in nd and 'سفید' in cn) or ('نوک مدادی' in nd and 'نوک مدادی' in cn):
                        candidates.append((80, c))
            elif 'نیکسان' in nd and 'نیکسان' in cn:
                if ('استیل' in nd and 'استیل' in cn) or ('چرم' in nd and 'چرمی' in cn):
                    candidates.append((80, c))
            elif 'دیپوینت' in nd and 'دیپوینت' in cn:
                if 't7' in nd and 't7' in cn:
                    if ('استیل' in nd and 'استیل' in cn) or ('سفید' in nd and 'سفید' in cn):
                        candidates.append((80, c))
                elif 'max' in nd and 'max' in cn:
                    candidates.append((80, c))
                elif '34' in nd and 'سفید' in nd and 'max' in cn:
                    candidates.append((80, c))
            elif 'اویز' in nd and 'اویز' in cn:
                for sz in ['16', '18', '20', '22', '24', '26', '32']:
                    if sz in nd and sz in cn:
                        candidates.append((80, c))
            elif 'وستینگهاوس' in c['brand'] or 'وستینگهوس' in cn:
                if 'همزن' in nd and 'همزن' in cn:
                    if ('آبی' in nd and 'آبی' in cn) or ('کرم' in nd and 'کرم' in cn):
                        candidates.append((80, c))
                elif 'توستر' in nd and 'توستر' in cn:
                    candidates.append((80, c))
                elif 'کتری' in nd and 'کتری' in cn:
                    if ('آبی' in nd and 'آبی' in cn) or ('کرم' in nd and 'کرم' in cn):
                        candidates.append((80, c))
                elif 'کولر' in nd and 'کولر' in cn:
                    candidates.append((80, c))
            elif 'پرومارون' in nd and 'پرومارون' in cn:
                for code in ['614', '9909', '512', '1116', '109', '1113', '1114', '9901']:
                    if code in nd and code in cn:
                        candidates.append((80, c))
            elif 'پرو امگا' in nd or 'امگا' in nd:
                for code in ['999', '888', '777', '900', 't7', '1899', '1898', '1989']:
                    if code in nd and code in cn:
                        candidates.append((80, c))
        if candidates:
            candidates.sort(key=lambda x: x[0], reverse=True)
            best_match = candidates[0][1]
            matched_indices[idx] = (it, best_match)
        else:
            unmatched_items.append((idx, it))

print(f"Matched count: {len(matched_indices)}")
print(f"Accounting count: {len(accounting_items)}")
print(f"Unmatched (New actions): {len(unmatched_items)}")

for idx, it in unmatched_items:
    print(f"#{idx} (qty {it['qty']}): {it['desc']}")

