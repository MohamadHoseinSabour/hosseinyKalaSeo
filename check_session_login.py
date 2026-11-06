import asyncio
import os
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def check_login():
    session_dir = os.path.abspath("./divar_session")
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=session_dir,
            channel="chrome",
            headless=True,
            locale="fa-IR"
        )
        page = context.pages[0] if context.pages else await context.new_page()
        print("Checking session...")
        await page.goto("https://divar.ir/my-divar/my-posts", wait_until="domcontentloaded", timeout=20000)
        await asyncio.sleep(2)
        url = page.url
        print("Final URL:", url)
        cookies = await context.cookies()
        token_cookies = [c['name'] for c in cookies]
        print("Cookies found:", len(cookies), token_cookies[:8])
        
        # Check if user is logged in
        is_logged_in = any('token' in c['name'].lower() or 'auth' in c['name'].lower() for c in cookies) or '/my-divar/my-posts' in url
        print("Is logged in:", is_logged_in)
        
        # Also check page content for phone number or store name
        content = await page.content()
        if 'حسینی' in content or 'خروج' in content or 'کیف پول' in content:
            print("Detected store or logout button -> USER IS LOGGED IN!")
            is_logged_in = True
        else:
            print("Did not detect store keywords in my-divar page")
            
        await context.close()
        return is_logged_in

if __name__ == "__main__":
    asyncio.run(check_login())
