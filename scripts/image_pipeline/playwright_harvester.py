import os
import sys
import time
import urllib.parse
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

def search_torob_playwright(page, query):
    """
    Navigates to Torob search page for query and extracts top product title and image URL.
    """
    encoded_q = urllib.parse.quote(query)
    url = f"https://torob.com/search/?query={encoded_q}"
    print(f"Searching Torob: {query} -> {url}")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=15000)
        time.sleep(2) # allow react components to render
        
        # Look for product cards
        # In Torob, product cards contain img elements and product links
        cards = page.query_selector_all("div[class*='ProductCard_'], a[class*='ProductCard_'], div[data-testid='product-card'], div[class*='card_']")
        print(f"Found {len(cards)} card elements on Torob")
        
        results = []
        for card in cards[:5]:
            title_el = card.query_selector("h2, h3, a[title], [class*='title'], [class*='name']")
            img_el = card.query_selector("img")
            
            title = title_el.inner_text().strip() if title_el else ""
            if not title and card.get_attribute("title"):
                title = card.get_attribute("title").strip()
                
            img_src = img_el.get_attribute("src") if img_el else None
            if not img_src and img_el:
                img_src = img_el.get_attribute("data-src")
                
            if img_src and title:
                # Remove resizing parameters if present to get high-res
                # e.g., torob image urls often end with /webp/ or have resize params
                results.append({'title': title, 'image_url': img_src})
                
        return results
    except Exception as e:
        print(f"Torob search error for {query}: {e}")
        return []

def main():
    test_queries = [
        "پتوشور پاکیزان 30",
        "ماشین لباسشویی پاکشوما دوقلو 15",
        "لباسشویی هیمالیا تسلا پرو 10 کیلو",
        "یخچال کمبی نیکسان 8410"
    ]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()
        
        for q in test_queries:
            res = search_torob_playwright(page, q)
            print(f"Results for '{q}': {len(res)}")
            for r in res[:2]:
                print(f"  - {r['title']} : {r['image_url']}")
                
        browser.close()

if __name__ == '__main__':
    main()
