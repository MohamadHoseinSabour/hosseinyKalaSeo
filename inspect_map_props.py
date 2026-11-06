import asyncio
import os
import json
from playwright.async_api import async_playwright

STORE_NEW_URL = "https://divar.ir/new/PREMIUM_PANEL/ZhWFYgaK_xTlfvkBc"

async def inspect_fiber_methods():
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
            const mapEl = document.querySelector('canvas') || document.querySelector('.mapboxgl-map');
            let f = findReact(mapEl);
            let d = 0;
            const res = {};
            while (f && d < 35) {
                if (f.memoizedProps) {
                    for (const k in f.memoizedProps) {
                        if (typeof f.memoizedProps[k] === 'function') {
                            res[`d${d}_${k}`] = 'function';
                        } else if (['initialCenter', 'location', 'defaultValuesMap', 'exactLocationData'].includes(k)) {
                            res[`d${d}_${k}`] = f.memoizedProps[k];
                        }
                    }
                }
                f = f.return;
                d++;
            }
            return res;
        }''')
        with open('fiber_methods.json', 'w', encoding='utf-8') as out:
            json.dump(info, out, ensure_ascii=False, indent=2)
        print('Saved fiber_methods.json. Keys count:', len(info))
        await b.close()

if __name__ == '__main__':
    asyncio.run(inspect_fiber_methods())
