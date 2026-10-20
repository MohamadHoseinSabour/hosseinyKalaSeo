import os
import sys
import json
import requests
from PIL import Image
import io

sys.stdout.reconfigure(encoding='utf-8')

import os
sys.path.insert(0, os.path.abspath('.'))
from scratch.image_search_targets import BASE_DIR, TARGETS

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

os.makedirs(BASE_DIR, exist_ok=True)

results_summary = []

for idx, t in enumerate(TARGETS, 1):
    cat = t['category']
    folder_name = t['folder_name']
    dest_dir = os.path.join(BASE_DIR, cat, folder_name)
    os.makedirs(dest_dir, exist_ok=True)
    
    print(f"\n[{idx}/{len(TARGETS)}] {cat} -> {folder_name}")
    
    found_images = []
    matched_title = ""
    source = ""
    
    # Try Digikala
    for q in t['queries']:
        try:
            r = requests.get('https://api.digikala.com/v1/search/', params={'q': q}, headers=headers, timeout=6)
            if r.status_code == 200:
                data = r.json().get('data', {}).get('products', [])
                for p in data[:5]:
                    title = p.get('title_fa', '')
                    title_lower = title.lower()
                    
                    # Check if all signatures match
                    sigs_match = all(s.lower() in title_lower for s in t['sigs'])
                    if sigs_match:
                        # Extract images
                        main_img = p.get('images', {}).get('main', {}).get('url', [])
                        list_imgs = p.get('images', {}).get('list', [])
                        
                        all_cand_imgs = []
                        if main_img:
                            all_cand_imgs.append(main_img[0].split('?')[0])
                        for li in list_imgs:
                            for u in li.get('url', []):
                                clean_u = u.split('?')[0]
                                if clean_u not in all_cand_imgs:
                                    all_cand_imgs.append(clean_u)
                                    
                        if all_cand_imgs:
                            matched_title = title
                            source = f"Digikala (ID: {p.get('id')})"
                            found_images = all_cand_imgs[:3] # top 3 images
                            break
            if found_images:
                break
        except Exception as e:
            pass
            
    # Download found images if any
    downloaded_files = []
    if found_images:
        print(f"  ✓ Matched in {source}: '{matched_title}'")
        for img_idx, img_url in enumerate(found_images, 1):
            fname = "main.jpg" if img_idx == 1 else f"{img_idx}.jpg"
            fpath = os.path.join(dest_dir, fname)
            try:
                r_img = requests.get(img_url, headers=headers, timeout=8)
                if r_img.status_code == 200 and len(r_img.content) > 5000:
                    with open(fpath, 'wb') as f:
                        f.write(r_img.content)
                    im = Image.open(fpath)
                    print(f"    - Saved {fname}: {im.size} ({len(r_img.content)//1024} KB)")
                    downloaded_files.append({
                        'filename': fname,
                        'path': fpath,
                        'dimensions': im.size,
                        'size_kb': len(r_img.content)//1024,
                        'url': img_url
                    })
            except Exception as e:
                print(f"    ⚠️ Error downloading {img_url}: {e}")
                
    if downloaded_files:
        results_summary.append({
            'category': cat,
            'name': folder_name,
            'status': 'DOWNLOADED',
            'matched_title': matched_title,
            'source': source,
            'files': downloaded_files
        })
    else:
        print("  ✗ Not found on Digikala. Marked for external search.")
        results_summary.append({
            'category': cat,
            'name': folder_name,
            'status': 'PENDING_SEARCH',
            'queries': t['queries'],
            'sigs': t['sigs'],
            'dest_dir': dest_dir
        })

with open('scratch/phase1_image_results.json', 'w', encoding='utf-8') as f:
    json.dump(results_summary, f, ensure_ascii=False, indent=2)

downloaded_cnt = sum(1 for r in results_summary if r['status'] == 'DOWNLOADED')
pending_cnt = sum(1 for r in results_summary if r['status'] == 'PENDING_SEARCH')
print(f"\n==========================================")
print(f"Phase 1 Complete!")
print(f"Downloaded: {downloaded_cnt} / {len(TARGETS)}")
print(f"Pending Phase 2: {pending_cnt} / {len(TARGETS)}")
print(f"==========================================")
