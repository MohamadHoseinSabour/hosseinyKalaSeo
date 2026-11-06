import asyncio
import os
from playwright.async_api import async_playwright
from divar_store_auto_poster import SESSION_DIR, STORE_NEW_URL, set_ahvaz_location, DEFAULT_PRICE

async def run_and_dump():
    async with async_playwright() as p:
        b = await p.chromium.launch_persistent_context(SESSION_DIR, channel='chrome', headless=False)
        page = b.pages[0] if b.pages else await b.new_page()
        await page.goto(STORE_NEW_URL, wait_until='networkidle')
        await asyncio.sleep(2)
        await page.locator('input[name="Title"]').fill('یخچال فریزر دوقلو کلور در اهواز - اقساط')
        img = os.path.abspath(r'divar_ads\01_یخچال_دوقلو_کلور\images\clover-economy-27ft-twin-refrigerator.jpg')
        await page.locator('input[type="file"]').set_input_files(img)
        await asyncio.sleep(2)
        await page.locator('button[type="submit"]:has-text("بعدی")').click()
        await asyncio.sleep(3)
        
        await set_ahvaz_location(page)
        await asyncio.sleep(1)
        
        status_btn = page.locator('button[name="status"]')
        if await status_btn.is_visible():
            await status_btn.click()
            await asyncio.sleep(1)
            new_opt = page.locator('.kt-select-dropdown__item:has-text("نو"), div[role="button"]:has-text("نو"), .kt-selector-row:has-text("نو"), li:has-text("نو")').first
            if await new_opt.is_visible():
                await new_opt.click()
            await asyncio.sleep(1)
            
        price_input = page.locator('input[name="price"]')
        if await price_input.is_visible():
            await price_input.fill(DEFAULT_PRICE)
            await asyncio.sleep(1)
            
        await page.locator('button[type="submit"]:has-text("بعدی")').first.click()
        await asyncio.sleep(3)
        
        text = await page.locator('body').inner_text()
        with open('step2_validation_dump.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        print('Saved step2_validation_dump.txt')
        await b.close()

if __name__ == '__main__':
    asyncio.run(run_and_dump())
