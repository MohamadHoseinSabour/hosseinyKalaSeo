import re
import json

with open('scratch/af_block_0.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Find the JSON string starting with "{\"fetchTime\"
start = text.find('\"{\\\"fetchTime\\\"')
if start == -1:
    start = text.find('{"fetchTime"')

print("Start index:", start)
# Extract the JSON string
# Let's find end of string or parse with json
# In JavaScript, it's a quoted string inside an array
# Let's extract between the quotes
idx1 = text.find('\"{\\', start)
# We can find the closing quote
# Or let's use regex
m = re.search(r'\"(\{\\?\"fetchTime\\?\"[\s\S]*?\})\"', text)
if m:
    raw = m.group(1).encode().decode('unicode_escape')
    try:
        lh = json.loads(raw)
        print("Successfully parsed Lighthouse JSON!")
        cats = lh.get('categories', {})
        for c_id, c_data in cats.items():
            print(f"Category: {c_id:15} | Score: {int(c_data.get('score', 0) * 100)}")
            
        print("\n=== FAILING ACCESSIBILITY AUDITS ===")
        for ref in cats.get('accessibility', {}).get('auditRefs', []):
            a_id = ref.get('id')
            audit = lh.get('audits', {}).get(a_id, {})
            score = audit.get('score')
            if score is not None and score < 1:
                print(f"\n[FAIL] {a_id}: {audit.get('title')} (score={score}, weight={ref.get('weight')})")
                details = audit.get('details', {})
                items = details.get('items', [])
                for it in items[:5]:
                    node = it.get('node', {})
                    print(f"  - Snippet: {node.get('snippet', '')}")
                    print(f"    Selector: {node.get('selector', '')}")
                    print(f"    Explanation: {node.get('explanation', '')}")

        print("\n=== FAILING BEST PRACTICES AUDITS ===")
        for ref in cats.get('best-practices', {}).get('auditRefs', []):
            a_id = ref.get('id')
            audit = lh.get('audits', {}).get(a_id, {})
            score = audit.get('score')
            if score is not None and score < 1:
                print(f"[FAIL] {a_id}: {audit.get('title')} (score={score})")

        print("\n=== PERFORMANCE METRICS ===")
        print("Performance score:", int(cats.get('performance', {}).get('score', 0) * 100))
        for metric in ['first-contentful-paint', 'largest-contentful-paint', 'total-blocking-time', 'cumulative-layout-shift', 'speed-index']:
            aud = lh.get('audits', {}).get(metric, {})
            print(f"  {metric}: {aud.get('displayValue')} (score={aud.get('score')})")

        print("\n=== PERFORMANCE DIAGNOSTICS ===")
        for p_id in ['render-blocking-resources', 'uses-optimized-images', 'uses-long-cache-ttl', 'uses-responsive-images', 'offscreen-images', 'unminified-css', 'unminified-javascript', 'unused-css-rules', 'unused-javascript']:
            aud = lh.get('audits', {}).get(p_id, {})
            if aud:
                print(f"  {p_id}: score={aud.get('score')}, displayValue={aud.get('displayValue')}")
                if aud.get('details') and aud['details'].get('overallSavingsMs'):
                    print(f"    overallSavingsMs: {aud['details']['overallSavingsMs']}")
                if aud.get('details') and aud['details'].get('overallSavingsBytes'):
                    print(f"    overallSavingsBytes: {aud['details']['overallSavingsBytes']}")

    except Exception as e:
        print("Error parsing json:", e)
else:
    print("Regex match failed")
