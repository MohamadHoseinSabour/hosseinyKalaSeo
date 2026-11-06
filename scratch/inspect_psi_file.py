with open('scratch/psi_report.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Length of html:", len(text))
matches = [m.start() for m in re.finditer(r'p31vkp5f3e', text)]
print("Occurrences of report id:", len(matches))
for idx in matches[:3]:
    print("--- Context ---")
    print(text[max(0, idx-100):min(len(text), idx+200)])

# Find where JSON or data is
m_json = re.findall(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', text)
if m_json:
    print("Found INITIAL_STATE!")
else:
    print("INITIAL_STATE not found")
