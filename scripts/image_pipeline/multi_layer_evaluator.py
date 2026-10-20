import os
import sys
import json
import re
from PIL import Image, ImageStat

sys.stdout.reconfigure(encoding='utf-8')

def evaluate_candidate(cand_data, item_data):
    """
    Evaluates a candidate image for:
    1. Exact Model Match Score (0 - 100)
    2. Watermark & Studio Quality (CLEAN, REJECTED, SUSPICIOUS)
    3. Final Verdict
    """
    file_path = cand_data.get('file_path')
    if not os.path.exists(file_path):
        return {'verdict': 'FILE_NOT_FOUND', 'score': 0, 'reasons': ['File does not exist']}
        
    cand_title = cand_data.get('matched_title', '')
    target_name = item_data.get('name', '')
    target_parent = item_data.get('parent_name', '')
    target_brand = item_data.get('brand', '')
    
    # 1. Technical Model Match Analysis
    full_target = f"{target_parent} {target_name}" if target_parent else target_name
    reasons = []
    model_score = 0
    
    # Check Brand
    brand_match = target_brand and target_brand in cand_title
    if brand_match:
        model_score += 30
    else:
        reasons.append(f"Brand mismatch: target '{target_brand}' not found in candidate title '{cand_title}'")
        
    # Check specific model numbers/codes
    # e.g. 60MW, SG518, B3115, DN-970, RF84102E2, 7303, H312, 1710, etc.
    target_codes = re.findall(r'[a-zA-Z0-9]+-?[a-zA-Z0-9]+', full_target)
    significant_codes = [c for c in target_codes if len(c) >= 3 and not (c.isdigit() and len(c) < 3)]
    
    code_matched = False
    for code in significant_codes:
        if code.lower() in cand_title.lower():
            code_matched = True
            model_score += 40
            reasons.append(f"Model code '{code}' matched in candidate title")
            break
            
    # Check key category/feature keywords
    key_features = [
        'دوقلو', 'کمبی', 'ساید', 'صندوقی', 'هوم بار', 'آبریز', 'روسو', 'اکونومی',
        'جاروبرقی', 'لباسشویی', 'مینی واش', 'پتوشور', 'سرخ کن', 'هواپز', 'غذاساز',
        'گاز صفحه ای', 'فر توکار', 'هود', 'خردکن', 'پلوپز', 'همزن', 'اسپرسو',
        'کتری برقی', 'چای ساز', 'آسیاب', 'پنکه', 'بخاری', 'آبگرمکن', 'سشوار', 'ریش تراش'
    ]
    
    matched_features = []
    for f in key_features:
        if f in full_target and f in cand_title:
            matched_features.append(f)
            
    if matched_features:
        model_score += min(30, len(matched_features) * 15)
        reasons.append(f"Features matched: {', '.join(matched_features)}")
        
    # Check negative mismatch (e.g. if target says 'دوقلو' but candidate is 'کمبی' or 'ساید')
    if 'دوقلو' in full_target and ('کمبی' in cand_title or 'ساید' in cand_title):
        model_score -= 40
        reasons.append("Structural mismatch: target is twin (دوقلو) but candidate is combi/side-by-side")
    if 'صندوقی' in full_target and 'ایستاده' in cand_title:
        model_score -= 40
        reasons.append("Structural mismatch: target is chest freezer but candidate is upright")
        
    # 2. Visual Quality & Watermark Check
    quality_verdict = 'CLEAN'
    try:
        img = Image.open(file_path).convert('RGB')
        w, h = img.size
        
        if w < 600 or h < 600:
            quality_verdict = 'LOW_RES'
            reasons.append(f"Low resolution: {w}x{h}")
            
        # Check border purity
        cw, ch = max(20, int(w * 0.08)), max(20, int(h * 0.08))
        corners = [
            (0, 0, cw, ch),
            (w - cw, 0, w, ch),
            (0, h - ch, cw, h),
            (w - cw, h - ch, w, h)
        ]
        
        has_corner_artifact = False
        for box in corners:
            crop = img.crop(box)
            stat = ImageStat.Stat(crop)
            mean_b = sum(stat.mean) / 3.0
            std_b = sum(stat.stddev) / 3.0
            if mean_b < 235 and std_b > 25:
                has_corner_artifact = True
                break
                
        if has_corner_artifact:
            quality_verdict = 'SUSPICIOUS_WATERMARK'
            reasons.append("Suspicious non-white pattern in corners (possible watermark)")
            
    except Exception as e:
        quality_verdict = 'CORRUPTED'
        reasons.append(f"Image open error: {e}")
        
    # Final combined verdict
    if model_score >= 60 and quality_verdict == 'CLEAN':
        final_verdict = 'APPROVED'
    elif model_score < 50:
        final_verdict = 'REJECTED_MODEL_MISMATCH'
    elif quality_verdict != 'CLEAN':
        final_verdict = f'REJECTED_{quality_verdict}'
    else:
        final_verdict = 'NEEDS_MANUAL_REVIEW'
        
    return {
        'model_score': model_score,
        'brand_match': brand_match,
        'code_matched': code_matched,
        'quality_verdict': quality_verdict,
        'final_verdict': final_verdict,
        'reasons': reasons,
        'dimensions': f"{w}x{h}" if 'w' in locals() else None
    }
