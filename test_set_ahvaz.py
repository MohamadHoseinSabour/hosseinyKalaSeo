import asyncio
import os
import json
from playwright.async_api import async_playwright

STORE_NEW_URL = "https://divar.ir/new/PREMIUM_PANEL/ZhWFYgaK_xTlfvkBc"

async def test_set_ahvaz_location():
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

        # Call onSubmit directly with Ahvaz Naderi coordinates!
        result = await page.evaluate('''() => {
            const findReact = (el) => {
                for (const k in el) if (k.startsWith('__reactFiber$')) return el[k];
                return null;
            };
            const mapEl = document.querySelector('.mapboxgl-map');
            let f = findReact(mapEl);
            let onSubmitFn = null;
            let onCloseFn = null;
            while (f) {
                if (f.memoizedProps) {
                    if (f.memoizedProps.onSubmit && !onSubmitFn) onSubmitFn = f.memoizedProps.onSubmit;
                    if (f.memoizedProps.onClose && !onCloseFn) onCloseFn = f.memoizedProps.onClose;
                }
                f = f.return;
            }
            
            if (onSubmitFn) {
                // Call onSubmit with Ahvaz Naderi
                // Center: [longitude, latitude] = [48.6838, 31.3224]
                // CityId: 7 (Ahvaz)
                // NeighbourhoodId: 328 (Naderi)
                onSubmitFn({
                    center: [48.6838, 31.3224],
                    cityId: 7,
                    neighbourhoodId: 328,
                    onSuccess: () => {
                        if (onCloseFn) onCloseFn();
                    }
                });
                return { success: true };
            }
            return { success: false };
        }''')
        
        print("[LOCATION SET RESULT]:", result)
        await asyncio.sleep(3)
        
        # Take screenshot of Step 2 after setting location
        await page.screenshot(path="after_setting_ahvaz.png")
        
        # Check text on Step 2
        body_text = await page.locator("body").inner_text()
        with open("after_loc_text.txt", "w", encoding="utf-8") as out:
            out.write(body_text)
            
        print("[LOCATION CONFIRMATION TEXT]:")
        for line in [l.strip() for l in body_text.split('\n') if l.strip()][:25]:
            print("  |", line)
            
        await asyncio.sleep(3)
        await b.close()

if __name__ == '__main__':
    asyncio.run(test_set_ahvaz_location())
