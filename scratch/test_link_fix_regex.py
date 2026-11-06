with open('scratch/live_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
from bs4 import BeautifulSoup

def fix_empty_links(content):
    # Fix category image links and discount image links
    def replacer(m):
        attrs = m.group(1)
        if 'aria-label' in attrs:
            return m.group(0)
        
        href_match = re.search(r'href=["\']([^"\']+)["\']', attrs)
        href = href_match.group(1) if href_match else ''
        
        label = "مشاهده جزئیات و خرید"
        if "یخچال" in href or "refrigerator" in href:
            label = "خرید و قیمت یخچال و فریزر"
        elif "لباسشویی" in href or "washing" in href:
            label = "خرید و قیمت ماشین لباسشویی"
        elif "ظرفشویی" in href or "dishwasher" in href:
            label = "خرید و قیمت ماشین ظرفشویی"
        elif "کولر" in href or "cooling" in href:
            label = "خرید و قیمت کولر آبی"
        elif "تخفیف" in href:
            label = "مشاهده تخفیف‌ها و پیشنهادات ویژه"
        elif "trustseal" in href or "enamad" in href:
            label = "نماد اعتماد الکترونیکی حسینی کالا"
        elif href == "#":
            label = "لینک ناوبری"
            
        return f'<a{attrs} aria-label="{label}">'

    # Regex to find <a ...> that enclose <img alt="" ...>
    content = re.sub(r'<a\b([^>]*?)>(?=\s*<img\b[^>]*\balt=["\']\s*["\'])', replacer, content)
    # Also fix <a href="#">
    content = re.sub(r'<a\b([^>]*?href=["\']#["\'][^>]*?)>', replacer, content)
    return content

fixed_html = fix_empty_links(html)
soup = BeautifulSoup(fixed_html, 'html.parser')

empty_links_after = []
for i, l in enumerate(soup.find_all('a')):
    text = l.get_text(strip=True)
    aria_label = l.get('aria-label')
    aria_labelledby = l.get('aria-labelledby')
    title = l.get('title')
    img = l.find('img')
    img_alt = img.get('alt') if img else None
    
    if not (text or aria_label or aria_labelledby or title or (img and img_alt)):
        empty_links_after.append((i, l.get('href'), str(l)[:120]))

print(f"Empty links before: 11 | Empty links after: {len(empty_links_after)}")
for it in empty_links_after:
    print(it)
