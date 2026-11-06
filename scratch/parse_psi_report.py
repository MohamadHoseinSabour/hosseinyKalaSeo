import requests
import json
import re

url = 'https://pagespeed.web.dev/analysis/https-hosseinykala-ir/p31vkp5f3e?form_factor=mobile'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)

with open('scratch/psi_report.html', 'w', encoding='utf-8') as f:
    f.write(r.text)

print("Saved report HTML. Searching for lighthouse json data...")

# Look for embedded JSON
matches = re.findall(r'<script[^>]*>([^<]*lighthouseResult[^<]*)</script>', r.text)
if not matches:
    matches = re.findall(r'(\{"lighthouseResult":[\s\S]*?\})\s*</script>', r.text)

print(f"Matches found: {len(matches)}")
if matches:
    data_str = matches[0]
    # Extract JSON
    try:
        data = json.loads(data_str)
        lh = data.get('lighthouseResult', {})
        cats = lh.get('categories', {})
        for cat_id, cat_info in cats.items():
            print(f"Category: {cat_id:15} | Score: {int(cat_info.get('score', 0) * 100)}")
            
        print("\n=== FAILING ACCESSIBILITY AUDITS ===")
        a11y_audits = cats.get('accessibility', {}).get('auditRefs', [])
        for ref in a11y_audits:
            audit = lh.get('audits', {}).get(ref.get('id'), {})
            score = audit.get('score')
            if score is not None and score < 1:
                print(f"  [FAIL] {ref.get('id')}: {audit.get('title')} (score: {score})")
                print(f"    Description: {audit.get('description', '')[:120]}")
                details = audit.get('details', {})
                items = details.get('items', [])
                print(f"    Failing elements count: {len(items)}")
                for it in items[:3]:
                    node = it.get('node', {})
                    print(f"      Node: {node.get('snippet', '')[:100]}")
                    
        print("\n=== PERFORMANCE AUDITS ===")
        perf = cats.get('performance', {})
        print("Performance score:", int(perf.get('score', 0) * 100))
        for metric in ['first-contentful-paint', 'largest-contentful-paint', 'total-blocking-time', 'cumulative-layout-shift', 'speed-index']:
            aud = lh.get('audits', {}).get(metric, {})
            print(f"  {metric}: {aud.get('displayValue')}")
    except Exception as e:
        print("JSON parse error:", e)
else:
    # Search for categories in text
    print("Searching regex for scores...")
    for cat in ['performance', 'accessibility', 'best-practices', 'seo']:
        m = re.findall(rf'"{cat}":\{{[^}}]*"score":([0-9.]+)', r.text)
        print(f"Score for {cat}:", m)
