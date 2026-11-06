import re
import json
import sys

with open('scratch/af_block_0.js', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'\"(\{\\?\"fetchTime\\?\"[\s\S]*?\})\"', text)
raw = m.group(1).encode().decode('unicode_escape')
lh = json.loads(raw)

cats = lh.get('categories', {})
print("Scores:")
for c_id, c_data in cats.items():
    print(f"  {c_id}: {int(c_data.get('score', 0) * 100)}")

with open('scratch/accessibility_fails.txt', 'w', encoding='utf-8') as out:
    out.write("=== FAILING ACCESSIBILITY AUDITS ===\n")
    for ref in cats.get('accessibility', {}).get('auditRefs', []):
        a_id = ref.get('id')
        audit = lh.get('audits', {}).get(a_id, {})
        score = audit.get('score')
        if score is not None and score < 1:
            out.write(f"\n[FAIL] {a_id}: {audit.get('title')} (score={score}, weight={ref.get('weight')})\n")
            out.write(f"  Description: {audit.get('description')}\n")
            details = audit.get('details', {})
            items = details.get('items', [])
            out.write(f"  Total failing elements: {len(items)}\n")
            for it in items:
                node = it.get('node', {})
                out.write(f"    - Snippet: {node.get('snippet', '')}\n")
                out.write(f"      Selector: {node.get('selector', '')}\n")
                out.write(f"      Explanation: {node.get('explanation', '')}\n")

print("Saved accessibility fails to scratch/accessibility_fails.txt")
