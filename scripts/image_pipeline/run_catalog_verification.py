import os
import sys
import json
import shutil
from multi_layer_evaluator import evaluate_candidate

sys.stdout.reconfigure(encoding='utf-8')

BASE_OUTPUT_DIR = 'product_images_2026-10-05'

def run_verification():
    harvested_file = 'scratch/all_candidates_harvested.json'
    if not os.path.exists(harvested_file):
        print(f"File {harvested_file} does not exist yet. Please wait for harvester to finish.")
        return
        
    with open(harvested_file, encoding='utf-8') as f:
        harvested_items = json.load(f)
        
    print(f"Loaded {len(harvested_items)} items for multi-layer evaluation...")
    
    approved_list = []
    rejected_list = []
    
    for item in harvested_items:
        row = item.get('row')
        name = item.get('name')
        brand = item.get('brand')
        parent_name = item.get('parent_name')
        sheet_folder = item.get('sheet_folder', 'misc')
        slug = item.get('slug', f"item_{row}")
        candidates = item.get('candidates', [])
        
        best_cand = None
        best_eval = None
        
        for cand in candidates:
            cand_eval = evaluate_candidate(cand, item)
            cand['evaluation'] = cand_eval
            
            if cand_eval.get('final_verdict') == 'APPROVED':
                if best_eval is None or cand_eval['model_score'] > best_eval['model_score']:
                    best_cand = cand
                    best_eval = cand_eval
                    
        if best_cand and best_eval:
            # Copy approved image to dated output directory
            dest_filename = f"{slug}.jpg"
            dest_path = os.path.join(BASE_OUTPUT_DIR, sheet_folder, dest_filename)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(best_cand['file_path'], dest_path)
            
            approved_list.append({
                'row': row,
                'name': name,
                'parent_name': parent_name,
                'brand': brand,
                'sheet_folder': sheet_folder,
                'slug': slug,
                'dest_path': dest_path,
                'relative_dest': os.path.relpath(dest_path),
                'matched_title': best_cand['matched_title'],
                'dimensions': best_eval['dimensions'],
                'model_score': best_eval['model_score'],
                'reasons': best_eval['reasons']
            })
            print(f" [APPROVED] [{brand}] {name} -> {dest_filename} ({best_eval['dimensions']})")
        else:
            rejected_list.append({
                'row': row,
                'name': name,
                'brand': brand,
                'sheet_folder': sheet_folder,
                'slug': slug,
                'candidates_count': len(candidates),
                'candidate_evaluations': [c.get('evaluation') for c in candidates]
            })
            print(f" [REJECTED/NO_MATCH] [{brand}] {name} ({len(candidates)} candidates checked)")
            
    # Save reports
    report_data = {
        'date': '2026-10-05',
        'total_items_processed': len(harvested_items),
        'total_approved': len(approved_list),
        'total_rejected_or_unmatched': len(rejected_list),
        'approved_items': approved_list,
        'rejected_items': rejected_list
    }
    
    report_json_path = os.path.join(BASE_OUTPUT_DIR, 'verification_report.json')
    with open(report_json_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
        
    print(f"\n==========================================")
    print(f"Multi-layer Verification Complete!")
    print(f"Approved: {len(approved_list)} / {len(harvested_items)}")
    print(f"Report saved to: {report_json_path}")
    print(f"==========================================")

if __name__ == '__main__':
    run_verification()
