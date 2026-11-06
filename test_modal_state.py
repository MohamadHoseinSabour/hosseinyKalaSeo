import asyncio
import os
from playwright.async_api import async_playwright

STORE_NEW_URL = "https://divar.ir/new/PREMIUM_PANEL/ZhWFYgaK_xTlfvkBc"

async def check():
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
        
        # Open location
        await page.locator('div:has-text("مکان آگهی*") button.kt-action-field, button:has-text("انتخاب")').first.click()
        await asyncio.sleep(2)
        
        # Set Ahvaz via onSubmit
        await page.evaluate('''() => {
            const findReact = (el) => {
                for (const k in el) if (k.startsWith('__reactFiber$')) return el[k];
                return null;
            };
            const mapEl = document.querySelector('.mapboxgl-map') || document.querySelector('canvas');
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
                onSubmitFn({
                    center: [48.6840, 31.3220],
                    cityId: 7,
                    neighbourhoodId: 328
                });
            }
        }''')
        await asyncio.sleep(2)
        
        dimmer = page.locator('.kt-dimmer--open')
        print("Dimmer open count:", await dimmer.count())
        
        # Check confirm button
        confirm_btn = page.locator('.kt-dimmer button:has-text("تأیید")').first
        if await confirm_btn.is_visible():
            print("Confirm button disabled?", await confirm_btn.get_attribute("disabled"))
            await confirm_btn.click()
            print("Clicked confirm button!")
            await asyncio.sleep(2)
            
        print("Dimmer open after confirm:", await dimmer.count())
        await page.screenshot(path="after_modal_fix.png")
        await b.close()

if __name__ == '__main__':
    asyncio.run(check())
