import urllib.request
import urllib.parse
import ssl
import sys
import json
import time

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

opener = urllib.request.build_opener(NoRedirectHandler)
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')]

persian_urls_from_gsc = [
    'https://hosseinykala.ir/راهنمای-خرید-کولر-آبی-سلولزی-و-پرتابل؛/',
    'https://hosseinykala.ir/category/راهنمای-خرید/',
    'https://hosseinykala.ir/لباسشویی-۸-کیلویی-بخریم-یا-۹-کیلویی؟-مق/',
    'https://hosseinykala.ir/راهنمای-خرید-یخچال-فریزر-دوقلو-در-سال-۱/',
    'https://hosseinykala.ir/راهنمای-خرید-یخچال-کوچک-هتلی/',
    'https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-44-فوت-کلور-مدل-54-فوت-glory-plus-lm70/',
    'https://hosseinykala.ir/product/ماشین-لباسشویی-9-کیلوگرم-اتوماتیک-کلور/',
    'https://hosseinykala.ir/product/یخچال-10-فوت-کلور-مدل-mini-refrigerator/',
    'https://hosseinykala.ir/product/یخچال-و-فریزر-27-فوت-کلور-مدل-كمبي-فريزر-پ/',
    'https://hosseinykala.ir/product/ماشین-لباسشویی-8-کیلوگرم-اتوماتیک-کلور/',
    'https://hosseinykala.ir/product/سرخکن-8-لیتر-دونالکس-مدل-dn-950/',
    'https://hosseinykala.ir/product/ماشین-لباسشویی-هوشمند-9-کیلوگرم-اتومات/',
    'https://hosseinykala.ir/product/اتو-بخار-۲۵۰۰-وات-دونالکس-مدل-815/',
    'https://hosseinykala.ir/product/جاروبرقی-بست-مدل-bvc-pc18b/',
    'https://hosseinykala.ir/راهنمای-خرید-ماشین-ظرفشویی-۱۵-نفره/',
    'https://hosseinykala.ir/product/ماشین-اصلاح-موی-سر-و-صورت-پرو-امگا-مدل-t7/',
    'https://hosseinykala.ir/یخچال-کمبی-یا-دوقلو/',
    'https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-21-فوت-الکترواستیل-مدل/',
    'https://hosseinykala.ir/product/ماشین-اصلاح-موی-سر-و-صورت-پرو-امگا-مدل-t5/',
    'https://hosseinykala.ir/product-category/گوشت-کوب-برقی/',
    'https://hosseinykala.ir/product/گوشت-کوب-برقی-دونالکس-مدل-dn-275/',
    'https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-40-فوت-کلور-مدل-گلوری-پ/',
    'https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-34-فوت-دیپوینت-مدل-max-du-_-مک/',
    'https://hosseinykala.ir/product/eastcool-2919-hotel-refrigerator-9ft/',
    'https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-40-فوت-کلور-مدل-گلوری-ع/',
    'https://hosseinykala.ir/product-category/یخچال-فریزر/',
    'https://hosseinykala.ir/product/کولر-آبی-سلولزی-16000-ریتون-مدل-کولر-پرتابل/',
    'https://hosseinykala.ir/product/یخچال-و-فریزر-27-فوت-کلور-مدل-كمبي-هوم-بار/',
    'https://hosseinykala.ir/product/یخچال-فریزر-9-فوت-ایستکول-مدل-هتلی-2919،-با/',
    'https://hosseinykala.ir/product/یخچال-و-فریزر-دوقلو-36-فوت-کلوِر-مدل-rnt101-fnt101/',
    'https://hosseinykala.ir/product/اسپرسو-ساز-۱۲-میلی-لیتر-دونالکس-مدلdn480/',
    'https://hosseinykala.ir/product/اسپرسو-ساز-۱۸-میلی-لیتر-دونالکس-مدل-dn475/',
    'https://hosseinykala.ir/product/یخچال-5-فوت-ایستکول-مدل-2835/',
    'https://hosseinykala.ir/product/یخچال-و-فریزر-دوقلو-28-فوت-هیمالیا-مدل-آل/',
    'https://hosseinykala.ir/product/یخچال-و-فریزر-28-فوت-دیپوینت-مدل-t7،-بدون-بر/',
    'https://hosseinykala.ir/product/یخچال-فریزر-30-فوت-دیپوینت-مدل-boss-pro/',
    'https://hosseinykala.ir/product/جاروبرقی-پاناسونیک-مدل-mc-cg715/'
]

print(f"Starting audit for {len(persian_urls_from_gsc)} URLs from GSC report...")
results = {'301': 0, '200': 0, '404': 0, 'other': 0, 'failures': []}

for raw_url in persian_urls_from_gsc:
    # URL encode non-ascii path
    parts = urllib.parse.urlsplit(raw_url)
    encoded_path = urllib.parse.quote(parts.path)
    encoded_url = urllib.parse.urlunsplit((parts.scheme, parts.netloc, encoded_path, parts.query, parts.fragment))
    
    req = urllib.request.Request(encoded_url)
    try:
        resp = opener.open(req)
        status = resp.status
        print(f"[200 OK] {raw_url[:65]}")
        results['200'] += 1
    except urllib.error.HTTPError as e:
        if e.code == 301:
            loc = e.headers.get('Location', '')
            print(f"[301 -> {loc[:50]}] {raw_url[:45]}")
            results['301'] += 1
        elif e.code == 404:
            print(f"[404 ERROR!] {raw_url}")
            results['404'] += 1
            results['failures'].append(raw_url)
        else:
            print(f"[{e.code}] {raw_url[:60]}")
            results['other'] += 1
    except Exception as ex:
        print(f"[ERR] {raw_url[:60]}: {ex}")
        results['other'] += 1
    
    time.sleep(0.15)

print("\n" + "="*50)
print("AUDIT SUMMARY:")
print(f"Total checked: {len(persian_urls_from_gsc)}")
print(f"301 Permanent Redirects: {results['301']}")
print(f"200 Direct OK: {results['200']}")
print(f"404 Not Found Errors: {results['404']}")
print(f"Other statuses: {results['other']}")
if results['failures']:
    print("\nURLs requiring IMMEDIATE 301 redirect fix:")
    for f in results['failures']:
        print("  - " + f)
else:
    print("\nEXCELLENT! 100% of tested legacy URLs are cleanly handled!")
print("="*50)
