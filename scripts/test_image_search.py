import sys
import os
import time
import urllib.parse
import requests
from playwright.sync_api import sync_playwright
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

def search_candidate_images(query, max_candidates=5):
    print(f"Searching for: {query}")
    candidates = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # Search via Google Images or Torob
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}&tbm=isch"
        
        try:
            page.goto(search_url, wait_until="networkidle", timeout=20000)
            page.wait_for_timeout(2000)
            
            # Find image elements
            img_elements = page.query_selector_all("img")
            print(f"Found {len(img_elements)} img tags on page")
            
            for img in img_elements:
                src = img.get_attribute("src") or img.get_attribute("data-src")
                if src and src.startswith("http") and not "google.com" in src:
                    candidates.append(src)
                elif src and src.startswith("https://encrypted-tbn0.gstatic.com"):
                    candidates.append(src)
                if len(candidates) >= max_candidates:
                    break
        except Exception as e:
            print(f"Search error: {e}")
        finally:
            browser.close()
            
    print(f"Collected {len(candidates)} candidates")
    return candidates

if __name__ == "__main__":
    results = search_candidate_images("یخچال و فریزر دوقلو هیمالیا مدل آیس پول 60MW")
    for idx, r in enumerate(results):
        print(f"[{idx+1}] {r[:100]}...")
