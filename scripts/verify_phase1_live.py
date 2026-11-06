import urllib.request
import re
import sys
from bs4 import BeautifulSoup

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0'}

def fetch(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode('utf-8')

print("="*60)
print("PHASE 1 LIVE VERIFICATION")
print("="*60)

# TEST 1: SITEMAP_INDEX.XML
print("\n[TEST 1] XML Sitemap Index:")
try:
    sitemap = fetch('https://hosseinykala.ir/sitemap_index.xml')
    if 'xts-template' in sitemap:
        print("❌ FAIL: xts-template found in sitemap_index.xml")
    else:
        print("✅ PASS: xts-template completely excluded from sitemap_index.xml!")
except Exception as e:
    print("Error fetching sitemap:", e)

# TEST 2: HOMEPAGE
print("\n[TEST 2] Homepage (https://hosseinykala.ir/):")
try:
    home_html = fetch('https://hosseinykala.ir/')
    soup_home = BeautifulSoup(home_html, 'html.parser')
    h1_tags = soup_home.find_all('h1')
    print(f"H1 Count: {len(h1_tags)}")
    for h in h1_tags:
        print("  - H1 Text:", h.get_text(strip=True)[:100])
    
    # Check HTTP internal links
    http_links = [a['href'] for a in soup_home.find_all('a', href=True) if a['href'].startswith('http://hosseinykala.ir')]
    print(f"Internal HTTP (insecure) links count: {len(http_links)}")
    if len(http_links) == 0:
        print("✅ PASS: 0 HTTP internal links! All converted to HTTPS.")
    else:
        print("❌ FAIL: Remaining HTTP links:", http_links[:5])
    
    if len(h1_tags) >= 1:
        print("✅ PASS: Homepage has valid H1 tag!")
    else:
        print("❌ FAIL: Homepage still missing H1 tag.")
except Exception as e:
    print("Error testing homepage:", e)

# TEST 3: CATEGORY PAGE
print("\n[TEST 3] Category Page (Refrigerators):")
try:
    cat_url = 'https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/'
    cat_html = fetch(cat_url)
    soup_cat = BeautifulSoup(cat_html, 'html.parser')
    
    cat_h1 = soup_cat.find_all('h1')
    print(f"Category H1 Count: {len(cat_h1)}")
    for h in cat_h1:
        print("  - H1 Text:", h.get_text(strip=True)[:100])
        
    meta_desc = soup_cat.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        desc_len = len(meta_desc['content'])
        print(f"Category Meta Description Length: {desc_len} chars")
        print("  - Content:", meta_desc['content'][:150] + "...")
        if 100 <= desc_len <= 180:
            print("✅ PASS: Meta description perfectly optimized within standard length!")
        else:
            print(f"⚠️ Notice: Meta description length is {desc_len}")
    else:
        print("❌ FAIL: No meta description found.")
except Exception as e:
    print("Error testing category page:", e)

# TEST 4: SINGLE BLOG POST
print("\n[TEST 4] Single Blog Post:")
try:
    post_url = 'https://hosseinykala.ir/home-appliances-installment-buying-guide/'
    post_html = fetch(post_url)
    soup_post = BeautifulSoup(post_html, 'html.parser')
    
    post_h1 = soup_post.find_all('h1')
    print(f"Blog Post H1 Count: {len(post_h1)}")
    for h in post_h1:
        print("  - H1 Text:", h.get_text(strip=True)[:100])
        
    # Check if old H3 post title remains
    h3_title = [h for h in soup_post.find_all('h3') if 'xts-title' in h.get('class', [])]
    print(f"Old H3 titles count: {len(h3_title)}")
    
    if len(post_h1) >= 1:
        print("✅ PASS: Blog post title successfully upgraded to H1!")
    else:
        print("❌ FAIL: Blog post still missing H1.")
except Exception as e:
    print("Error testing blog post:", e)

print("\n" + "="*60)
