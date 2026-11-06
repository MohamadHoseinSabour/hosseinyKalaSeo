import asyncio
import os
from playwright.async_api import async_playwright

async def test_headed():
    user_data_dir = os.path.abspath("./divar_browser_session")
    os.makedirs(user_data_dir, exist_ok=True)
    
    print(f"Launching Chrome with profile at: {user_data_dir}")
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            channel="chrome",
            headless=False,
            viewport={"width": 1280, "height": 800},
            locale="fa-IR"
        )
        page = browser.pages[0] if browser.pages else await browser.new_page()
        print("Navigating to https://divar.ir...")
        await page.goto("https://divar.ir", timeout=20000)
        print("Page title:", await page.title())
        print("Waiting 5 seconds so user can see the window...")
        await asyncio.sleep(5)
        await browser.close()
        print("Browser test closed.")

if __name__ == "__main__":
    asyncio.run(test_headed())
