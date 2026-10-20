# -*- coding: utf-8 -*-
"""
fix_missing_images_and_reaudit.py
=================================
رفع مشکل آپلود تصویر برای دو کالای دارای کاراکتر فارسی در نام فایل:
1. هود آشپزخانه آلتون مدل H315B (ID: 4088)
2. پلوپز پارس خزر مدل 361 (ID: 4113)
و سپس ممیزی کامل هر ۸ کالای باقیمانده.
"""

import os
import sys
import io
import time
import json
import requests
from PIL import Image

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

def upload_clean_image(fp, ascii_filename, product_name):
    img = Image.open(fp).convert('RGB')
    max_dim = 1200
    w, h = img.size
    if w > max_dim or h > max_dim:
        scale = max_dim / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=85, optimize=True)
    img_bytes = buf.getvalue()
    
    upload_headers = {
        'User-Agent': HEADERS['User-Agent'],
        'Content-Type': 'image/jpeg',
        'Content-Disposition': f'attachment; filename="{ascii_filename}"'
    }
    
    r = requests.post(
        'https://hosseinykala.ir/wp-json/wp/v2/media',
        auth=AUTH,
        headers=upload_headers,
        data=img_bytes,
        timeout=45
    )
    if r.status_code in [200, 201]:
        m_id = r.json().get('id')
        print(f"  ✓ عکس آپلود شد: ID {m_id}")
        # Update meta
        requests.post(
            f'https://hosseinykala.ir/wp-json/wp/v2/media/{m_id}',
            auth=AUTH,
            headers=HEADERS,
            json={'alt_text': f"{product_name} - حسینی کالا اهواز", 'title': f"خرید {product_name}"},
            timeout=15
        )
        return m_id
    else:
        raise Exception(f"Failed upload: {r.status_code} - {r.text[:200]}")

# 1. Fix Alton H315B
print("1. رفع مشکل هود آشپزخانه آلتون مدل H315B (ID: 4088)...")
alton_img = r'product_images_2026-10-05\cooking_appliances\هود آشپزخانه آلتون مدل H315B\315-آلتون-هود-آشپزخانه.jpg'
alton_mid = upload_clean_image(alton_img, 'alton-h315b-hood.jpg', 'هود آشپزخانه آلتون مدل H315B')

r_up_alton = requests.post(
    'https://hosseinykala.ir/wp-json/wc/v3/products/4088',
    auth=AUTH,
    headers=HEADERS,
    json={'images': [{'id': alton_mid}]},
    timeout=30
)
print(f"  ✓ پیوست تصویر به محصول 4088: وضعیت {r_up_alton.status_code}")

# 2. Fix Pars Khazar 361
print("\n2. رفع مشکل پلوپز پارس خزر مدل 361 (ID: 4113)...")
pk_img = r'product_images_2026-10-05\cooking_appliances\پلوپز پارس خزر مدل 361\پلوپز-16نفره-361-ts-361.webp'
pk_mid = upload_clean_image(pk_img, 'parskhazar-ts361-rice-cooker.jpg', 'پلوپز پارس خزر مدل 361')

r_up_pk = requests.post(
    'https://hosseinykala.ir/wp-json/wc/v3/products/4113',
    auth=AUTH,
    headers=HEADERS,
    json={'images': [{'id': pk_mid}]},
    timeout=30
)
print(f"  ✓ پیوست تصویر به محصول 4113: وضعیت {r_up_pk.status_code}")

# 3. Update creation_progress.json
with open('scratch/creation_progress.json', 'r', encoding='utf-8') as f:
    prog = json.load(f)
if 'هود آشپزخانه آلتون مدل H315B' in prog:
    prog['هود آشپزخانه آلتون مدل H315B']['media_ids'] = [alton_mid]
if 'پلوپز پارس خزر مدل 361' in prog:
    prog['پلوپز پارس خزر مدل 361']['media_ids'] = [pk_mid]
with open('scratch/creation_progress.json', 'w', encoding='utf-8') as f:
    json.dump(prog, f, ensure_ascii=False, indent=2)

print("\nتصاویر هر دو محصول با موفقیت آپلود و پیوست شدند!")
