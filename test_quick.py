import asyncio
import os
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        b = await p.chromium.launch_persistent_context(
            'divar_session', 
            channel='chrome', 
            headless=False, 
            viewport={'width': 1280, 'height': 900}
        )
        page = b.pages[0] if b.pages else await b.new_page()
        print('Navigating to store new ad...', flush=True)
        await page.goto('https://divar.ir/new/PREMIUM_PANEL/ZhWFYgaK_xTlfvkBc', wait_until='networkidle')
        await asyncio.sleep(2)
        print('Current URL:', page.url, flush=True)
        print('Page title:', await page.title(), flush=True)
        
        btn = page.locator('button:has-text("پاک کردن")')
        count = await btn.count()
        print('Clear button count:', count, flush=True)
        
        title_in = page.locator('input[name="Title"]')
        print('Title input visible:', await title_in.is_visible(), flush=True)
        await page.screenshot(path='current_screen.png')
        print('Screenshot saved: current_screen.png', flush=True)
        await b.close()

if __name__ == '__main__':
    asyncio.run(check())
