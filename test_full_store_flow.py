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

async def test_full_store_wizard():
    async with async_playwright() as p:
        b = await p.chromium.launch_persistent_context('divar_session', channel='chrome', headless=False, viewport={"width": 1280, "height": 900})
        page = b.pages[0] if b.pages else await b.new_page()
        
        print("[STORE TEST] Opening Store Ad Registration URL:", STORE_NEW_URL)
        await page.goto(STORE_NEW_URL, wait_until="networkidle")
        await asyncio.sleep(2)
        
        # Step 1: Title and Image
        test_title = "یخچال فریزر دوقلو کلور در اهواز - اقساط"
        await page.locator('input[name="Title"]').fill(test_title)
        
        # Upload 3 images
        img_folder = os.path.abspath(r"divar_ads\01_یخچال_دوقلو_کلور\images")
        all_imgs = [os.path.join(img_folder, f) for f in os.listdir(img_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))][:3]
        print(f"[STORE TEST] Uploading {len(all_imgs)} images...")
        await page.locator('input[type="file"]').set_input_files(all_imgs)
        await asyncio.sleep(3)
        await page.screenshot(path="store_wizard_s1.png")
        
        # Step 1 -> Next
        await page.locator('button[type="submit"]:has-text("بعدی")').click()
        print("[STORE TEST] Moving to Step 2...")
        await asyncio.sleep(3)
        await page.screenshot(path="store_wizard_s2.png")
        
        s2_text = await page.locator("body").inner_text()
        with open("store_s2_text.txt", "w", encoding="utf-8") as f:
            f.write(s2_text)
            
        # Check if Location needs selection or is prefilled
        loc_btn = page.locator('div:has-text("مکان آگهی*") button.kt-action-field, button:has-text("انتخاب")').first
        if await loc_btn.is_visible(timeout=2000):
            print("[STORE TEST] Location selection required. Opening map...")
            await loc_btn.click()
            await asyncio.sleep(2)
            canvas = page.locator('canvas').first
            if await canvas.is_visible():
                box = await canvas.bounding_box()
                if box:
                    cx = box['x'] + box['width'] / 2
                    cy = box['y'] + box['height'] / 2
                    await page.mouse.move(cx, cy)
                    await page.mouse.down()
                    await page.mouse.move(cx + 30, cy + 30, steps=5)
                    await page.mouse.up()
                    await asyncio.sleep(2)
            await page.locator('button:has-text("تأیید")').first.click()
            await asyncio.sleep(2)

        # Status: Select "نو"
        status_btn = page.locator('button[name="status"]')
        if await status_btn.is_visible(timeout=2000):
            await status_btn.click()
            await asyncio.sleep(1)
            new_opt = page.locator('.kt-select-dropdown__item:has-text("نو"), div[role="button"]:has-text("نو"), .kt-selector-row:has-text("نو"), li:has-text("نو")').first
            if await new_opt.is_visible():
                await new_opt.click()
            await asyncio.sleep(1)

        # Price: 100000000
        price_input = page.locator('input[name="price"]')
        if await price_input.is_visible(timeout=2000):
            await price_input.fill("100000000")
            await asyncio.sleep(1)

        await page.screenshot(path="store_wizard_s2_filled.png")
        
        # Step 2 -> Step 3
        print("[STORE TEST] Clicking Next to Step 3...")
        await page.locator('button[type="submit"]:has-text("بعدی")').click()
        await asyncio.sleep(4)
        await page.screenshot(path="store_wizard_s3.png")

        # Step 3: Description
        desc_input = page.locator('textarea[name="Description"]')
        if await desc_input.is_visible(timeout=3000):
            print("[STORE TEST] Filling Description...")
            with open(r"divar_ads\01_یخچال_دوقلو_کلور\ad_content.txt", encoding="utf-8") as f:
                desc_text = f.read()
            # Clean header if any
            clean_desc = desc_text
            if "====================" in clean_desc:
                clean_desc = clean_desc.split("====================")[-1].strip()
            if "متن آگهی:" in clean_desc:
                clean_desc = clean_desc.split("متن آگهی:")[-1].strip()
            await desc_input.fill(clean_desc)
            await asyncio.sleep(2)
            
        await page.screenshot(path="store_wizard_s3_filled.png")

        # Step 3 -> Step 4
        print("[STORE TEST] Clicking Next to Step 4...")
        await page.locator('button[type="submit"]:has-text("بعدی")').click()
        await asyncio.sleep(4)
        await page.screenshot(path="store_wizard_s4.png")
        
        s4_text = await page.locator("body").inner_text()
        with open("store_s4_text.txt", "w", encoding="utf-8") as f:
            f.write(s4_text)
            
        print("[STORE TEST] Step 4 reached successfully!")
        print("[STORE TEST] Stopping here in the browser so ad stays as draft / preview.")
        print("[STORE TEST] Waiting 10 seconds before close for inspection...")
        await asyncio.sleep(10)
        await b.close()

if __name__ == '__main__':
    asyncio.run(test_full_store_wizard())
