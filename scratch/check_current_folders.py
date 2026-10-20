import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base = 'new_product_images'
for cat in sorted(os.listdir(base)):
    cat_path = os.path.join(base, cat)
    if os.path.isdir(cat_path):
        print(f"\n📁 [{cat}]")
        for prod in sorted(os.listdir(cat_path)):
            prod_path = os.path.join(cat_path, prod)
            files = [f for f in os.listdir(prod_path) if os.path.isfile(os.path.join(prod_path, f))]
            status = f"✓ {len(files)} file(s): {', '.join(files)}" if files else "⚠️ [EMPTY / NEED IMAGE]"
            print(f"  • {prod} -> {status}")
