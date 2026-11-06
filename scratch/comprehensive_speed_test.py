import requests
import time
import re
import sys

# Set console encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()

test_urls = [
    {
        "name": "صفحه اصلی (Homepage)",
        "url": "https://hosseinykala.ir/",
        "expected_pattern": r"حسینی کالا|خرید نقد و اقساط",
        "forbidden_pattern": r"کارت ویزیت - حسینی کالا"
    },
    {
        "name": "کارت ویزیت آنلاین (/contact)",
        "url": "https://hosseinykala.ir/contact",
        "expected_pattern": r"کارت ویزیت",
        "forbidden_pattern": r"خرید نقد و اقساط|پرفروش‌ترین"
    },
    {
        "name": "کارت ویزیت آنلاین با اسلش (/contact/)",
        "url": "https://hosseinykala.ir/contact/",
        "expected_pattern": r"کارت ویزیت",
        "forbidden_pattern": r"خرید نقد و اقساط|پرفروش‌ترین"
    },
    {
        "name": "فروشگاه اصلی (/shop/)",
        "url": "https://hosseinykala.ir/shop/",
        "expected_pattern": r"فروشگاه",
        "forbidden_pattern": r"کارت ویزیت"
    },
    {
        "name": "صفحه تکی محصول (/product/...)",
        "url": "https://hosseinykala.ir/product/depoint-decent-combi-refrigerator-freezer/",
        "expected_pattern": r"دیپوینت|تومان|افزودن به سبد خرید",
        "forbidden_pattern": r"کارت ویزیت"
    },
    {
        "name": "آرشیو وبلاگ (/blog/)",
        "url": "https://hosseinykala.ir/blog/",
        "expected_pattern": r"وبلاگ|مقالات|راهنما",
        "forbidden_pattern": r"کارت ویزیت"
    },
    {
        "name": "پست تکی وبلاگ (راهنمای خرید لباسشویی)",
        "url": "https://hosseinykala.ir/washing-machine-buying-guide-khuzestan/",
        "expected_pattern": r"راهنمای خرید|لباسشویی",
        "forbidden_pattern": r"کارت ویزیت"
    },
    {
        "name": "تماس با ما (/contact-us/)",
        "url": "https://hosseinykala.ir/contact-us/",
        "expected_pattern": r"تماس با ما",
        "forbidden_pattern": r"کارت ویزیت"
    },
    {
        "name": "درباره ما (/about-us/)",
        "url": "https://hosseinykala.ir/about-us/",
        "expected_pattern": r"درباره ما",
        "forbidden_pattern": r"کارت ویزیت"
    }
]

headers_mobile = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
}

print("=" * 80)
print("🚀 مرحله ۱: ارسال درخواست اولیه (Prime Cache)")
print("=" * 80)

for item in test_urls:
    try:
        t0 = time.time()
        res = session.get(item["url"], headers=headers_mobile, timeout=20, allow_redirects=True)
        ttfb = (time.time() - t0) * 1000
        cache_hdr = res.headers.get("X-HosseinyKala-Cache", "MISSING")
        print(f"[{res.status_code}] {item['name']:<35} | TTFB: {ttfb:6.0f}ms | Cache: {cache_hdr}")
    except Exception as e:
        print(f"[ERR] {item['name']}: {e}")

time.sleep(1)

print("\n" + "=" * 80)
print("⚡ مرحله ۲: بررسی کش سریع FastCache (Hit Test & TTFB & محتوا)")
print("=" * 80)

success_count = 0

for item in test_urls:
    try:
        t0 = time.time()
        res = session.get(item["url"], headers=headers_mobile, timeout=10, allow_redirects=True)
        ttfb = (time.time() - t0) * 1000
        cache_hdr = res.headers.get("X-HosseinyKala-Cache", "MISSING")
        encoding = res.headers.get("Content-Encoding", "none")
        
        # Check expected pattern
        has_expected = bool(re.search(item["expected_pattern"], res.text))
        has_forbidden = bool(re.search(item["forbidden_pattern"], res.text))
        
        status_symbol = "✅" if (cache_hdr == "HIT" and has_expected and not has_forbidden) else "❌"
        if status_symbol == "✅":
            success_count += 1
            
        print(f"{status_symbol} {item['name']:<35} | TTFB: {ttfb:5.0f}ms | Cache: {cache_hdr:<3} | Enc: {encoding:<4} | Exp: {has_expected} | NoForbid: {not has_forbidden}")
        if not has_expected:
            print(f"   ⚠️ هشدار محتوا: عبارت مورد انتظار '{item['expected_pattern']}' در صفحه یافت نشد!")
        if has_forbidden:
            print(f"   🚨 خطای تداخل کش: عبارت ممنوعه '{item['forbidden_pattern']}' در این صفحه پیدا شد!")
    except Exception as e:
        print(f"❌ {item['name']}: {e}")

print("=" * 80)
print(f"نتیجه نهایی: {success_count}/{len(test_urls)} صفحه با موفقیت کامل از کش سریع با محتوای ۱۰۰٪ صحیح سرو شدند.")
print("=" * 80)
