with open('scratch/psi_report.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
cbs = re.findall(r'AF_initDataCallback\s*\(\s*({[\s\S]*?})\s*\);', text)
print("AF_initDataCallback blocks found:", len(cbs))
for i, block in enumerate(cbs):
    print(f"Block {i} length: {len(block)}")
    if 'score' in block.lower() or 'accessibility' in block.lower():
        print(f"  Block {i} contains keywords!")
        with open(f'scratch/af_block_{i}.js', 'w', encoding='utf-8') as out:
            out.write(block)
