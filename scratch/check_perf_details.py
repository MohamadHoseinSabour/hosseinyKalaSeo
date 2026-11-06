import re
import json

with open('scratch/af_block_0.js', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'\"(\{\\?\"fetchTime\\?\"[\s\S]*?\})\"', text)
raw = m.group(1).encode().decode('unicode_escape')
lh = json.loads(raw)

audits = lh.get('audits', {})
print("=== PERFORMANCE METRIC VALUES ===")
for m in ['first-contentful-paint', 'largest-contentful-paint', 'total-blocking-time', 'cumulative-layout-shift', 'speed-index']:
    a = audits.get(m, {})
    print(f"  {m:25}: displayValue={a.get('displayValue')}, score={a.get('score')}")

print("\n=== LCP DETAILS ===")
lcp_audit = audits.get('largest-contentful-paint-element', {})
items = lcp_audit.get('details', {}).get('items', [])
for it in items:
    print("  LCP Element snippet:", it.get('node', {}).get('snippet'))
    print("  LCP Element selector:", it.get('node', {}).get('selector'))

print("\n=== OPPORTUNITIES WITH SAVINGS ===")
for a_id, a in audits.items():
    details = a.get('details', {})
    if isinstance(details, dict) and details.get('overallSavingsMs', 0) > 0:
        print(f"  {a_id}: overallSavingsMs={details.get('overallSavingsMs')}, title={a.get('title')}")
    if isinstance(details, dict) and details.get('overallSavingsBytes', 0) > 20000:
        print(f"  {a_id}: overallSavingsBytes={details.get('overallSavingsBytes')/1024:.1f} KB, title={a.get('title')}")
