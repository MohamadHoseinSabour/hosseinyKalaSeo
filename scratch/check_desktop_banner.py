with open('scratch/live_page.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'(<img[^>]*clover-home-appliances-october-sale-banner[^>]*>)', text)
if m:
    print("Desktop banner IMG tag:\n", m.group(1))
else:
    print("Desktop banner IMG tag not found")
