import re
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/af_chunk.js', 'r', encoding='utf-8') as f:
    text = f.read()

# text looks like: AF_initDataCallback({key: 'ds:0', hash: '1', data:[...], sideChannel: {}});
# Find start of data:[
data_idx = text.find('data:[')
if data_idx == -1:
    data_idx = text.find('data: [')

start_bracket = text.find('[', data_idx)

# Find matching closing bracket
count = 0
in_string = False
escape = False
quote_char = ''
end_bracket = -1

for i in range(start_bracket, len(text)):
    c = text[i]
    if escape:
        escape = False
        continue
    if c == '\\':
        escape = True
        continue
    if in_string:
        if c == quote_char:
            in_string = False
        continue
    else:
        if c in ('"', "'"):
            in_string = True
            quote_char = c
        elif c == '[':
            count += 1
        elif c == ']':
            count -= 1
            if count == 0:
                end_bracket = i
                break

if end_bracket == -1:
    print("Could not find matching end bracket")
    sys.exit(1)

print(f"Bracket matched: from {start_bracket} to {end_bracket}")
json_raw = text[start_bracket:end_bracket+1]

try:
    data = json.loads(json_raw)
    print("Parsed JSON data successfully!")
    
    def search_lighthouse(obj):
        if isinstance(obj, str):
            if '"lighthouseVersion"' in obj or '"categories"' in obj:
                try:
                    return json.loads(obj)
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

        print("\n--- Performance Opportunities & Diagnostics ---")
        for a_id, a in audits.items():
            if a.get('details', {}).get('type') == 'opportunity' and a.get('score', 1) < 0.9:
                print(f"  [OPPORTUNITY] {a.get('title')}: {a.get('displayValue')}")
    else:
        print("LighthouseResult string not found in data structure")

except Exception as e:
    print("Error parsing json:", e)
