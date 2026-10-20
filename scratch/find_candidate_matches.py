import json
import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_candidates_harvested.json', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total items in harvested data: {len(items)}")

matches_found = []
needs_deep_search = []

def clean_str(s):
    if not s:
        return ""
    # normalize persian chars
    s = s.replace('ي', 'ی').replace('ك', 'ک')
    return s.strip()

for it in items:
    row = it.get('row')
    sheet = it.get('sheet_folder')
    brand = clean_str(it.get('brand', ''))
    name = clean_str(it.get('name', ''))
    parent = clean_str(it.get('parent_name', ''))
    full_target = f"{parent} {name}" if parent else name
    slug = it.get('slug')
    cands = it.get('candidates', [])
    
    # Extract model codes or distinctive Persian keywords
    # e.g., 60MW, SG518, B3115, DN-970, RF8410, 7303, H312, H315B, 4035, 6031, 6032, 2013, FH-2000P, 3PN, RL-731
    codes = re.findall(r'[a-zA-Z0-9]+-?[a-zA-Z0-9]+', full_target)
    sig_codes = [c for c in codes if len(c) >= 3 and not (c.isdigit() and len(c) < 3)]
    
    # Also check distinct model words in Persian
    # e.g. روسو, آیس پول, اکونومی, تسلا, سینیور, گلوری, پلار, بوتان, پاکیزان, فریدولین, ساپر, سانی
    best_candidate = None
    best_score = 0
    best_reason = ""
    
    for c in cands:
        title = clean_str(c.get('matched_title', ''))
        file_path = c.get('file_path', '')
        if not os.path.exists(file_path):
            continue
            
        score = 0
        reasons = []
        
        # Check brand
        if brand and (brand.lower() in title.lower() or brand in title):
            score += 30
            reasons.append(f"Brand '{brand}' matched")
            
        # Check model codes
        for code in sig_codes:
            if code.lower() in title.lower():
                score += 50
                reasons.append(f"Code '{code}' matched")
                break
                
        # Check specific model names
        persian_models = ['آیس پول', 'روسو', 'اکونومی', 'تسلا', 'سینیور', 'گلوری', 'امگا', 'آلفا', 
                          'پاکیزان', 'فریدولین', 'ساپر', 'سانی', 'بوتان', 'پلار', 'گرنویک', 'کورکماز', 
                          'کاستلو', 'نیاک', 'لاوان', 'اویز', 'ویلز', 'پروامگا', 'پرومارون', 'آلتون', 'دونالکس']
        for pm in persian_models:
            if pm in full_target and pm in title:
                score += 30
                reasons.append(f"Model term '{pm}' matched")
                break
                
        # Negative checks
        if 'دوقلو' in full_target and ('کمبی' in title or 'ساید' in title):
            score -= 50
        if 'لباسشویی' in full_target and 'ظرفشویی' in title:
            score -= 50
        if 'بخاری' in full_target and 'کولر' in title:
            score -= 50
            
        if score > best_score:
            best_score = score
            best_candidate = c
            best_reason = " | ".join(reasons)
            
    if best_candidate and best_score >= 50:
        matches_found.append({
            'row': row,
            'sheet': sheet,
            'brand': brand,
            'target': full_target,
            'slug': slug,
            'best_cand': best_candidate,
            'score': best_score,
            'reason': best_reason
        })
    else:
        needs_deep_search.append({
            'row': row,
            'sheet': sheet,
            'brand': brand,
            'target': full_target,
            'slug': slug,
            'best_score': best_score,
            'candidates_count': len(cands)
        })

print(f"\nCandidates with strong model match: {len(matches_found)}")
print(f"Items needing deep search / query refinement: {len(needs_deep_search)}")

print("\n--- Strong Matches Found ---")
for m in matches_found:
    print(f"[{m['sheet']}] [{m['brand']}] {m['target']} (Score: {m['score']})")
    print(f"   -> Cand Title: {m['best_cand']['matched_title']}")
    print(f"   -> File: {m['best_cand']['file_path']}")
