import asyncio
from playwright.async_api import async_playwright
from divar_store_auto_poster import SESSION_DIR, STORE_NEW_URL

async def test_reset():
    async with async_playwright() as p:
        b = await p.chromium.launch_persistent_context(SESSION_DIR, channel='chrome', headless=False)
        page = b.pages[0] if b.pages else await b.new_page()
        await page.goto(STORE_NEW_URL, wait_until='networkidle')
        await asyncio.sleep(2)
        
        print("[RESET] Current URL:", page.url)
        body = await page.locator("body").inner_text()
        print("[RESET] Body lines:", [l.strip() for l in body.split('\n') if l.strip()][:10])
        
        # Check "پاک کردن" button
        clear_btn = page.locator('button:has-text("پاک کردن")').first
        if await clear_btn.is_visible():
            print("[RESET] Found 'پاک کردن' button! Clicking it...")
            await clear_btn.click()
            await asyncio.sleep(1)
            # Check if confirmation modal appears
            confirm_clear = page.locator('button:has-text("پاک کردن"), button:has-text("حذف"), button:has-text("بله")').last
            if await confirm_clear.is_visible():
                print("[RESET] Confirming clear in modal...")
                await confirm_clear.click()
                await asyncio.sleep(2)
            print("[RESET] Form reset to Step 1!")
            await page.screenshot(path="after_clear.png")
            body_after = await page.locator("body").inner_text()
            print("[RESET] After clear body:", [l.strip() for l in body_after.split('\n') if l.strip()][:10])
            
        await b.close()

if __name__ == '__main__':
    asyncio.run(test_reset())
