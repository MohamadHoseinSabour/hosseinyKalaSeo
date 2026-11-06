import re
import json

with open('scratch/af_block_0.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Look for data object
m = re.search(r'data:\s*(\[[\s\S]*\])\s*,\s*sideChannel:', text)
if not m:
    m = re.search(r'data:\s*(\[[\s\S]*\])\s*\}', text)

print("Found data array:", bool(m))

# Let's search directly in text for score values or category names
categories = ['performance', 'accessibility', 'best-practices', 'seo']
for c in categories:
    m_score = re.findall(rf'"{c}"[\s\S]{{1,200}}?"score":\s*([0-9.]+)', text)
    print(f"Category '{c}' matches: {m_score}")

# Find failing accessibility items
# In lighthouse, audits have "id": "...", "score": 0, "title": "..."
m_a11y = re.findall(r'"([a-z0-9-]+)":\{"id":"\1"[^}]*?"title":"([^"]+)"[^}]*?"score":([0-9.]+)', text)
print(f"\nAll audits matched: {len(m_a11y)}")
failing = [x for x in m_a11y if float(x[2]) < 1]
print(f"Failing audits ({len(failing)}):")
for f_id, f_title, f_score in failing:
    print(f"  [{f_id}] {f_title} -> {f_score}")

# If regex didn't match the format, let's search for specific audit keys
known_audits = [
    'button-name', 'color-contrast', 'document-title', 'html-has-lang', 'image-alt',
    'link-name', 'meta-viewport', 'aria-allowed-attr', 'aria-required-attr', 'aria-valid-attr',
    'aria-hidden-body', 'heading-order', 'label', 'target-size', 'tap-targets'
]
print("\nChecking known audits:")
for a in known_audits:
    matches = re.findall(rf'"{a}"[\s\S]{{1,300}}?"score":\s*([0-9.]+)', text)
    if matches:
        print(f"  {a}: scores={matches}")
