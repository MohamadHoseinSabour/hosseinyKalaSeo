import requests
import json
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

gsc_pages = [
    'https://hosseinykala.ir/about-us/',
    'https://hosseinykala.ir/contact-us/',
    'https://hosseinykala.ir/راهنمای-خرید-کولر-آبی-سلولزی-و-پرتابل؛/',
    'https://hosseinykala.ir/category/راهنمای-خرید/',
    'https://hosseinykala.ir/washing-machine-8kg-vs-9kg-guide/',
    'https://hosseinykala.ir/twin-refrigerator-buying-guide/',
    'https://hosseinykala.ir/product/clover-bmw-t2-washing-machine-9kg/',
    'https://hosseinykala.ir/product/clover-glory-plus-lm70-twin-refrigerator/',
    'https://hosseinykala.ir/لباسشویی-۸-کیلویی-بخریم-یا-۹-کیلویی؟-مق/',
    'https://hosseinykala.ir/story/',
    'https://hosseinykala.ir/product/pro-omega-t5-hair-clipper/',
    'https://hosseinykala.ir/راهنمای-خرید-یخچال-فریزر-دوقلو-در-سال-۱/',
    'https://hosseinykala.ir/راهنمای-خرید-یخچال-کوچک-هتلی/',
    'https://hosseinykala.ir/product/clover-bmw-t3-washing-machine-8kg/',
    'https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-44-فوت-کلور-مدل-54-فوت-glory-plus-lm70/',
    'https://hosseinykala.ir/product/ماشین-لباسشویی-9-کیلوگرم-اتوماتیک-کلور/',
    'https://hosseinykala.ir/product/bost-bvc-pc18b-vacuum-cleaner/',
    'https://hosseinykala.ir/product/donallex-dn-275-hand-blender/',
    'https://hosseinykala.ir/product/pro-omega-t7-hair-clipper/',
    'https://hosseinykala.ir/product/electrosteel-future-twin-refrigerator-21ft/',
    'https://hosseinykala.ir/product/reyton-vento-16000-portable-air-cooler/',
    'https://hosseinykala.ir/product/ماشین-لباسشویی-8-کیلوگرم-اتوماتیک-کلور/',
    'https://hosseinykala.ir/blog/page/2/',
    'https://hosseinykala.ir/product/depoint-boss-pro-refrigerator-30ft/',
    'https://hosseinykala.ir/product/daewoo-lm-9170-washing-machine-9kg/',
    'https://hosseinykala.ir/product-category/اسپرسو-ساز/donallex-espresso-makers/',
    'https://hosseinykala.ir/product/ماشین-لباسشویی-هوشمند-9-کیلوگرم-اتومات/',
    'https://hosseinykala.ir/product/reyton-vento-7000-air-cooler/',
    'https://hosseinykala.ir/product/اتو-بخار-۲۵۰۰-وات-دونالکس-مدل-815/',
    'https://hosseinykala.ir/product/یخچال-و-فریزر-27-فوت-کلور-مدل-كمبي-فريزر-پ/',
    'https://hosseinykala.ir/product/جاروبرقی-بست-مدل-bvc-pc18b/',
    'https://hosseinykala.ir/product-category/یخچال-فریزر/electrosteel-refrigerators/',
    'https://hosseinykala.ir/product/یخچال-10-فوت-کلور-مدل-mini-refrigerator/',
    'https://hosseinykala.ir/product-category/یخچال-فریزر/eastcool-refrigerators/',
    'https://hosseinykala.ir/product/donallex-dn475-espresso-maker/',
    'https://hosseinykala.ir/راهنمای-خرید-ماشین-ظرفشویی-۱۵-نفره/',
    'https://hosseinykala.ir/product/pro-omega-8806-hair-dryer/',
    'https://hosseinykala.ir/product-category/اصلاح-و-زیبایی/اصلاح-موی-سر/pro-omega-hair-clippers/',
    'https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-21-فوت-الکترواستیل-مدل/',
    'https://hosseinykala.ir/product-category/washing-cleaning/جاروبرقی/bost-vacuum-cleaners/',
    'https://hosseinykala.ir/product-category/یخچال-فریزر/clover-refrigerators/',
    'https://hosseinykala.ir/یخچال-کمبی-یا-دوقلو/',
    'https://hosseinykala.ir/product/ماشین-اصلاح-موی-سر-و-صورت-پرو-امگا-مدل-t5/',
    'https://hosseinykala.ir/product/clover-mini-refrigerator-10ft/',
    'https://hosseinykala.ir/product-category/گوشت-کوب-برقی/',
    'https://hosseinykala.ir/product/گوشت-کوب-برقی-دونالکس-مدل-dn-275/',
    'https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-34-فوت-دیپوینت-مدل-max-du-_-مک/',
    'https://hosseinykala.ir/product/eastcool-2919-hotel-refrigerator-9ft/',
    'https://hosseinykala.ir/product/clover-rosso-plus-w60-twin-refrigerator-40ft/',
    'https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-40-فوت-کلور-مدل-گلوری-ع/',
    'https://hosseinykala.ir/product/delmonti-dn580-toaster-oven/',
    'https://hosseinykala.ir/product/یخچال-و-فریزر-27-فوت-کلور-مدل-كمبي-هوم-بار/',
    'https://hosseinykala.ir/product/donallex-dn480-espresso-maker/',
    'https://hosseinykala.ir/product-category/یخچال-فریزر/',
    'https://hosseinykala.ir/product-category/ماشین-ظرفشویی/clover-dishwashers/',
    'https://hosseinykala.ir/product/کولر-آبی-سلولزی-16000-ریتون-مدل-کولر-پرتابل/',
    'https://hosseinykala.ir/product/سرخکن-8-لیتر-دونالکس-مدل-dn-950/',
    'https://hosseinykala.ir/product/depoint-t7-refrigerator-28ft/',
    'https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-40-فوت-کلور-مدل-گلوری-پ/',
    'https://hosseinykala.ir/product/depoint-max-du-twin-refrigerator-34ft/',
    'https://hosseinykala.ir/product/donallex-815-steam-iron-2500w/',
    'https://hosseinykala.ir/depoint-refrigerator-brand-review/',
    'https://hosseinykala.ir/product/clover-rnt101-fnt101-twin-refrigerator-36ft/',
    'https://hosseinykala.ir/product/دستگاه-تصفیه-کننده-آب-سافت-واتر-مدل-ir-06/',
    'https://hosseinykala.ir/product/یخچال-فریزر-9-فوت-ایستکول-مدل-هتلی-2919،-با/',
    'https://hosseinykala.ir/product-category/washing-cleaning/ماشین-لباسشویی/clover-washing-machines/',
    'https://hosseinykala.ir/product/اسپرسو-ساز-۱۸-میلی-لیتر-دونالکس-مدل-dn475/',
    'https://hosseinykala.ir/product/یخچال-و-فریزر-دوقلو-36-فوت-کلوِر-مدل-rnt101-fnt101/',
    'https://hosseinykala.ir/product/ماشین-اصلاح-موی-سر-و-صورت-پرو-امگا-مدل-t7/',
    'https://hosseinykala.ir/product-category/ماشین-لباسشویی/',
    'https://hosseinykala.ir/product/clover-frnt-70-glory-plus/',
    'https://hosseinykala.ir/product/clover-rosso-homebar-refrigerator-27ft/',
    'https://hosseinykala.ir/product/haverson-75-inch-4k-smart-tv/',
    'https://hosseinykala.ir/product/donallex-dn-120-juicer-1000w/',
    'https://hosseinykala.ir/product/اسپرسو-ساز-۱۲-میلی-لیتر-دونالکس-مدلdn480/',
    'https://hosseinykala.ir/shop/',
    'https://hosseinykala.ir/product-category/سرخ-کن/',
    'https://hosseinykala.ir/product-category/صوتی،-تصویری-و-گرمایشی/',
    'https://hosseinykala.ir/product-category/سرخ-کن/donallex-air-fryers/',
    'https://hosseinykala.ir/product-category/کولر-گازی/',
    'https://hosseinykala.ir/blog/',
    'https://hosseinykala.ir/product-category/washing-cleaning/ماشین-ظرفشویی/clover-dishwashers/',
    'https://hosseinykala.ir/product/ماشین-ظرفشویی-15-نفره-کلور-مدل-cdw-h15tw1/',
    'https://hosseinykala.ir/product/یخچال-و-فریزر-27-فوت-کلوِر-مدل-frnt101/',
    'https://hosseinykala.ir/تخفیف-ها-و-پیشنهادات/',
    'https://hosseinykala.ir/product-category/washing-cleaning/ماشین-لباسشویی/',
    'https://hosseinykala.ir/product/oviz-black-granite-pots/',
    'https://hosseinykala.ir/product/clover-cdw-h15v-dishwasher-15p/',
    'https://hosseinykala.ir/product-category/audio-video/',
    'https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-40-فوت-کلور-مدل-رسوپلا/',
    'https://hosseinykala.ir/product-category/washing-cleaning/جاروبرقی/panasonic-vacuum-cleaners/',
    'https://hosseinykala.ir/product/آبمیوهگیری-1000-وات-دونالکس-مدل-dn-120/',
    'https://hosseinykala.ir/product-category/سشوار/',
    'https://hosseinykala.ir/product-category/drink-makers/اسپرسو-ساز/',
    'https://hosseinykala.ir/product-category/جاروبرقی/',
    'https://hosseinykala.ir/home-appliances-installment-buying-guide/',
    'https://hosseinykala.ir/order-tracking/',
    'https://hosseinykala.ir/product/oviz-plus-black-12pcs-cookware-set/',
    'https://hosseinykala.ir/category/راهنمای-خرید/page/2/',
    'https://hosseinykala.ir/product/eastcool-2835-refrigerator-5ft/',
    'https://hosseinykala.ir/product/pakshoma-21kg-twin-tub-washer/',
    'https://hosseinykala.ir/air-fryer-buying-guide/',
    'https://hosseinykala.ir/product-category/مخلوط-کن/donallex-blenders/',
    'https://hosseinykala.ir/product/یخچال-5-فوت-ایستکول-مدل-2835/',
    'https://hosseinykala.ir/product-category/اصلاح-و-زیبایی/سشوار/pro-omega-hair-dryers/',
    'https://hosseinykala.ir/refah-bank-beta-installment-guide/',
    'https://hosseinykala.ir/product-category/اصلاح-و-زیبایی/',
    'https://hosseinykala.ir/product/ماشین-ظرفشویی-16-نفره-کلور-مدل-cdw-h16tw1/',
    'https://hosseinykala.ir/product-category/مخلوط-کن/',
    'https://hosseinykala.ir/product/یخچال-و-فریزر-28-فوت-دیپوینت-مدل-t7،-بدون-بر/',
    'https://hosseinykala.ir/product/clover-glory-w60-twin-refrigerator-40ft/',
    'https://hosseinykala.ir/product/سشوار-حرفه-ای-پرو-امگا-مدل-8806/',
    'https://hosseinykala.ir/علاقه-مندی-ها/',
    'https://hosseinykala.ir/product/یخچال-فریزر-30-فوت-دیپوینت-مدل-boss-pro/',
    'https://hosseinykala.ir/product/donallex-dn-950-air-fryer-8l/',
    'https://hosseinykala.ir/product/جاروبرقی-پاناسونیک-مدل-mc-cg715/'
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def check_url(url):
    try:
        r = requests.get(url, headers=headers, allow_redirects=False, timeout=6)
        loc = r.headers.get('Location', '')
        return {'url': url, 'status': r.status_code, 'location': loc}
    except Exception as e:
        return {'url': url, 'status': 'ERR', 'location': str(e)}

results = []
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(check_url, u): u for u in gsc_pages}
    for future in as_completed(futures):
        res = future.result()
        results.append(res)
        print(f"[{res['status']}] {res['url'][:45]} -> {res['location'][:45]}", flush=True)

with open('data/gsc_url_check.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nAll {len(results)} URLs checked and saved to data/gsc_url_check.json", flush=True)
