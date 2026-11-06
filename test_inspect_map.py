import asyncio
import os
import sys
import json
from playwright.async_api import async_playwright

STORE_NEW_URL = "https://divar.ir/new/PREMIUM_PANEL/ZhWFYgaK_xTlfvkBc"

async def inspect_map_react_and_network():
    async with async_playwright() as p:
        b = await p.chromium.launch_persistent_context('divar_session', channel='chrome', headless=False, viewport={"width": 1280, "height": 900})
        page = b.pages[0] if b.pages else await b.new_page()
        
        # Track all network requests
        requests_log = []
        page.on("request", lambda r: requests_log.append(r.url) if "map" in r.url or "place" in r.url or "geo" in r.url or "location" in r.url else None)
        
        await page.goto(STORE_NEW_URL, wait_until="networkidle")
        await asyncio.sleep(2)
        
        await page.locator('input[name="Title"]').fill("یخچال فریزر دوقلو کلور در اهواز - اقساط")
        img_folder = os.path.abspath(r"divar_ads\01_یخچال_دوقلو_کلور\images")
        first_img = [os.path.join(img_folder, f) for f in os.listdir(img_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))][0]
        await page.locator('input[type="file"]').set_input_files(first_img)
        await asyncio.sleep(2)
        await page.locator('button[type="submit"]:has-text("بعدی")').click()
        await asyncio.sleep(3)
        
        # Click location
        await page.locator('div:has-text("مکان آگهی*") button.kt-action-field, button:has-text("انتخاب")').first.click()
        await asyncio.sleep(2)
        
        # Inspect React Fiber on the map container
        react_info = await page.evaluate('''() => {
            const findReact = (el) => {
                for (const key in el) {
                    if (key.startsWith('__reactFiber$') || key.startsWith('__reactInternalInstance$')) {
                        return el[key];
                    }
                }
                return null;
            };
            
            const mapEl = document.querySelector('.mapboxgl-map') || document.querySelector('canvas');
            if (!mapEl) return { found: false };
            
            let fiber = findReact(mapEl);
            let depth = 0;
            const findings = [];
            while (fiber && depth < 30) {
                if (fiber.memoizedProps) {
                    const keys = Object.keys(fiber.memoizedProps);
                    for (const k of keys) {
                        if (k.toLowerCase().includes('map') || k.toLowerCase().includes('loc') || k.toLowerCase().includes('change') || k.toLowerCase().includes('coord') || k.toLowerCase().includes('center')) {
                            findings.push({
                                depth,
                                propKey: k,
                                type: typeof fiber.memoizedProps[k]
                            });
                        }
                    }
                }
                fiber = fiber.return;
                depth++;
            }
            return { found: true, findings };
        }''')
        
        print("[DEBUG] React Fiber:", json.dumps(react_info, ensure_ascii=False, indent=2))
        print("[DEBUG] Network URLs with map/place/location:")
        for u in requests_log:
            print("  ", u)
            
        await asyncio.sleep(3)
        await b.close()

if __name__ == '__main__':
    asyncio.run(inspect_map_react_and_network())
