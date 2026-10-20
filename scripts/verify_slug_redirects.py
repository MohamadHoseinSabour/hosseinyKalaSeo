import sys
import requests
import json
import urllib.parse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

test_pairs = [
    # (Label, Old Persian URL, New English URL)
    (
        "Post 3000 (Air Cooler)",
        "https://hosseinykala.ir/راهنمای-خرید-کولر-آبی-سلولزی-و-پرتابل؛/",
        "https://hosseinykala.ir/portable-cellulose-air-cooler-guide/"
    ),
    (
        "Post 3098 (Mini Refrigerator)",
        "https://hosseinykala.ir/راهنمای-خرید-یخچال-کوچک-هتلی/",
        "https://hosseinykala.ir/mini-hotel-refrigerator-buying-guide/"
    ),
    (
        "Post 3099 (Dishwasher)",
        "https://hosseinykala.ir/راهنمای-خرید-ماشین-ظرفشویی-۱۵-نفره/",
        "https://hosseinykala.ir/15-place-dishwasher-buying-guide/"
    ),
    (
        "Post 3100 (Combi vs Twin)",
        "https://hosseinykala.ir/یخچال-کمبی-یا-دوقلو/",
        "https://hosseinykala.ir/combi-vs-twin-refrigerator-guide/"
    ),
    (
        "Post 3101 (Clover Review)",
        "https://hosseinykala.ir/بررسی-تخصصی-برند-کلور/",
        "https://hosseinykala.ir/clover-brand-review/"
    ),
    (
        "Post 3102 (Dowry Guide)",
        "https://hosseinykala.ir/چک-لیست-خرید-جهیزیه-اقتصادی/",
        "https://hosseinykala.ir/economical-dowry-checklist-guide/"
    ),
    (
        "Product 3453 (Electrosteel Future)",
        "https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-21-فوت-الکترواستیل-مدل/",
        "https://hosseinykala.ir/product/electrosteel-future-twin-refrigerator-21ft/"
    ),
    (
        "Product 2972 (Clover Glory Plus 54ft)",
        "https://hosseinykala.ir/product/یخچال-فریزر-گلوری-پلاس-دوقلو-کلور54-فوت/",
        "https://hosseinykala.ir/product/clover-glory-plus-54ft-twin-refrigerator/"
    ),
    (
        "Product 3395 (Himalia Alpha 28ft)",
        "https://hosseinykala.ir/product/یخچال-و-فریزر-دوقلو-28-فوت-هیمالیا-مدل-آ/",
        "https://hosseinykala.ir/product/himalia-alpha-twin-refrigerator-28ft/"
    ),
    (
        "Product 3266 (Pakshoma Split 18000)",
        "https://hosseinykala.ir/product/کولر-گازی-اسپلیت-دیواری-18000-دور-ثابت-پا/",
        "https://hosseinykala.ir/product/pakshoma-18000-split-air-conditioner/"
    )
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print("=== VERIFYING SLUGS AND 301 REDIRECTS ===\n", flush=True)
results = []
for label, old_url, new_url in test_pairs:
    # 1. Test new English URL (Should be 200)
    new_status = None
    try:
        r_new = requests.get(new_url, headers=headers, allow_redirects=False, timeout=12)
        new_status = r_new.status_code
    except Exception as e:
        new_status = f"ERR ({e})"

    # 2. Test old Persian URL (Should be 301 -> new_url)
    old_status = None
    redirect_to = None
    try:
        r_old = requests.get(old_url, headers=headers, allow_redirects=False, timeout=12)
        old_status = r_old.status_code
        redirect_to = r_old.headers.get('Location', '')
    except Exception as e:
        old_status = f"ERR ({e})"

    status_match = "PASS" if (new_status == 200 and old_status in [301, 302]) else "CHECK"
    print(f"[{status_match}] {label}:", flush=True)
    print(f"   New URL ({new_status}): {new_url}", flush=True)
    print(f"   Old URL ({old_status}): {old_url} -> Redirects To: {redirect_to}\n", flush=True)
    results.append({
        'label': label,
        'new_url': new_url,
        'new_status': new_status,
        'old_url': old_url,
        'old_status': old_status,
        'redirect_to': redirect_to,
        'status_match': status_match
    })

with open('data/slug_redirect_verification_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved verification results to data/slug_redirect_verification_results.json", flush=True)
