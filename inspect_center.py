import asyncio
import os
import json
from playwright.async_api import async_playwright

STORE_NEW_URL = "https://divar.ir/new/PREMIUM_PANEL/ZhWFYgaK_xTlfvkBc"

async def check_center():
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
        
        info = await page.evaluate('''() => {
            const findReact = (el) => {
                for (const k in el) if (k.startsWith('__reactFiber$')) return el[k];
                return null;
            };
            const mapEl = document.querySelector('.mapboxgl-map');
            let f = findReact(mapEl);
            const res = {};
            while (f) {
                if (f.memoizedProps) {
                    if (f.memoizedProps.initialCenter) res.initialCenter = f.memoizedProps.initialCenter;
                    if (f.memoizedProps.location) res.location = f.memoizedProps.location;
                    if (f.memoizedProps.exactLocationData) res.exactLocationData = f.memoizedProps.exactLocationData;
                    if (f.memoizedProps.defaultValuesMap) res.defaultValuesMap = f.memoizedProps.defaultValuesMap;
                    if (f.memoizedProps.mapConfig) res.mapConfig = f.memoizedProps.mapConfig;
                }
                f = f.return;
            }
            return res;
        }''')
        with open('center_info.json', 'w', encoding='utf-8') as out:
            json.dump(info, out, ensure_ascii=False, indent=2)
        print('Saved center_info.json')
        await b.close()

if __name__ == '__main__':
    asyncio.run(check_center())
