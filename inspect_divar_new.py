import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def inspect_new():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome", headless=True)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        print("Navigating to https://divar.ir/new...")
        try:
            await page.goto("https://divar.ir/new", wait_until="domcontentloaded", timeout=30000)
            title = await page.title()
            print("Loaded! Title:", title)
            await asyncio.sleep(2)
            content = await page.content()
            print("Page content length:", len(content))
            with open("divar_new_page.html", "w", encoding="utf-8") as f:
                f.write(content)
            print("Saved divar_new_page.html")
        except Exception as e:
            print("Error:", e)
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect_new())

