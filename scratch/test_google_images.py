import os
import sys
import time
import urllib.parse
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

def search_google_images(page, query):
    encoded_q = urllib.parse.quote(query)
    url = f"https://www.google.com/search?tbm=isch&q={encoded_q}"
    print(f"Searching Google Images: {query}")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=15000)
        time.sleep(1.5)
        
        # Get image elements
        # In Google Images, images are in img elements with src or data-src
        imgs = page.query_selector_all("table img, div img[src^='http'], div img[src^='data:image']")
        print(f"Found {len(imgs)} images on Google Images")
        
        results = []
        for img in imgs[:10]:
            src = img.get_attribute("src")
            alt = img.get_attribute("alt")
            if src and not src.startswith("data:"):
                results.append({'alt': alt, 'src': src})
                
        # Also let's inspect web search results
        return results
    except Exception as e:
        print(f"Error: {e}")
        return []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    res = search_google_images(page, "پتوشور پاکیزان 30 کیلو")
    print(f"Results: {len(res)}")
    for r in res[:3]:
        print(" -", r)
    browser.close()
