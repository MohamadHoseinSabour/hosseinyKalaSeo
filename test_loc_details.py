import asyncio
import os
import sys
import json
from playwright.async_api import async_playwright

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

STORE_NEW_URL = "https://divar.ir/new/PREMIUM_PANEL/ZhWFYgaK_xTlfvkBc"

async def test_location_inspection():
    async with async_playwright() as p:
        b = await p.chromium.launch_persistent_context('divar_session', channel='chrome', headless=False, viewport={"width": 1280, "height": 900})
        page = b.pages[0] if b.pages else await b.new_page()
        
        await page.goto(STORE_NEW_URL, wait_until="networkidle")
        await asyncio.sleep(2)
        
        # Step 1: Fill title
        await page.locator('input[name="Title"]').fill("یخچال فریزر دوقلو کلور در اهواز - اقساط")
        
        # Upload 1 image
        img_folder = os.path.abspath(r"divar_ads\01_یخچال_دوقلو_کلور\images")
        first_img = [os.path.join(img_folder, f) for f in os.listdir(img_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))][0]
        await page.locator('input[type="file"]').set_input_files(first_img)
        await asyncio.sleep(2)
        
        # Next -> Step 2
        await page.locator('button[type="submit"]:has-text("بعدی")').click()
        await asyncio.sleep(3)
        
        # Now on Step 2: Open location
        loc_btn = page.locator('div:has-text("مکان آگهی*") button.kt-action-field, button:has-text("انتخاب")').first
        await loc_btn.click()
        await asyncio.sleep(2)
        
        # Check map instance on window or elements
        map_info = await page.evaluate('''() => {
            const res = {};
            // Look for mapboxgl or leaflet or similar
            const canvases = document.querySelectorAll('canvas');
            res.canvasCount = canvases.length;
            
            // Check all input or search fields in modal
            const inputs = Array.from(document.querySelectorAll('.kt-dimmer input, .kt-dimmer button')).map(e => ({
                tag: e.tagName,
                text: (e.innerText || e.placeholder || '').trim(),
                className: e.className
            }));
            res.inputs = inputs;
            
            // Check if mapboxgl map instance can be found on canvas or container
            for (const c of canvases) {
                const parent = c.closest('.mapboxgl-map') || c.parentElement;
                if (parent) {
                    res.parentClass = parent.className;
                }
            }
            return res;
        }''')
        
        print("[DEBUG] Map info:", json.dumps(map_info, ensure_ascii=False, indent=2))
        await page.screenshot(path="loc_inspection.png")
        
        await b.close()

if __name__ == '__main__':
    asyncio.run(test_location_inspection())
