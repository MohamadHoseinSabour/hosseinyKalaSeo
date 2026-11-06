import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def check():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome', headless=True)
        page = await b.new_page(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        print("Navigating to https://divar.ir/s/ahvaz/new...")
        await page.goto('https://divar.ir/s/ahvaz/new', wait_until='domcontentloaded', timeout=20000)
        await asyncio.sleep(2)
        print("Final URL:", page.url)
        elements = await page.query_selector_all('li, a, button, p')
        print(f"Total elements: {len(elements)}")
        for el in elements:
            text = (await el.inner_text()).strip()
            if any(k in text for k in ['لوازم خانگی', 'وسایل برقی', 'املاک', 'وسایل نقلیه', 'خدمات']):
                print("Category option:", text.replace('\n', ' -- '))
        await b.close()

if __name__ == "__main__":
    asyncio.run(check())
