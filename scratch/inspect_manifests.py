import sys
import os
import json
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

with open('extracted_products/manifest.json', 'r', encoding='utf-8') as f:
    ext_man = json.load(f)

with open('new_products/manifest.json', 'r', encoding='utf-8') as f:
    new_man = json.load(f)

print(f"extracted_products manifest type: {type(ext_man)}")
if isinstance(ext_man, dict):
    print("extracted_products keys (sample 5):", list(ext_man.keys())[:5])
    k0 = list(ext_man.keys())[0]
    print(f"Sample value for {k0}:", ext_man[k0])
elif isinstance(ext_man, list):
    print("Sample ext_man[0]:", ext_man[0])

print(f"\nnew_products manifest type: {type(new_man)}")
if isinstance(new_man, dict):
    print("new_products keys (sample 5):", list(new_man.keys())[:5])
    k0 = list(new_man.keys())[0]
    print(f"Sample value for {k0}:", new_man[k0])
elif isinstance(new_man, list):
    print("Sample new_man[0]:", new_man[0])
