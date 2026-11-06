import asyncio
import os
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

SESSION_DIR = os.path.abspath("./divar_session")

async def diagnose():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            channel="chrome",
            headless=True,
            viewport={"width": 1280, "height": 850},
            locale="fa-IR"
        )
        page = context.pages[0] if context.pages else await context.new_page()

        print("[1] Going to https://divar.ir/my-divar...")
        await page.goto("https://divar.ir/my-divar", wait_until="domcontentloaded")
        await asyncio.sleep(2)
        print("URL:", page.url)
        await page.screenshot(path="step1_my_divar.png")

        # Click on store name
        store_elem = await page.query_selector('text="فروشگاه خانه کلور حسینی کالا"')
        if not store_elem:
            store_elem = await page.query_selector('text="خانه کلور"')
            
        if store_elem:
            print("[2] Clicking store...")
            await store_elem.click()
            await asyncio.sleep(3)
            print("URL after store click:", page.url)
            await page.screenshot(path="step2_store_panel.png")
            
            # Find all buttons or links on this store page
            elems = await page.query_selector_all('button, a')
            print(f"[3] Found {len(elems)} buttons/links in store panel:")
            for el in elems[:20]:
                txt = (await el.inner_text()).strip()
                href = await el.get_attribute('href')
                if txt:
                    print(f" - [{txt}] -> href: {href}")

            # Look for "ثبت آگهی"
            post_btn = await page.query_selector('button:has-text("ثبت آگهی"), a:has-text("ثبت آگهی")')
            if post_btn:
                print("[4] Clicking 'ثبت آگهی'...")
                # Listen for new page/tab
                async with context.expect_page(timeout=5000) as new_page_info:
                    await post_btn.click()
                    
                new_page = None
                try:
                    new_page = await new_page_info.value
                    print("[5] A NEW TAB WAS OPENED!")
                except Exception:
                    print("[5] No new tab, stay on current page or popup.")
                    
                target_page = new_page if new_page else page
                await asyncio.sleep(3)
                print("Target page URL:", target_page.url)
                await target_page.screenshot(path="step3_after_new_post.png")
                
                # Check target page content
                content = await target_page.content()
                print("Target page HTML length:", len(content))
                
                inputs = await target_page.query_selector_all('input')
                textareas = await target_page.query_selector_all('textarea')
                buttons = await target_page.query_selector_all('button')
                print(f"Inputs: {len(inputs)}, Textareas: {len(textareas)}, Buttons: {len(buttons)}")
                for inp in inputs:
                    p_h = await inp.get_attribute('placeholder')
                    name = await inp.get_attribute('name')
                    typ = await inp.get_attribute('type')
                    print(f"  Input: typ={typ}, name={name}, ph={p_h}")
                for b in buttons[:10]:
                    print(f"  Button: {(await b.inner_text()).strip()[:40]}")
            else:
                print("[4] 'ثبت آگهی' button not found in store panel!")
        else:
            print("[2] Store element not found on my-divar!")
            
        await context.close()
        print("Done diagnosing.")

if __name__ == "__main__":
    asyncio.run(diagnose())
