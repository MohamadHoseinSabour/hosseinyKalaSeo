import csv
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

input_path = 'data/hosseinykala_404_redirects_rankmath.csv'

with open(input_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    rows = list(reader)

cleaned_rows = []
header = rows[0]
cleaned_rows.append(header)

fixed_count = 0
for r in rows[1:]:
    if len(r) >= 3:
        src = r[0]
        # Clean corrupted prefix /"https:////hosseinykala.ir// or /""https:////...
        src = re.sub(r'^[/"\\]*https?:?/*(?:hosseinykala\.ir)?/*', '/', src)
        src = re.sub(r'/+$', '/', src)
        src = re.sub(r'"+', '', src)
        if not src.startswith('/'):
            src = '/' + src
        
        # Check if src changed
        if src != r[0]:
            fixed_count += 1
            
        r[0] = src
        cleaned_rows.append(r)

# Ensure the missing 404 URL is included:
glory_missing = ['/product/یخچال-فریزر-دوقلو-40-فوت-کلور-مدل-گلوری-پ/', 'exact', 'https://hosseinykala.ir/product/clover-glory-plus-lm70-twin-refrigerator/', '301', 'active']
existing_sources = [r[0] for r in cleaned_rows]
if glory_missing[0] not in existing_sources:
    cleaned_rows.append(glory_missing)
    print("Added missing glory plus redirect!")

with open(input_path, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(cleaned_rows)

print(f"Sanitization complete! Fixed {fixed_count} corrupted source URLs.")
print(f"Total redirects now in CSV: {len(cleaned_rows)-1}")
