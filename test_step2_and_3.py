import asyncio
import os
import sys
import json

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from playwright.async_api import async_playwright

SESSION_DIR = os.path.abspath("divar_session")

async def test_complete_step2_and_beyond():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            channel="chrome",
            headless=False,
            viewport={"width": 1280, "height": 900},
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else await browser.new_page()
        
        print("[STEP 1] Navigating to https://divar.ir/new ...")
        await page.goto("https://divar.ir/new", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)
        
        # Close any popups
        for sel in ['button:has-text("متوجه شدم")', 'button:has-text("بستن")']:
            try:
                btn = page.locator(sel).first
                if await btn.is_visible(timeout=1000):
                    await btn.click()
            except Exception:
                pass

        # Step 1: Title & Image
        test_title = "یخچال فریزر دوقلو کلور در اهواز - اقساط"
        await page.locator('input[name="Title"]').fill(test_title)
        
        img_folder = os.path.abspath(r"divar_ads\01_یخچال_دوقلو_کلور\images")
        first_img = [os.path.join(img_folder, f) for f in os.listdir(img_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))][0]
        print(f"[STEP 1] Using test image: {os.path.basename(first_img)}")
        await page.locator('input[type="file"]').set_input_files(first_img)
        await asyncio.sleep(3)
        
        # Click Next
        await page.locator('button[type="submit"]:has-text("بعدی")').first.click()
        print("[STEP 1 -> STEP 2] Navigated to Step 2")
        await asyncio.sleep(3)
        await page.screenshot(path="walk_step2_initial.png")

        # Step 2: Location (مکان آگهی)
        print("[STEP 2] Handling Location...")
        loc_row = page.locator('button:has-text("انتخاب")').first
        if await loc_row.is_visible():
            await loc_row.click()
            await asyncio.sleep(2)
            await page.screenshot(path="walk_step2_location_modal.png")
            
            # Dump location modal elements
            loc_elements = await page.evaluate('''() => {
                const els = document.querySelectorAll('.kt-new-modal input, .kt-new-modal button, .kt-new-modal li, .kt-new-modal .kt-selector-row');
                return Array.from(els).map(el => (el.innerText || el.placeholder || '').trim());
            }''')
            print("[STEP 2] Location modal elements count:", len(loc_elements))
            
            # Inside location modal, look for search input or neighborhood options
            search_input = page.locator('.kt-new-modal input[type="search"], .kt-new-modal input.kt-textfield__input').first
            if await search_input.is_visible():
                await search_input.fill("کیانپارس")
                await asyncio.sleep(1)
            
            item = page.locator('.kt-new-modal .kt-selector-row:has-text("کیانپارس"), .kt-new-modal div:has-text("کیانپارس")').first
            if await item.is_visible():
                await item.click()
                print("[STEP 2] Selected location: کیانپارس")
            else:
                first_row = page.locator('.kt-new-modal .kt-selector-row').first
                if await first_row.is_visible():
                    await first_row.click()
                    print("[STEP 2] Selected first location item")
            
            await asyncio.sleep(1)
            # Check if confirm button exists
            confirm_btn = page.locator('.kt-new-modal button:has-text("تأیید"), .kt-new-modal button:has-text("انتخاب")').first
            if await confirm_btn.is_visible():
                await confirm_btn.click()
            await asyncio.sleep(1)

        # Step 2: Status (وضعیت*)
        print("[STEP 2] Handling Status...")
        status_btn = page.locator('button[name="status"]')
        if await status_btn.is_visible():
            await status_btn.click()
            await asyncio.sleep(1)
            await page.screenshot(path="walk_step2_status_modal.png")
            
            # Select "نو"
            new_opt = page.locator('.kt-new-modal div:has-text("نو"), .kt-new-modal .kt-selector-row:has-text("نو"), button:has-text("نو")').first
            if await new_opt.is_visible():
                await new_opt.click()
                print("[STEP 2] Selected status: نو")
            await asyncio.sleep(1)

        # Step 2: Price (قیمت)
        print("[STEP 2] Handling Price...")
        price_input = page.locator('input[name="price"]')
        if await price_input.is_visible():
            await price_input.fill("100000000")
            print("[STEP 2] Filled price: 100000000")

        await asyncio.sleep(1)
        await page.screenshot(path="walk_step2_completed.png")
        
        # Click Next on Step 2
        print("[STEP 2] Clicking Next...")
        await page.locator('button[type="submit"]:has-text("بعدی")').first.click()
        await asyncio.sleep(4)
        await page.screenshot(path="walk_step3_actual.png")

        # Now let's see what is on Step 3!
        step3_text = await page.locator("body").inner_text()
        with open("walk_step3_text.txt", "w", encoding="utf-8") as f:
            f.write(step3_text)

        step3_interactive = await page.evaluate('''() => {
            const els = document.querySelectorAll('input, textarea, button, [role="button"], select, [role="radio"], [role="checkbox"], div.kt-selector-row');
            return Array.from(els).map(el => ({
                tag: el.tagName,
                text: (el.innerText || el.placeholder || el.name || '').slice(0, 60).replace(/\\n/g, ' '),
                name: el.name || '',
                type: el.type || '',
                role: el.getAttribute('role') || '',
                className: el.className
            }));
        }''')
        with open("walk_step3_interactive.json", "w", encoding="utf-8") as f:
            json.dump(step3_interactive, f, ensure_ascii=False, indent=2)

        print("[STEP 3] Saved Step 3 details! Reviewing text...")
        for line in [l.strip() for l in step3_text.split("\n") if l.strip()][:30]:
            print("   |", line)

        await asyncio.sleep(5)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_complete_step2_and_beyond())
