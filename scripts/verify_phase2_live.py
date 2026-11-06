import urllib.request
import json
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
print("PHASE 2 SCHEMA & E-E-A-T LIVE VERIFICATION")
print("="*60)

# TEST 1: PRODUCT SCHEMA (DEPOINT DECENT REFRIGERATOR)
print("\n[TEST 1] Product Schema (https://hosseinykala.ir/product/depoint-decent-combi-refrigerator-freezer/):")
try:
    prod_html = fetch('https://hosseinykala.ir/product/depoint-decent-combi-refrigerator-freezer/')
    soup_prod = BeautifulSoup(prod_html, 'html.parser')
    s_tag = soup_prod.find('script', type='application/ld+json')
    if s_tag:
        data = json.loads(s_tag.string)
        prod_entity = next((item for item in data.get('@graph', []) if item.get('@type') == 'Product'), None)
        if prod_entity:
            offers = prod_entity.get('offers', {})
            print("  - Offer @type:", offers.get('@type'))
            print("  - Price:", offers.get('price'), offers.get('priceCurrency'))
            print("  - Has Return Policy:", 'hasMerchantReturnPolicy' in offers)
            print("  - Has Shipping Details:", 'shippingDetails' in offers)
            print("  - Seller @type:", offers.get('seller', {}).get('@type'))
            
            if offers.get('@type') == 'Offer' and 'hasMerchantReturnPolicy' in offers and 'shippingDetails' in offers:
                print("✅ PASS: Product schema fully Google Merchant compliant!")
            else:
                print("❌ FAIL: Product schema still missing merchant properties.")
        else:
            print("❌ FAIL: Product entity not found in @graph")
    else:
        print("❌ FAIL: No JSON-LD found on product page")
except Exception as e:
    print("Error testing product schema:", e)

# TEST 2: HOMEPAGE SCHEMA
print("\n[TEST 2] Homepage Schema (https://hosseinykala.ir/):")
try:
    home_html = fetch('https://hosseinykala.ir/')
    soup_home = BeautifulSoup(home_html, 'html.parser')
    s_tag = soup_home.find('script', type='application/ld+json')
    if s_tag:
        data = json.loads(s_tag.string)
        graph = data.get('@graph', [])
        
        has_article = any(item.get('@type') == 'Article' or (isinstance(item.get('@type'), list) and 'Article' in item.get('@type')) for item in graph)
        print("  - Article schema on homepage:", has_article)
        
        store_entity = next((item for item in graph if 'HomeGoodsStore' in str(item.get('@type')) or 'Store' in str(item.get('@type'))), None)
        if store_entity:
            print("  - Store @type:", store_entity.get('@type'))
            print("  - Name:", store_entity.get('name'))
            print("  - Geo Coordinates:", store_entity.get('geo'))
            print("  - Address:", store_entity.get('address', {}).get('addressLocality'))
            
            if not has_article and store_entity.get('geo'):
                print("✅ PASS: Homepage schema successfully converted to HomeGoodsStore with Ahvaz Geo and 0 Article schemas!")
            else:
                print("❌ FAIL: Homepage schema issues remain.")
        else:
            print("❌ FAIL: No HomeGoodsStore entity found on homepage.")
    else:
        print("❌ FAIL: No JSON-LD found on homepage")
except Exception as e:
    print("Error testing homepage schema:", e)

# TEST 3: BLOG POST E-E-A-T AUTHOR
print("\n[TEST 3] Blog Post Schema & Author Persona:")
try:
    blog_html = fetch('https://hosseinykala.ir/home-appliances-installment-buying-guide/')
    soup_blog = BeautifulSoup(blog_html, 'html.parser')
    s_tag = soup_blog.find('script', type='application/ld+json')
    if s_tag:
        data = json.loads(s_tag.string)
        graph = data.get('@graph', [])
        post_entity = next((item for item in graph if item.get('@type') in ['BlogPosting', 'Article']), None)
        if post_entity:
            author = post_entity.get('author', {})
            print("  - Author Name:", author.get('name'))
            print("  - Author JobTitle:", author.get('jobTitle'))
            if author.get('name') == 'تیم کارشناسی حسینی کالا':
                print("✅ PASS: Blog author persona successfully updated to 'تیم کارشناسی حسینی کالا'!")
            else:
                print(f"❌ FAIL: Author name is {author.get('name')}")
        else:
            print("❌ FAIL: BlogPosting entity not found in @graph")
    else:
        print("❌ FAIL: No JSON-LD found on blog post")
except Exception as e:
    print("Error testing blog post schema:", e)

print("\n" + "="*60)
