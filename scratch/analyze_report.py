import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('product_images_2026-10-05/verification_report.json', encoding='utf-8') as f:
    rep = json.load(f)

approved = rep.get('approved_items', [])
rejected = rep.get('rejected_items', [])

print(f"Total Approved: {len(approved)}")
for a in approved:
    print(f" - [{a.get('brand')}] {a.get('name')} -> {a.get('slug')} ({a.get('dimensions')})")

print(f"\nTotal Rejected/Unmatched: {len(rejected)}")
no_cand = [r for r in rejected if r.get('candidates_count', 0) == 0]
has_cand = [r for r in rejected if r.get('candidates_count', 0) > 0]
print(f"Rejected with 0 candidates: {len(no_cand)}")
print(f"Rejected with >= 1 candidates: {len(has_cand)}")

print("\nSample of rejected with candidates:")
for r in has_cand[:15]:
    c_evals = r.get('candidate_evaluations', [])
    first_ev = c_evals[0] if c_evals else {}
    print(f" - [{r.get('brand')}] {r.get('name')}: {r.get('candidates_count')} cands, verdict={first_ev.get('final_verdict')}, reasons={first_ev.get('reasons', [])[:2]}")

print("\nSample of rejected with 0 candidates:")
for r in no_cand[:15]:
    print(f" - [{r.get('brand')}] {r.get('name')}")
