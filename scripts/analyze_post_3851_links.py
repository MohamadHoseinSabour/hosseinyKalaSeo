import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/post_3851_current_content.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all matches
matches = list(re.finditer(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', content, re.DOTALL))
print(f"Total <a> tags: {len(matches)}\n")

for i, m in enumerate(matches, 1):
    full = m.group(0)
    href = m.group(1)
    text = m.group(2)
    clean_text = re.sub(r'<[^>]+>', '', text).strip()
    
    # Check type
    link_type = "OTHER"
    if href == "https://hosseinykala.ir/":
        link_type = "HOMEPAGE (KEEP)"
    elif "/product-category/" in href:
        link_type = "CATEGORY (KEEP)"
    elif "/product/" in href:
        link_type = "PRODUCT (REMOVE/UNLINK)"
    elif any(x in href for x in ["refah-bank", "bajet", "mellat", "sayadi", "mehr-iran"]):
        link_type = "ARTICLE (REMOVE/UNLINK)"
        
    print(f"#{i} [{link_type}]")
    print(f"   HREF: {href}")
    print(f"   TEXT: {clean_text}")
    print(f"   SNIPPET: {full[:100]}...\n")
