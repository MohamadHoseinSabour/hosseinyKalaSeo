import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Try searching Torob
    query = "اسپرسوساز وستینگهاوس 1663"
    url = f"https://torob.com/search/?query={query}"
    print(f"Navigating to {url}...")
    page.goto(url, wait_until="networkidle", timeout=20000)
    
    # Check titles and images
    cards = page.query_selector_all("div.ProductCard_wrapper__3jZ2i, a[href*='/p/']")
    print(f"Found {len(cards)} card elements")
    
    # Get all product links or images
    products = page.query_selector_all("a[href*='/p/']")
    for idx, prod in enumerate(products[:5]):
        text = prod.inner_text().replace('\n', ' ')
        img = prod.query_selector("img")
        img_src = img.get_attribute("src") if img else None
        print(f"[{idx+1}] Text: {text[:60]} | Img: {img_src}")
        
    browser.close()
