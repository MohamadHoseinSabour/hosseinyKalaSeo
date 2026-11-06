import sys
import asyncio
from playwright.async_api import async_playwright
import json

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome", headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        api_calls = []

        async def handle_response(response):
            if "api.divar.ir" in response.url or "/v8/" in response.url or "post" in response.url:
                try:
                    if "json" in response.headers.get("content-type", ""):
                        data = await response.json()
                        api_calls.append({"url": response.url, "data": data})
                        print(f"Captured API: {response.url[:80]}...")
                except Exception:
                    pass

        page.on("response", handle_response)

        print("Navigating to https://divar.ir/pro/xTlfvkBc...")
        await page.goto("https://divar.ir/pro/xTlfvkBc", wait_until="networkidle", timeout=30000)

        # Scroll down multiple times to load all 45 items
        for i in range(15):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(1.5)
            # check number of cards
            cards = await page.query_selector_all('article, a[href*="/v/"]')
            print(f"Scroll {i+1}: {len(cards)} items found")
            if len(cards) >= 45:
                print("All 45+ items reached!")
                break

        # Extract all posts
        post_elements = await page.query_selector_all('a[href*="/v/"]')
        posts = []
        for el in post_elements:
            href = await el.get_attribute('href')
            text = await el.inner_text()
            lines = [l.strip() for l in text.split('\n') if l.strip()]
            title = lines[0] if len(lines) > 0 else ""
            price = lines[1] if len(lines) > 1 else ""
            extra = " | ".join(lines[2:]) if len(lines) > 2 else ""
            posts.append({
                "title": title,
                "price": price,
                "extra": extra,
                "href": href,
                "full_text": text
            })

        print(f"Total extracted posts: {len(posts)}")
        with open("divar_all_posts.json", "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)

        with open("divar_api_calls.json", "w", encoding="utf-8") as f:
            json.dump(api_calls, f, ensure_ascii=False, indent=2)

        await browser.close()
        print("Done!")

if __name__ == "__main__":
    asyncio.run(main())
