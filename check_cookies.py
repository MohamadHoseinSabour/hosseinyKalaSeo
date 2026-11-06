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
        cookies = await ctx.cookies()
        print('Total cookies in divar_session:', len(cookies))
        for c in cookies:
            print(f"  Cookie: {c['name']} = {c['value'][:25]}...")
        
        # Check localStorage
        ls = await page.evaluate('() => JSON.stringify(window.localStorage)')
        print("\nLocalStorage keys:", list(eval(ls).keys()) if ls else "Empty")
        if ls and ('token' in ls.lower() or 'auth' in ls.lower() or 'user' in ls.lower()):
            print("Found auth in localStorage!")
            
        await ctx.close()

if __name__ == "__main__":
    asyncio.run(check())
