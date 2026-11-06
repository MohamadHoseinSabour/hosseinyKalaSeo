import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def check():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context('./divar_session', channel='chrome', headless=True)
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        await page.goto('https://divar.ir/my-divar', wait_until='domcontentloaded')
        await asyncio.sleep(2)
        
        login_btn = await page.query_selector('text="ورود به حساب کاربری"') or await page.query_selector('text="ورود"')
        print("Login button visible:", bool(login_btn))
        
        token = await page.evaluate('() => localStorage.getItem("token") || localStorage.getItem("auth_token") || ""')
        print("Token exists in localStorage:", bool(token))
        
        # Check if store exists
        store_elem = await page.query_selector('text="فروشگاه خانه کلور حسینی کالا"')
        print("Store element exists:", bool(store_elem))
        
        await ctx.close()

if __name__ == "__main__":
    asyncio.run(check())
