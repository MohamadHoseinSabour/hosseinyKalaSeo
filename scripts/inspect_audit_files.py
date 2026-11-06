import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

for fname in ['final_classified_audit.json', 'inventory_audit_summary.json', 'parsed_incoming_rp_cu_5.json']:
    print(f"\n=================== {fname} ===================")
    with open(f'scratch/{fname}', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # search for TV items
    def search_obj(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                search_obj(v, path + f"/{k}")
        elif isinstance(obj, list):
            for i, it in enumerate(obj):
                search_obj(it, path + f"/[{i}]")
        elif isinstance(obj, str):
            if any(w in obj for w in ['TOSHIBA', 'توشیبا', 'X.VISJON', 'XVISION', 'ایکس', 'L2300EE', 'هایسنس']):
                print(f"Path: {path} => {obj}")

    search_obj(data)
