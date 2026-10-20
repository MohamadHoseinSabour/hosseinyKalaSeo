import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

img_base = 'new_product_images'

for cat in sorted(os.listdir(img_base)):
    cat_p = os.path.join(img_base, cat)
    if not os.path.isdir(cat_p):
        continue
    print(f"\n==========================================")
    print(f"CATEGORY: {cat}")
    print(f"==========================================")
    for prod in sorted(os.listdir(cat_p)):
        prod_p = os.path.join(cat_p, prod)
        if not os.path.isdir(prod_p):
            continue
        files = os.listdir(prod_p)
        print(f"\n* Product Folder: '{prod}'")
        for f in files:
            fp = os.path.join(prod_p, f)
            sz = os.path.getsize(fp)
            print(f"    - {f} ({sz:,} bytes)")
            if f.endswith('.txt'):
                try:
                    with open(fp, 'r', encoding='utf-8') as tf:
                        txt_content = tf.read().strip()
                        print(f"      [TXT CONTENT]: {txt_content}")
                except Exception as e:
                    print(f"      [TXT ERROR]: {e}")
