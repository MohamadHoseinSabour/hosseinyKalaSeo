import asyncio
import os
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

SESSION_DIR = os.path.abspath("./divar_session")

async def inspect_authenticated_new():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            SESSION_DIR,
            channel="chrome",
            headless=True,
            viewport={"width": 1280, "height": 850},
            locale="fa-IR"
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()

        print("[1] Opening https://divar.ir/new as AUTHENTICATED user...")
        await page.goto("https://divar.ir/new", wait_until="domcontentloaded")
        await asyncio.sleep(4)
        print("URL:", page.url)

        await page.screenshot(path="auth_new_screen.png")
        content = await page.content()
        with open("auth_new_screen.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("Saved auth_new_screen.png and auth_new_screen.html (len: %d)" % len(content))

        # Check all visible texts
        elems = await page.query_selector_all('button, div, a, p, span, h1, h2, h3, label')
        print(f"Total elements: {len(elems)}")
        for el in elems:
            txt = (await el.inner_text()).strip()
            if any(k in txt for k in ['فروشگاه', 'خانه کلور', 'حسینی', 'شخصی', 'کسب', 'ثبت آگهی', 'انتخاب']):
                if len(txt) < 80:
                    print(f"  Match: [{txt}]")

        await ctx.close()

if __name__ == "__main__":
    asyncio.run(inspect_authenticated_new())
