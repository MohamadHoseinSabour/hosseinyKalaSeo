import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def inspect_category_flow():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome', headless=True)
        page = await b.new_page(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        print("Navigating to https://divar.ir/new...")
        await page.goto("https://divar.ir/new", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(2)
        
        # Check inputs on the page
        inputs = await page.query_selector_all('input')
        print(f"Total inputs on /new: {len(inputs)}")
        for inp in inputs:
            p_holder = await inp.get_attribute('placeholder')
            name = await inp.get_attribute('name')
            inp_type = await inp.get_attribute('type')
            print(f"Input: type={inp_type}, name={name}, placeholder={p_holder}")
            
        # Check category elements or clickable items
        items = await page.query_selector_all('button, a, div[role="button"]')
        print(f"Clickable items: {len(items)}")
        for it in items[:25]:
            text = (await it.inner_text()).strip().replace('\n', ' > ')
            if text:
                print(f" - [{text}]")
                
        await b.close()

if __name__ == "__main__":
    asyncio.run(inspect_category_flow())
