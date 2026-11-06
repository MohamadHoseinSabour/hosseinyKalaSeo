with open('scratch/live_page.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'(<img[^>]*clover-october-sale-square-banner[^>]*>)', text)
if m:
    print("Full IMG tag:")
    print(m.group(1))
else:
    print("Not found by regex")
