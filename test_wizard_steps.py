import asyncio
import os
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

SESSION_DIR = os.path.abspath("./divar_session")
AD_FOLDER = os.path.abspath("./divar_ads/01_یخچال_دوقلو_کلور")
IMAGES_DIR = os.path.join(AD_FOLDER, "images")

async def test_step1_to_step2():
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
        await asyncio.sleep(2)

        # Dismiss PWA modal if visible
        pwa_btn = await page.query_selector('button:has-text("متوجه شدم")')
        if pwa_btn and await pwa_btn.is_visible():
            print("[DISMISS] Clicking 'متوجه شدم'...")
            try:
                await pwa_btn.click(timeout=3000)
                await asyncio.sleep(1)
            except Exception:
                pass

        # 1. Fill Title
        title = "یخچال فریزر دوقلو کلور در اهواز - اقساطی"
        print(f"[STEP 1] Filling title: {title}")
        title_inp = await page.query_selector('input[name="Title"]')
        if title_inp:
            await title_inp.fill(title)
            print("Title filled!")
        else:
            print("ERROR: input[name='Title'] not found!")

        # 2. Upload 3 images
        images = [os.path.join(IMAGES_DIR, f) for f in os.listdir(IMAGES_DIR) if f.lower().endswith(('.jpg', '.png'))][:3]
        print(f"[STEP 1] Uploading {len(images)} images...")
        file_inp = await page.query_selector('input[name="Images"]')
        if file_inp:
            await file_inp.set_input_files(images)
            print("Images set!")
            await asyncio.sleep(4) # wait for upload preview
        else:
            print("ERROR: input[name='Images'] not found!")

        await page.screenshot(path="step1_completed.png")
        print("Saved step1_completed.png")

        # 3. Click "بعدی"
        next_btn = await page.query_selector('button:has-text("بعدی")')
        if next_btn:
            # Check if button is disabled
            is_disabled = await next_btn.is_disabled()
            print("Next button disabled?", is_disabled)
            if not is_disabled:
                print("Clicking 'بعدی'...")
                await next_btn.click()
                await asyncio.sleep(3)
                
                print("[STEP 2] URL:", page.url)
                await page.screenshot(path="step2_page.png")
                content = await page.content()
                with open("step2.html", "w", encoding="utf-8") as f:
                    f.write(content)
                print("Saved step2.html (len: %d)" % len(content))
            else:
                print("Next button is disabled! Waiting a moment...")
                await asyncio.sleep(3)
                is_disabled = await next_btn.is_disabled()
                print("Next button disabled after wait?", is_disabled)
        else:
            print("Next button not found!")

        await ctx.close()
        print("Done.")

if __name__ == "__main__":
    asyncio.run(test_step1_to_step2())
