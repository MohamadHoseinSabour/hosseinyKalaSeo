import asyncio
import os
import json
from playwright.async_api import async_playwright

STORE_NEW_URL = "https://divar.ir/new/PREMIUM_PANEL/ZhWFYgaK_xTlfvkBc"

async def test_find_map_instance():
    async with async_playwright() as p:
        b = await p.chromium.launch_persistent_context('divar_session', channel='chrome', headless=False)
        page = b.pages[0] if b.pages else await b.new_page()
        await page.goto(STORE_NEW_URL, wait_until='networkidle')
        await asyncio.sleep(2)
        await page.locator('input[name="Title"]').fill('یخچال فریزر دوقلو کلور در اهواز - اقساط')
        img = os.path.abspath(r'divar_ads\01_یخچال_دوقلو_کلور\images\clover-economy-27ft-twin-refrigerator.jpg')
        await page.locator('input[type="file"]').set_input_files(img)
        await asyncio.sleep(2)
        await page.locator('button[type="submit"]:has-text("بعدی")').click()
        await asyncio.sleep(3)
        await page.locator('div:has-text("مکان آگهی*") button.kt-action-field, button:has-text("انتخاب")').first.click()
        await asyncio.sleep(2)

        # Inspect all properties of mapbox container and its parent React fibers
        res = await page.evaluate('''() => {
            const findReact = (el) => {
                for (const k in el) if (k.startsWith('__reactFiber$')) return el[k];
                return null;
            };
            
            const mapEl = document.querySelector('.mapboxgl-map');
            if (!mapEl) return { found: false };
            
            let fiber = findReact(mapEl);
            let targetFiber = null;
            let current = fiber;
            while (current) {
                if (current.memoizedProps && current.memoizedProps.onConfirm) {
                    targetFiber = current;
                    break;
                }
                if (current.memoizedProps && current.memoizedProps.onSubmit) {
                    targetFiber = current;
                    break;
                }
                current = current.return;
            }
            
            const propsList = [];
            current = fiber;
            let depth = 0;
            while (current && depth < 30) {
                if (current.memoizedProps) {
                    propsList.push({
                        depth,
                        keys: Object.keys(current.memoizedProps).filter(k => typeof current.memoizedProps[k] === 'function')
                    });
                }
                current = current.return;
                depth++;
            }
            
            return {
                found: true,
                propsList
            };
        }''')
        
        print("[DEBUG] Fiber callback inspect:", json.dumps(res, ensure_ascii=False, indent=2))
        await b.close()

if __name__ == '__main__':
    asyncio.run(test_find_map_instance())
