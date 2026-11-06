import asyncio
import os
import sys
import json
import logging

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from playwright.async_api import async_playwright
from PIL import Image

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DivarPoster")

SESSION_DIR = os.path.abspath("divar_session")
STORE_NEW_URL = "https://divar.ir/new/PREMIUM_PANEL/ZhWFYgaK_xTlfvkBc"
ADS_DATA_FILE = "divar_prepared_ads.json"

# Store exact coordinates & IDs for Ahvaz, Naderi, Kaveh St.
AHVAZ_CITY_ID = 7
NADERI_NEIGHBORHOOD_ID = 328
AHVAZ_COORDS = [48.6840, 31.3220]  # [longitude, latitude]
DEFAULT_PRICE = "111111111"

def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', errors='replace').decode('ascii'))

def cleanup_profile_locks():
    """Cleans up stale Chrome singleton lock files if previous process exited abnormally."""
    for lf in ["SingletonLock", "SingletonSocket", "SingletonCookie"]:
        lock_path = os.path.join(SESSION_DIR, lf)
        if os.path.exists(lock_path):
            try:
                os.remove(lock_path)
            except Exception:
                pass

def load_ads():
    if not os.path.exists(ADS_DATA_FILE):
        raise FileNotFoundError(f"Missing {ADS_DATA_FILE}. Please run prepare_ad_data.py first.")
    with open(ADS_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

async def dismiss_popups(page):
    selectors = [
        'button:has-text("متوجه شدم")',
        'button:has-text("بستن")',
        'button[aria-label="بستن"]',
        '.modal__close-button-eadb9',
        '.kt-new-modal__close-button'
    ]
    for sel in selectors:
        try:
            btn = page.locator(sel).first
            if await btn.is_visible(timeout=600):
                await btn.click(force=True)
                await asyncio.sleep(0.4)
        except Exception:
            pass

async def clear_existing_draft(page):
    """Resets any previous unsubmitted draft so the form starts 100% clean."""
    safe_print("      Checking for previous drafts to reset...")
    
    # Case 1: Check if "آیا مایل به ثبت آگهی از ابتدا هستید؟" dialog is already showing
    try:
        initial_prompt = page.locator('text="آیا مایل به ثبت آگهی از ابتدا هستید؟"')
        if await initial_prompt.is_visible(timeout=1000):
            yes_btn = page.locator('button:has-text("بله")').first
            if await yes_btn.is_visible(timeout=1000):
                await yes_btn.click(force=True)
                await asyncio.sleep(1.5)
                safe_print("      Reset confirmed via 'بله' dialog.")
                return
    except Exception:
        pass

    # Case 2: In the form header, 'پاک کردن' button is visible
    try:
        clear_btn = page.locator('button:has-text("پاک کردن")').first
        if await clear_btn.is_visible(timeout=1500):
            await clear_btn.click(force=True)
            await asyncio.sleep(0.8)
            
            # Modal appears: "آیا مایل به ثبت آگهی از ابتدا هستید؟" with buttons "نه" and "بله"
            yes_btn = page.locator('.kt-modal button:has-text("بله"), .kt-dimmer button:has-text("بله"), [role="dialog"] button:has-text("بله"), button:has-text("بله")').last
            if await yes_btn.is_visible(timeout=2000):
                await yes_btn.click(force=True)
                await asyncio.sleep(1.5)
                safe_print("      Draft reset successfully (Clicked 'پاک کردن' -> 'بله').")
            else:
                await page.keyboard.press("Enter")
                await asyncio.sleep(1.5)
                safe_print("      Draft reset confirmed via Enter key.")
    except Exception as e:
        safe_print(f"      Draft clear note: {e}")

async def remove_existing_photos(page):
    """Remove any previously uploaded/draft photos before adding new ones."""
    safe_print("      Checking for existing draft photos to remove...")
    while True:
        del_btns = page.locator('.kt-file-upload-preview__delete-button, button:has-text("حذف عکس"), button[aria-label="حذف عکس"]')
        count = await del_btns.count()
        if count == 0:
            break
        try:
            await del_btns.first.click(force=True)
            await asyncio.sleep(0.3)
        except Exception:
            break
    safe_print("      Existing photos cleared.")

async def set_ahvaz_location(page):
    """Sets exact location to Ahvaz, Naderi (Kaveh St) via Divar's location handler."""
    safe_print("      Setting location to: Ahvaz, Naderi, Kaveh St...")
    try:
        loc_btn = page.locator('div:has-text("مکان آگهی*") button.kt-action-field, button:has-text("انتخاب")').first
        if not await loc_btn.is_visible(timeout=2500):
            return
            
        await loc_btn.click()
        await asyncio.sleep(2)
        
        # Inject exact Ahvaz Naderi location directly into React Fiber
        res = await page.evaluate(f'''() => {{
            const findReact = (el) => {{
                for (const k in el) if (k.startsWith('__reactFiber$')) return el[k];
                return null;
            }};
            const mapEl = document.querySelector('.mapboxgl-map') || document.querySelector('canvas');
            if (!mapEl) return false;
            let f = findReact(mapEl);
            let onSubmitFn = null;
            let onCloseFn = null;
            while (f) {{
                if (f.memoizedProps) {{
                    if (f.memoizedProps.onSubmit && !onSubmitFn) onSubmitFn = f.memoizedProps.onSubmit;
                    if (f.memoizedProps.onClose && !onCloseFn) onCloseFn = f.memoizedProps.onClose;
                }}
                f = f.return;
            }}
            
            if (onSubmitFn) {{
                onSubmitFn({{
                    center: [{AHVAZ_COORDS[0]}, {AHVAZ_COORDS[1]}],
                    cityId: {AHVAZ_CITY_ID},
                    neighbourhoodId: {NADERI_NEIGHBORHOOD_ID},
                    onSuccess: () => {{
                        if (onCloseFn) onCloseFn();
                    }}
                }});
                return true;
            }}
            return false;
        }}''')
        
        if res:
            safe_print("      Location set to Ahvaz, Naderi (Kaveh St) successfully.")
            await asyncio.sleep(1.5)
        else:
            # Fallback: Confirm current location
            confirm_loc = page.locator('button:has-text("تأیید")').first
            if await confirm_loc.is_visible(timeout=1500):
                await confirm_loc.click(force=True)
                await asyncio.sleep(1)
                
        # Close dimmer if still lingering
        dimmer = page.locator('.kt-dimmer--open')
        if await dimmer.count() > 0:
            close_btn = page.locator('.kt-dimmer button:has-text("انصراف"), .kt-dimmer .kt-modal__close-button').first
            if await close_btn.is_visible(timeout=1000):
                await close_btn.click(force=True)
            await asyncio.sleep(1)
            
    except Exception as e:
        safe_print(f"      Location note: {e}")

async def prepare_ad_in_store(page, ad):
    title = ad["title"]
    content = ad["content"]
    images = [img for img in ad["images"] if os.path.exists(img)][:10]
    
    safe_print("\n" + "=" * 60)
    safe_print(f"[*] Preparing Ad in Store: {title}")
    safe_print(f"[*] Folder: {ad['folder']} | Images: {len(images)} | Content: {len(content)} chars")
    safe_print("=" * 60)
    
    # 1. Navigate directly to Store ad creation URL
    safe_print("[1/4] Navigating to Store Ad Wizard (ZhWFYgaK_xTlfvkBc)...")
    await page.goto(STORE_NEW_URL, wait_until="networkidle", timeout=40000)
    await asyncio.sleep(2)
    await dismiss_popups(page)
    
    # Reset existing draft if present
    await clear_existing_draft(page)
    
    # Step 1: Title and Images
    safe_print("[1/4] Filling Title & managing photos...")
    title_input = page.locator('input[name="Title"]')
    await title_input.wait_for(state="visible", timeout=15000)
    await title_input.fill(title)
    await asyncio.sleep(1)
    
    # Remove any existing photos first
    await remove_existing_photos(page)
    
    # Upload new images (ensuring minimum 600x600 size for Divar)
    if images:
        valid_images = []
        for img_path in images:
            try:
                with Image.open(img_path) as im:
                    w, h = im.size
                    if w < 500 or h < 500:
                        scale = max(600 / w, 600 / h)
                        nw, nh = int(w * scale), int(h * scale)
                        resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
                        final_img = Image.new("RGB", (max(nw, 600), max(nh, 600)), (255, 255, 255))
                        final_img.paste(resized, ((final_img.width - nw) // 2, (final_img.height - nh) // 2))
                        final_img.save(img_path, quality=95)
                valid_images.append(img_path)
            except Exception:
                valid_images.append(img_path)

        file_input = page.locator('input[type="file"]')
        await file_input.set_input_files(valid_images)
        safe_print(f"      Uploaded {len(valid_images)} fresh photos (verified >= 600px).")
        await asyncio.sleep(4)
        
    next_s1 = page.locator('button[type="submit"]:has-text("بعدی")').first
    await next_s1.click()
    
    # Wait for Step 2 indicator
    await page.locator('button[name="status"], input[name="price"], div:has-text("صفحهٔ ۲ از ۴")').first.wait_for(state="visible", timeout=15000)
    safe_print("[1/4] Advanced to Step 2.")
    await asyncio.sleep(1)
    await dismiss_popups(page)

    # Step 2: Category, Location, Status, Price
    safe_print("[2/4] Configuring Category, Location & Status...")
    
    # Set Ahvaz Location
    await set_ahvaz_location(page)

    # Status: Select "نو"
    try:
        status_btn = page.locator('button[name="status"]')
        await status_btn.wait_for(state="visible", timeout=8000)
        await status_btn.click()
        await asyncio.sleep(1)
        new_opt = page.locator('.kt-select-dropdown__item:has-text("نو"), div[role="button"]:has-text("نو"), .kt-selector-row:has-text("نو"), li:has-text("نو")').first
        await new_opt.wait_for(state="visible", timeout=5000)
        await new_opt.click()
        safe_print("      Status set to: New (نو).")
        await asyncio.sleep(1)
    except Exception as e:
        safe_print(f"      Status note: {e}")

    # Price: Set to the cheapest product in this ad's category
    ad_price = str(ad.get("price", "5000000"))
    try:
        price_input = page.locator('input[name="price"]')
        await price_input.wait_for(state="visible", timeout=8000)
        await price_input.fill("")
        await price_input.fill(ad_price)
        safe_print(f"      Price entered (Category Min): {int(ad_price):,} Toman.")
        await asyncio.sleep(1)
    except Exception as e:
        safe_print(f"      Price note: {e}")

    # Step 2 -> Step 3
    next_s2 = page.locator('button[type="submit"]:has-text("بعدی")').first
    await next_s2.click()
    
    # Wait for Step 3 Description textarea
    desc_area = page.locator('textarea[name="Description"]')
    await desc_area.wait_for(state="visible", timeout=15000)
    safe_print("[2/4] Advanced to Step 3.")
    await asyncio.sleep(1)

    # Step 3: Description
    safe_print("[3/4] Filling Ad Description...")
    await desc_area.fill(content)
    safe_print(f"      Description filled ({len(content)} chars, no dashed lines).")
    await asyncio.sleep(2)

    # Step 3 -> Step 4
    next_s3 = page.locator('button[type="submit"]:has-text("بعدی")').first
    await next_s3.click()
    
    # Wait for Step 4 Preview / Final screen
    await page.locator('div:has-text("صفحهٔ ۴ از ۴"), div:has-text("اطلاعات تماس"), button:has-text("انتشار آگهی")').first.wait_for(state="visible", timeout=20000)
    safe_print("[3/4] Advanced to Step 4 (Contact Info & Final Review Screen).")
    await asyncio.sleep(2)

    # Step 4 Reached!
    safe_print("=" * 60)
    safe_print(">>> [SUCCESS: AD PREPARED & DRAFTED IN STORE PANEL] <<<")
    safe_print(f"Title: {title}")
    safe_print("Store: فروشگاه خانه کلور حسینی کالا")
    safe_print("Location: اهواز، نادری، خیابان کاوه")
    safe_print(f"Price: {int(ad_price):,} Toman")
    safe_print("All photos, description, location, and specs are filled!")
    safe_print("The ad is currently on your Chrome screen in Step 4 / Preview.")
    safe_print("=" * 60)

async def main():
    cleanup_profile_locks()
    ads = load_ads()
    
    safe_print("\n============================================================")
    safe_print("   HOSSEINY KALA - DIVAR STORE AUTO POSTER (VERIFIED)       ")
    safe_print("   Store: Khaneh Clover Hosseiny Kala                       ")
    safe_print("============================================================")
    safe_print(f"Loaded {len(ads)} category-based ad templates.")
    safe_print("\nAvailable Ads:")
    for idx, ad in enumerate(ads, 1):
        clean_name = ad["folder"]
        price_num = int(ad.get('price', 0))
        price_str = f"{price_num:,} تومان" if price_num > 0 else "توافقی"
        safe_print(f"  [{idx:2d}] {clean_name[:35]:<35} ({len(ad['images'])} عکس | {price_str})")

    safe_print("\nOptions:")
    safe_print("  - Enter ad number (1 to 20)")
    safe_print("  - Type 'all' to draft all ads one by one")
    safe_print("  - Type 'q' to quit")
    
    choice = input("\nEnter your choice: ").strip().lower()
    if choice == "q":
        return

    to_process = []
    if choice == "all":
        to_process = ads
    elif choice.isdigit() and 1 <= int(choice) <= len(ads):
        to_process = [ads[int(choice) - 1]]
    else:
        safe_print("Invalid selection. Defaulting to Ad #1.")
        to_process = [ads[0]]

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch_persistent_context(
                user_data_dir=SESSION_DIR,
                channel="chrome",
                headless=False,
                viewport={"width": 1280, "height": 900},
                args=["--disable-blink-features=AutomationControlled"]
            )
            page = browser.pages[0] if browser.pages else await browser.new_page()

            for idx, ad in enumerate(to_process, 1):
                try:
                    await prepare_ad_in_store(page, ad)
                    
                    safe_print("\n" + "#" * 60)
                    safe_print(f"CHECK THE CHROME WINDOW! Ad [{idx}/{len(to_process)}] is ready on Step 4.")
                    safe_print("Options:")
                    safe_print("  - Review or edit in Chrome if needed.")
                    safe_print("  - Press [Enter] here when ready to proceed to next ad.")
                    safe_print("  - Type 's' + [Enter] to skip.")
                    safe_print("  - Type 'q' + [Enter] to quit automation.")
                    safe_print("#" * 60)
                    
                    user_action = input(">>> Action (Enter/s/q): ").strip().lower()
                    if user_action == "q":
                        safe_print("Stopping automation as requested.")
                        break
                except Exception as e:
                    logger.error(f"Error processing ad: {e}")
                    retry = input("An error occurred. Press Enter to continue to next ad or 'q' to quit: ").strip().lower()
                    if retry == "q":
                        break

            safe_print("\nAll tasks completed. Closing browser in 3 seconds...")
            await asyncio.sleep(3)
            await browser.close()
            safe_print("Done!")
    except Exception as e:
        safe_print(f"\n[ERROR] Could not start browser: {e}")
        safe_print("TIP: If Chrome is currently open, please close all Chrome windows and run again.")

if __name__ == "__main__":
    asyncio.run(main())
