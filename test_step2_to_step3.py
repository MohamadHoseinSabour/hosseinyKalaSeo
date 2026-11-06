import asyncio
import os
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

SESSION_DIR = os.path.abspath("./divar_session")
AD_FOLDER = os.path.abspath("./divar_ads/01_یخچال_دوقلو_کلور")
IMAGES_DIR = os.path.join(AD_FOLDER, "images")

async def test_step2_to_step3():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            SESSION_DIR,
            channel="chrome",
            headless=True,
            viewport={"width": 1280, "height": 850},
            locale="fa-IR"
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()

        print("[1] Opening https://divar.ir/new...")
        await page.goto("https://divar.ir/new", wait_until="domcontentloaded")

        # Step 1: Title & Images
        title_inp = await page.wait_for_selector('input[name="Title"]', timeout=20000)
        await title_inp.fill("یخچال فریزر دوقلو کلور در اهواز - اقساطی")
        images = [os.path.join(IMAGES_DIR, f) for f in os.listdir(IMAGES_DIR) if f.lower().endswith(('.jpg', '.png'))][:3]
        await page.set_input_files('input[name="Images"]', images)
        await asyncio.sleep(4)
        next_btn = await page.wait_for_selector('button.kt-button--primary:has-text("بعدی")', timeout=10000)
        await next_btn.click()
        print("[STEP 1 -> STEP 2] Clicked Next!")
        await asyncio.sleep(3)

        # Step 2: Handle Condition and Price
        print("[STEP 2] Setting Condition to 'نو'...")
        # Check condition button
        cond_btn = await page.query_selector('div:has-text("وضعیت*") button, div:has-text("وضعیت") button')
        if cond_btn:
            await cond_btn.click()
            await asyncio.sleep(1)
            # Click "نو"
            new_opt = await page.query_selector('div[role="option"]:has-text("نو"), li:has-text("نو"), button:has-text("نو")')
            if new_opt:
                await new_opt.click()
                print("Selected 'نو'!")
                await asyncio.sleep(1)

        # Check Price
        # Let's see if price can be left empty for توافقی or set to a placeholder
        # Click "بعدی" to go to Step 3
        print("[STEP 2] Clicking 'بعدی'...")
        step2_next = await page.query_selector('button.kt-button--primary:has-text("بعدی")')
        if step2_next:
            await step2_next.click()
            await asyncio.sleep(3)
            
        print("[STEP 3] URL:", page.url)
        await page.screenshot(path="wizard_step3.png")
        content = await page.content()
        with open("wizard_step3.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("Saved wizard_step3.png and wizard_step3.html (len: %d)" % len(content))

        await ctx.close()

if __name__ == "__main__":
    asyncio.run(test_step2_to_step3())
