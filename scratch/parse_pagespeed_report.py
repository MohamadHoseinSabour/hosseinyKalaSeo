import urllib.request
import re
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request('https://pagespeed.web.dev/analysis/https-hosseinykala-ir/p31vkp5f3e?form_factor=mobile', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode('utf-8')

m = re.search(r'data:(\[.*\])\s*\}\);', html, re.DOTALL)
if not m:
    print("Regex data match failed")
    sys.exit(1)

raw_data = m.group(1)

try:
    data = json.loads(raw_data)
    print("Parsed JSON data successfully!")
    def search_lighthouse(obj):
        if isinstance(obj, str):
            if '"lighthouseVersion"' in obj or '"categories"' in obj:
                try:
                    parsed = json.loads(obj)
                    return parsed
                except:
                    pass
        elif isinstance(obj, list):
            for item in obj:
                res = search_lighthouse(item)
                if res: return res
        elif isinstance(obj, dict):
            for k, v in obj.items():
                res = search_lighthouse(v)
                if res: return res
        return None

    lr = search_lighthouse(data)
    if lr:
        print("\n=== LIGHTHOUSE REPORT EXTRACTED FROM p31vkp5f3e ===")
        cats = lr.get('categories', {})
        for cat_id, cat in cats.items():
            print(f"  {cat_id.upper()}: {int(cat.get('score', 0) * 100)}")
        
        audits = lr.get('audits', {})
        print("\n--- Failed Audits in Accessibility ---")
        a11y_refs = cats.get('accessibility', {}).get('auditRefs', [])
        for r in a11y_refs:
            a_id = r.get('id')
            a = audits.get(a_id, {})
            score = a.get('score')
            if score is not None and score < 1:
                print(f"  [{a_id}] {a.get('title')} (score: {score})")
                details = a.get('details', {})
                for it in details.get('items', [])[:5]:
                    node = it.get('node', {})
                    snippet = node.get('snippet') or it.get('description')
                    explanation = node.get('explanation')
                    print(f"    - Snippet: {snippet}")
                    if explanation:
                        print(f"      Explanation: {explanation}")
        
        print("\n--- Performance Metrics ---")
        for m_name in ['first-contentful-paint', 'largest-contentful-paint', 'total-blocking-time', 'cumulative-layout-shift', 'speed-index', 'server-response-time']:
            audit = audits.get(m_name, {})
            print(f"  {m_name}: {audit.get('displayValue')} (score: {audit.get('score')})")

        with open('scratch/p31vkp5f3e_audits.json', 'w', encoding='utf-8') as out:
            json.dump({'categories': cats, 'audits': audits}, out, indent=2)

    else:
        print("LighthouseResult string not found in data array")

except Exception as e:
    print("Error parsing:", e)
