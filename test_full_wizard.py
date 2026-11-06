import asyncio
import os
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

SESSION_DIR = os.path.abspath("./divar_session")
AD_FOLDER = os.path.abspath("./divar_ads/01_یخچال_دوقلو_کلور")
IMAGES_DIR = os.path.join(AD_FOLDER, "images")

async def test_full_wizard():
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

        # Wait for Title input to appear
        print("[2] Waiting for form to mount (waiting for input[name='Title'])...")
        title_inp = await page.wait_for_selector('input[name="Title"]', timeout=20000)
        print(">>> Form mounted! Found input[name='Title']!")

        # 1. Fill Title
        title = "یخچال فریزر دوقلو کلور در اهواز - اقساطی"
        await title_inp.fill(title)
        print(f"[STEP 1] Filled title: {title}")

        # 2. Upload images
        images = [os.path.join(IMAGES_DIR, f) for f in os.listdir(IMAGES_DIR) if f.lower().endswith(('.jpg', '.png'))][:3]
        print(f"[STEP 1] Setting {len(images)} images on input[name='Images']...")
        await page.set_input_files('input[name="Images"]', images)
        print("Images set! Waiting 4s for upload processing...")
        await asyncio.sleep(4)

        await page.screenshot(path="wizard_step1_ready.png")
        print("Saved wizard_step1_ready.png")

        # 3. Click "بعدی"
        print("[STEP 1] Looking for 'بعدی' button...")
        next_btn = await page.wait_for_selector('button.kt-button--primary:has-text("بعدی")', timeout=10000)
        print("Next button found. Clicking 'بعدی'...")
        await next_btn.click()
        
        # 4. Wait for Step 2
        print("\n[STEP 2] Waiting for next step...")
        await asyncio.sleep(4)
        print("Current URL:", page.url)
        await page.screenshot(path="wizard_step2.png")
        content = await page.content()
        with open("wizard_step2.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("Saved wizard_step2.png and wizard_step2.html (len: %d)" % len(content))

        await ctx.close()
        print("Test finished successfully!")

if __name__ == "__main__":
    asyncio.run(test_full_wizard())
