import asyncio
import os
import json
from playwright.async_api import async_playwright

STORE_NEW_URL = "https://divar.ir/new/PREMIUM_PANEL/ZhWFYgaK_xTlfvkBc"

async def test_confirm_fiber():
    async with async_playwright() as p:
        b = await p.chromium.launch_persistent_context('divar_session', channel='chrome', headless=False)
        page = b.pages[0] if b.pages else await b.new_page()
        await page.goto(STORE_NEW_URL, wait_until='networkidle')
        await asyncio.sleep(2)
        await page.locator('input[name="Title"]').fill('یخچال فریزر دوقلو کلور در اهواز - اقساط')
        img = os.path.abspath(r'divar_ads\01_یخچال_دوقلو_کلور\images\clover-economy-27ft-twin-refrigerator.jpg')
        await page.locator('input[type="file"]').set_input_files(img)
        await asyncio.sleep(2)
        await page.locator('button[type="submit"]:has-text("بعدی")').click()
        await asyncio.sleep(3)
        await page.locator('div:has-text("مکان آگهی*") button.kt-action-field, button:has-text("انتخاب")').first.click()
        await asyncio.sleep(2)

        info = await page.evaluate('''() => {
            const findReact = (el) => {
                for (const k in el) if (k.startsWith('__reactFiber$')) return el[k];
                return null;
            };
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('تأیید'));
            if (!btn) return { btnFound: false };
            
            const f = findReact(btn);
            let cur = f;
            const res = [];
            while (cur) {
                if (cur.memoizedProps) {
                    const keys = Object.keys(cur.memoizedProps);
                    for (const k of keys) {
                        if (k === 'onClick' || k === 'onSubmit' || k === 'onConfirm' || k === 'location' || k.toLowerCase().includes('point')) {
                            res.push({ key: k, type: typeof cur.memoizedProps[k], val: typeof cur.memoizedProps[k] !== 'function' ? cur.memoizedProps[k] : 'func' });
                        }
                    }
                }
                cur = cur.return;
            }
            return { btnFound: true, props: res };
        }''')
        
        print("[DEBUG] Confirm button fiber:", json.dumps(info, ensure_ascii=False, indent=2))
        await b.close()

if __name__ == '__main__':
    asyncio.run(test_confirm_fiber())
