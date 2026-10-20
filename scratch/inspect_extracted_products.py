import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ext_dir = 'extracted_products'
print(f"Top-level dirs in {ext_dir}:")
for item in sorted(os.listdir(ext_dir)):
    p = os.path.join(ext_dir, item)
    if os.path.isdir(p):
        sub = os.listdir(p)
        print(f"  [Cat] {item} ({len(sub)} items)")
        for s in sub[:5]:
            sp = os.path.join(p, s)
            if os.path.isdir(sp):
                files = [f for f in os.listdir(sp) if not f.endswith('.txt')]
                print(f"    - {s} -> {len(files)} image files")
            else:
                print(f"    - [File] {s}")
