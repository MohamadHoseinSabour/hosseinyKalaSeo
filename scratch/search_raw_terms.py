import json

raw_lines = open('data/inventory_incoming_raw.csv', encoding='utf-8', errors='ignore').readlines()
print("From inventory_incoming_raw.csv:")
for i, line in enumerate(raw_lines):
    for term in ['604', 'KENRA', 'دستی', 'قابلمه', 'استیل', 'کنرا', 'طلا', 'سبزی خردکن']:
        if term in line:
            print(f"Line {i+1}: {line.strip()}")
            break
