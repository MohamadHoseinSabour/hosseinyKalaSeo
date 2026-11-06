#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
دستیار نیمه‌خودکار ثبت آگهی‌های دسته‌ای در دیوار (فروشگاه حسینی کالا)
این برنامه مرورگر کروم را با پروفایل اختصاصی شما باز می‌کند تا سشن ورود ذخیره بماند.
برای هر آگهی، پوشه تصاویر باز شده، متن آماده کپی شده و تا مرحله پیش‌نمایش در مرورگر پیش می‌رود.
"""

import os
import sys
import json
import asyncio
import subprocess
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ADS_DIR = os.path.join(BASE_DIR, "divar_ads")
SESSION_DIR = os.path.join(BASE_DIR, "divar_session")
PROGRESS_FILE = os.path.join(BASE_DIR, "divar_posting_progress.json")

def copy_to_clipboard(text):
    """کپی متن در کلیپ‌بورد ویندوز"""
    try:
        p = subprocess.Popen(['clip.exe'], stdin=subprocess.PIPE)
        p.communicate(text.encode('utf-16'))
        return True
    except Exception as e:
        print(f"خطا در کپی کلیپ‌بورد: {e}")
        return False

def open_folder_in_explorer(path):
    """باز کردن پوشه تصاویر در اکسپلورر ویندوز برای Drag and Drop آسان عکس‌ها"""
    try:
        os.startfile(path)
    except Exception:
        subprocess.Popen(['explorer', path])

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_progress(progress):
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def get_ads_list():
    if not os.path.exists(ADS_DIR):
        print("پوشه divar_ads یافت نشد!")
        return []
    folders = [f for f in sorted(os.listdir(ADS_DIR)) if os.path.isdir(os.path.join(ADS_DIR, f))]
    ads = []
    for f in folders:
        fpath = os.path.join(ADS_DIR, f)
        txt_path = os.path.join(fpath, "ad_content.txt")
        images_dir = os.path.join(fpath, "images")
        title = f
        content = ""
        if os.path.exists(txt_path):
            with open(txt_path, 'r', encoding='utf-8') as tf:
                content = tf.read()
                # extract title
                for line in content.splitlines():
                    if "عنوان آگهی دیوار" in line:
                        continue
                    if line.strip() and not line.startswith("═") and not line.startswith("【") and not line.startswith("📌"):
                        title = line.strip()
                        break
        images = []
        if os.path.exists(images_dir):
            images = [os.path.join(images_dir, img) for img in os.listdir(images_dir) if img.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        
        ads.append({
            "folder": f,
            "folder_path": fpath,
            "title": title,
            "images_dir": images_dir,
            "images": images,
            "content": content
        })
    return ads

async def run_semi_poster():
    os.makedirs(SESSION_DIR, exist_ok=True)
    ads = get_ads_list()
    progress = load_progress()
    
    print("\n" + "="*70)
    print("      🚀 دستیار نیمه‌خودکار ثبت آگهی‌های دیوار (فروشگاه حسینی کالا)      ")
    print("="*70)
    print(f"تعداد ۲۰ آگهی دسته‌ای آماده در پوشه divar_ads شناسایی شد.")
    print("این اسکریپت کروم را باز می‌کند تا بدون انتشار خودکار، آگهی‌ها را تا پیش‌نمایش آماده کنید.\n")

    async with async_playwright() as p:
        print("در حال راه‌اندازی مرورگر کروم با سشن اختصاصی...")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            channel="chrome",
            headless=False,
            viewport={"width": 1280, "height": 850},
            locale="fa-IR",
            args=["--start-maximized"]
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        # 1. Check Login
        print("\nدر حال باز کردن دیوار جهت بررسی وضعیت لاگین...")
        await page.goto("https://divar.ir/s/ahvaz", wait_until="domcontentloaded")
        await asyncio.sleep(2)
        
        print("\n" + "-"*70)
        print("🔑 بررسی وضعیت ورود:")
        print("اگر قبلاً وارد نشده‌اید، لطفاً در پنجره کروم روی 'دیوار من' یا 'ورود' کلیک کنید")
        print("و با شماره موبایل فروشگاه لاگین کنید. (نشست شما برای دفعات بعدی ذخیره می‌ماند)")
        input("\n>>> پس از ورود به دیوار در مرورگر، کلید Enter را در این ترمینال فشار دهید... ")
        print("-"*70 + "\n")
        
        while True:
            print("\n📋 لیست آگهی‌های دسته‌ای:")
            for i, ad in enumerate(ads, 1):
                status_icon = "⏳"
                if progress.get(ad['folder']) == "completed":
                    status_icon = "✅"
                elif progress.get(ad['folder']) == "skipped":
                    status_icon = "⏭️"
                print(f" [{i:02d}] {status_icon} {ad['title']} ({len(ad['images'])} تصویر)")
            
            print("\nدستورات:")
            print(" - شماره آگهی (مثلاً 1 یا 4)")
            print(" - عبارت 'all' برای ثبت مرحله‌به‌مرحله از اولین آگهی")
            print(" - عبارت 'q' برای خروج")
            
            choice = input("\nانتخاب شما: ").strip().lower()
            if choice == 'q':
                break
                
            selected_indices = []
            if choice == 'all':
                selected_indices = list(range(len(ads)))
            elif choice.isdigit() and 1 <= int(choice) <= len(ads):
                selected_indices = [int(choice) - 1]
            else:
                print("انتخاب نامعتبر!")
                continue
                
            for idx in selected_indices:
                ad = ads[idx]
                print("\n" + "="*70)
                print(f"📌 پردازش آگهی [{idx+1}/{len(ads)}]: {ad['title']}")
                print("="*70)
                
                # Copy description to clipboard
                copy_to_clipboard(ad['content'])
                print("✅ متن کامل آگهی در کلیپ‌بورد سیستم کپی شد (آماده Paste با Ctrl+V)")
                
                # Open images folder
                if os.path.exists(ad['images_dir']) and len(ad['images']) > 0:
                    print(f"📁 پوشه تصاویر ({len(ad['images'])} عکس) در ویندوز باز شد.")
                    print("👉 می‌توانید عکس‌ها را مستقیماً بگیرید و در کادر آپلود دیوار بکشید (Drag & Drop)")
                    open_folder_in_explorer(ad['images_dir'])
                else:
                    print("⚠️ تصویری در این پوشه یافت نشد.")
                    
                # Open Divar New Post URL
                print("\n🌐 در حال انتقال صفحه مرورگر به صفحه ثبت آگهی جدید اهواز...")
                try:
                    await page.goto("https://divar.ir/s/ahvaz/new", wait_until="domcontentloaded")
                except Exception as e:
                    print(f"خطا در رفتن به آدرس: {e}")
                    
                print("\n" + "-"*70)
                print("📝 اطلاعات پیشنهادی جهت ورود:")
                print(f"عنوان آگهی: {ad['title']}")
                print(f"قیمت: توافقی (بدون قیمت قطعی به دلیل نوسان بازار)")
                print(f"شهر: اهواز | محدوده: نادری")
                print("متن توضیحات: در کلیپ‌بورد شما ذخیره شده (کلید Ctrl + V را بزنید)")
                print("-"*70)
                
                print("\n👁️ لطفاً مشخصات آگهی را تا مرحله «پیش‌نمایش (Preview)» تکمیل و بررسی فرمایید.")
                action = input(">>> پس از بازبینی، کلید Enter را بزنید (یا 's' برای رد شدن / 'q' برای خروج): ").strip().lower()
                
                if action == 'q':
                    break
                elif action == 's':
                    progress[ad['folder']] = "skipped"
                    print(f"آگهی {ad['folder']} رد شد.")
                else:
                    progress[ad['folder']] = "completed"
                    print(f"✅ آگهی {ad['folder']} به عنوان ثبت‌شده ذخیره شد.")
                save_progress(progress)
                
            if choice == 'all' or choice == 'q':
                break

        print("\nسشن مرورگر در حال بسته شدن...")
        await context.close()
        print("برنامه با موفقیت به پایان رسید.")

if __name__ == "__main__":
    try:
        asyncio.run(run_semi_poster())
    except KeyboardInterrupt:
        print("\nعملیات توسط کاربر متوقف شد.")
