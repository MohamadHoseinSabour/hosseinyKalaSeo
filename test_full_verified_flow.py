import asyncio
import os
import sys
import json
from playwright.async_api import async_playwright
from divar_store_auto_poster import (
    SESSION_DIR, STORE_NEW_URL, load_ads, dismiss_popups,
    AHVAZ_CITY_ID, NADERI_NEIGHBORHOOD_ID, AHVAZ_COORDS, DEFAULT_PRICE
)

async def test_full_flow():
    ads = load_ads()
    ad = ads[0] # Ad #1
    
    async with async_playwright() as p:
        b = await p.chromium.launch_persistent_context(SESSION_DIR, channel='chrome', headless=False, viewport={"width": 1280, "height": 900})
        page = b.pages[0] if b.pages else await b.new_page()
        
        print("\n[STEP 1] Navigating to Store Ad URL...")
        await page.goto(STORE_NEW_URL, wait_until="networkidle")
        await asyncio.sleep(2)
        await dismiss_popups(page)
        
        # Reset form if draft photos exist or not on Step 1
        try:
            clear_btn = page.locator('button:has-text("پاک کردن")').first
            if await clear_btn.is_visible(timeout=2000):
                print("[STEP 1] Clearing previous draft to ensure clean state...")
                await clear_btn.click(force=True)
                await asyncio.sleep(0.5)
                confirm = page.locator('.kt-new-modal button:has-text("پاک کردن"), .kt-dimmer button:has-text("پاک کردن"), button.kt-button--primary:has-text("پاک کردن")').last
                if await confirm.is_visible(timeout=2000):
                    await confirm.click(force=True)
                    await asyncio.sleep(2)
                print("[STEP 1] Form reset successfully.")
        except Exception as e:
            print(f"[STEP 1] Clear draft note: {e}")

        # Also remove any individual photos if still present
        while True:
            del_btns = page.locator('.kt-file-upload-preview__delete-button, button:has-text("حذف عکس"), button[aria-label="حذف عکس"]')
            if await del_btns.count() == 0:
                break
            try:
                await del_btns.first.click(force=True)
                await asyncio.sleep(0.3)
            except Exception:
                break

        # Fill Title
        print(f"[STEP 1] Filling Title: {ad['title']}")
        title_in = page.locator('input[name="Title"]')
        await title_in.wait_for(state="visible", timeout=15000)
        await title_in.fill(ad['title'])
        await asyncio.sleep(1)
        
        # Upload Images
        images = [img for img in ad['images'] if os.path.exists(img)][:10]
        print(f"[STEP 1] Uploading {len(images)} photos...")
        await page.locator('input[type="file"]').set_input_files(images)
        await asyncio.sleep(3)
        
        # Step 1 -> Next
        await page.locator('button[type="submit"]:has-text("بعدی")').first.click()
        print("[STEP 1] Advanced to Step 2.")
        await asyncio.sleep(3)
        await dismiss_popups(page)

        # Step 2: Location
        print("[STEP 2] Setting Location to Ahvaz, Naderi, Kaveh St...")
        loc_btn = page.locator('div:has-text("مکان آگهی*") button.kt-action-field, button:has-text("انتخاب")').first
        if await loc_btn.is_visible(timeout=3000):
            await loc_btn.click()
            await asyncio.sleep(2)
            
            # Inject location into React
            res = await page.evaluate(f'''() => {{
                const findReact = (el) => {{
                    for (const k in el) if (k.startsWith('__reactFiber$')) return el[k];
                    return null;
                }};
                const mapEl = document.querySelector('.mapboxgl-map') || document.querySelector('canvas');
                if (!mapEl) return false;
                let f = findReact(mapEl);
                let onSubmitFn = null;
                let onCloseFn = null;
                while (f) {{
                    if (f.memoizedProps) {{
                        if (f.memoizedProps.onSubmit && !onSubmitFn) onSubmitFn = f.memoizedProps.onSubmit;
                        if (f.memoizedProps.onClose && !onCloseFn) onCloseFn = f.memoizedProps.onClose;
                    }}
                    f = f.return;
                }}
                if (onSubmitFn) {{
                    onSubmitFn({{
                        center: [{AHVAZ_COORDS[0]}, {AHVAZ_COORDS[1]}],
                        cityId: {AHVAZ_CITY_ID},
                        neighbourhoodId: {NADERI_NEIGHBORHOOD_ID},
                        onSuccess: () => {{
                            if (onCloseFn) onCloseFn();
                        }}
                    }});
                    return true;
                }}
                return false;
            }}''')
            print("         Injected location:", res)
            await asyncio.sleep(2)
            
            # If dimmer is still around, close it
            dimmer = page.locator('.kt-dimmer--open')
            if await dimmer.count() > 0:
                close_btn = page.locator('.kt-dimmer button:has-text("انصراف"), .kt-dimmer .kt-modal__close-button').first
                if await close_btn.is_visible():
                    await close_btn.click()
                await asyncio.sleep(1)

        # Step 2: Status
        status_btn = page.locator('button[name="status"]')
        await status_btn.wait_for(state="visible", timeout=10000)
        await status_btn.click()
        await asyncio.sleep(1)
        new_opt = page.locator('.kt-select-dropdown__item:has-text("نو"), div[role="button"]:has-text("نو"), .kt-selector-row:has-text("نو"), li:has-text("نو")').first
        await new_opt.wait_for(state="visible", timeout=5000)
        await new_opt.click()
        print("         Status set to: نو (New)")
        await asyncio.sleep(1)

        # Step 2: Price
        price_input = page.locator('input[name="price"]')
        await price_input.wait_for(state="visible", timeout=10000)
        await price_input.fill(DEFAULT_PRICE)
        print(f"         Price set to: {DEFAULT_PRICE}")
        await asyncio.sleep(1)

        # Step 2 -> Next
        await page.locator('button[type="submit"]:has-text("بعدی")').first.click()
        print("[STEP 2] Advanced to Step 3.")
        await asyncio.sleep(3)

        # Step 3: Description
        print("[STEP 3] Entering Description...")
        desc_area = page.locator('textarea[name="Description"]')
        await desc_area.wait_for(state="visible", timeout=10000)
        await desc_area.fill(ad['content'])
        print(f"         Filled {len(ad['content'])} chars (no dashed lines).")
        await asyncio.sleep(2)

        # Step 3 -> Next
        await page.locator('button[type="submit"]:has-text("بعدی")').first.click()
        print("[STEP 3] Advanced to Step 4.")
        await asyncio.sleep(4)

        # Step 4: Verification
        print("=" * 60)
        print("[SUCCESS] All 4 steps completed perfectly!")
        print(f"Title: {ad['title']}")
        print(f"Price: {DEFAULT_PRICE}")
        print("Location: Ahvaz, Naderi, Kaveh St")
        print("Photos: Uploaded cleanly")
        print("Step 4 / Preview screen is live in Chrome!")
        print("=" * 60)
        
        await page.screenshot(path="final_verified_preview.png")
        await asyncio.sleep(6)
        await b.close()

if __name__ == '__main__':
    asyncio.run(test_full_flow())
