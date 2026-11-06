import asyncio
import os
import sys
import json
from playwright.async_api import async_playwright

STORE_NEW_URL = "https://divar.ir/new/PREMIUM_PANEL/ZhWFYgaK_xTlfvkBc"

async def test_search_location():
    async with async_playwright() as p:
        b = await p.chromium.launch_persistent_context('divar_session', channel='chrome', headless=False, viewport={"width": 1280, "height": 900})
        page = b.pages[0] if b.pages else await b.new_page()
        
        await page.goto(STORE_NEW_URL, wait_until="networkidle")
        await asyncio.sleep(2)
        
        # Step 1
        await page.locator('input[name="Title"]').fill("یخچال فریزر دوقلو کلور در اهواز - اقساط")
        img_folder = os.path.abspath(r"divar_ads\01_یخچال_دوقلو_کلور\images")
        first_img = [os.path.join(img_folder, f) for f in os.listdir(img_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))][0]
        await page.locator('input[type="file"]').set_input_files(first_img)
        await asyncio.sleep(2)
        await page.locator('button[type="submit"]:has-text("بعدی")').click()
        await asyncio.sleep(3)
        
        # Step 2: Open location map
        loc_btn = page.locator('div:has-text("مکان آگهی*") button.kt-action-field, button:has-text("انتخاب")').first
        await loc_btn.click()
        await asyncio.sleep(2)
        
        # Search input
        search_input = page.locator('input[placeholder*="جستجوی شهر"], input[placeholder*="محله"]').first
        print("[LOCATION] Found search input:", await search_input.is_visible())
        
        # Type "اهواز، نادری"
        await search_input.fill("اهواز نادری")
        await asyncio.sleep(2)
        await page.screenshot(path="loc_search_results.png")
        
        # Check suggestions
        suggestions = await page.evaluate('''() => {
            const items = document.querySelectorAll('.kt-dimmer li, .kt-dimmer .kt-selector-row, .kt-dimmer div[role="button"], .kt-suggestion-item, .search-result');
            return Array.from(items).map(el => (el.innerText || '').trim().replace(/\\n/g, ' - '));
        }''')
        print("[LOCATION] Suggestions:", json.dumps(suggestions[:10], ensure_ascii=False, indent=2))
        
        # Let's also check if Mapbox object is accessible on window or canvas
        map_coords = await page.evaluate('''() => {
            // Find mapboxgl Map instance
            const mapEl = document.querySelector('.mapboxgl-map');
            if (mapEl && mapEl._map) {
                return { has_map: true, center: mapEl._map.getCenter() };
            }
            return { has_map: false };
        }''')
        print("[LOCATION] Map instance check:", map_coords)

        await asyncio.sleep(4)
        await b.close()

if __name__ == '__main__':
    asyncio.run(test_search_location())
