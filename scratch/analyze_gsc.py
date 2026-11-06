import csv
import io
import sys

sys.stdout.reconfigure(encoding='utf-8')

raw_data = '''Date,Clicks,Impressions,CTR,Position
2026-08-03,0,0,,
2026-08-04,0,0,,
2026-08-05,0,0,,
2026-08-06,0,2,0,9
2026-08-07,0,2,0,4
2026-08-08,0,4,0,6.2
2026-08-09,0,8,0,6.6
2026-08-10,1,8,0.125,7
2026-08-11,0,10,0,5.4
2026-08-12,0,11,0,11.8
2026-08-13,0,11,0,6.8
2026-08-14,2,21,0.0952,5.9
2026-08-15,5,17,0.2941,6.8
2026-08-16,4,38,0.1053,7.3
2026-08-17,2,33,0.0606,7.4
2026-08-18,3,35,0.0857,6.5
2026-08-19,2,36,0.0556,9.8
2026-08-20,1,28,0.0357,19.8
2026-08-21,1,29,0.0345,13.2
2026-08-22,2,50,0.04,13.8
2026-08-23,1,34,0.0294,17
2026-08-24,1,43,0.0233,14.3
2026-08-25,0,37,0,15.4
2026-08-26,0,36,0,15.9
2026-08-27,3,31,0.0968,13.6
2026-08-28,0,30,0,15.9
2026-08-29,3,34,0.0882,13
2026-08-30,1,27,0.037,19.6
2026-08-31,1,31,0.0323,22.2
2026-09-01,3,27,0.1111,19.1
2026-09-02,0,22,0,20.8
2026-09-03,1,21,0.0476,13.4
2026-09-04,2,27,0.0741,16.5
2026-09-05,2,44,0.0455,12.7
2026-09-06,2,44,0.0455,17.1
2026-09-07,0,27,0,13.3
2026-09-08,2,32,0.0625,14.3
2026-09-09,3,34,0.0882,12.8
2026-09-10,5,43,0.1163,11.1
2026-09-11,0,37,0,21.2
2026-09-12,2,29,0.069,20.8
2026-09-13,0,28,0,7.1
2026-09-14,0,28,0,8.8
2026-09-15,2,27,0.0741,18
2026-09-16,0,29,0,14.9
2026-09-17,2,43,0.0465,20
2026-09-18,2,34,0.0588,14
2026-09-19,1,31,0.0323,12
2026-09-20,3,24,0.125,12.4
2026-09-21,2,37,0.0541,17.5
2026-09-22,2,43,0.0465,12.4
2026-09-23,2,32,0.0625,15.6
2026-09-24,4,49,0.0816,9.9
2026-09-25,6,37,0.1622,16.3
2026-09-26,5,40,0.125,13.2
2026-09-27,6,60,0.1,13.3
2026-09-28,5,54,0.0926,15.3
2026-09-29,2,45,0.0444,16.1
2026-09-30,4,72,0.0556,14.4
2026-10-01,6,48,0.125,14
2026-10-02,6,59,0.1017,18.6
2026-10-03,9,79,0.1139,15.4
2026-10-04,7,59,0.1186,12.4
2026-10-05,3,69,0.0435,13.3
2026-10-06,3,58,0.0517,18.4
2026-10-07,3,74,0.0405,14.9
2026-10-08,3,54,0.0556,15.6
2026-10-09,4,64,0.0625,16.3
2026-10-10,3,70,0.0429,14.4
2026-10-11,6,37,0.1622,12.5
2026-10-12,9,74,0.1216,12.6
2026-10-13,7,55,0.1273,12.4
2026-10-14,5,69,0.0725,14.4
2026-10-15,6,56,0.1071,11.1
2026-10-16,3,71,0.0423,11.2
2026-10-17,4,55,0.0727,11.9
2026-10-18,2,85,0.0235,13.4'''

queries_raw = '''حسینی کالا,3,3,1,1
کالا بانک ملت حامی کارت,1,95,0.0105,9.45
آون توستر دلمونتی ۶۰ لیتری,1,13,0.0769,6.92
قیمت جاروبرقی بست bvc pc18b,1,7,0.1429,9.86
ماشین ظرفشویی کلور,1,3,0.3333,14.33
لیست فروشگاههای طرف قرارداد کارت رفاهی بانک رفاه,1,1,1,2
کالا کارت بانک مهر,1,1,1,2
لباسشویی دوو مدل 9170,1,1,1,22
طرح بتا بازنشستگان,1,1,1,32
اسپرسو ساز دونالکس 470,1,1,1,45
جارو برقی بوست,0,253,0,44.91
یخچال الکترواستیل,0,66,0,47.61
یخچال ایستکول,0,48,0,46.58
bajet tejarat,0,41,0,7.93
گوشت کوب برقی دونالکس,0,14,0,16.14
خرید بالکلی,0,14,0,88.21
قیمت بالکلی,0,11,0,75.64
جاروبرقی کلور,0,5,0,5.2
جاروبرقی بست,0,5,0,8.8
خرید اقساطی بازنشستگان تامین اجتماعی,0,5,0,20
خرید اقساطی بازنشستگان,0,4,0,20.75
کولر پرتابل ریتون ۱۶۰۰۰,0,3,0,6
یخچال 10 فوت کلور مدل mini refrigerator,0,3,0,9
برند کلور,0,3,0,9.67
ماشین اصلاح پرو امگا,0,3,0,9.67
ایرفرایر دونالکس,0,3,0,10
ظرفشویی کلور,0,3,0,15.67
خط تولید ایرفرایر,0,3,0,21.67
بهترین ماشین لباسشویی دوو,0,3,0,82.67
فوت فانتزی,0,2,0,3.5
بتا بانک رفاه,0,2,0,7.5
یخچال کلور 10 فوت,0,2,0,8
حامی کارت ملت,0,2,0,9.5
کتری برقی اریکسون,0,2,0,9.5
بخاری برقی گلدن لوکس,0,2,0,10
فروشگاه لوازم خانگی حسینی,0,2,0,10
ماشین اصلاح امگا,0,2,0,10
ظرفشویی کلور ۱۵ نفره,0,2,0,13
لوازم خانگی باجت,0,2,0,21
طرح بتا بانک رفاه,0,2,0,30.5
آب سرد کن افترون,0,2,0,31
یخچال فریزر الکترواستیل,0,2,0,35.5
خرید lc1f800bd,0,2,0,36.5
جاروبرقی پاناسونیک,0,2,0,37.5
یخچال فریزر ایستکول,0,2,0,47.5
چای ساز,0,2,0,96
لیست فروشگاههای اینترنتی طرف قرارداد کارت رفاهی بانک رفاه,0,1,0,3
ثبت نام کالا کارت بانک مهر ایران,0,1,0,4
کالا کارت,0,1,0,4
خرید اقساطی محصولات دوو,0,1,0,5
کولر ریتون ۱۶۰۰۰,0,1,0,5
ماشین اصلاح پرو امگا t5,0,1,0,8
نصب فرابانک ملت,0,1,0,8
beta refah,0,1,0,9
ظرفشویی ۱۵ نفره,0,1,0,9
وام دیجی پی بانک ملت,0,1,0,9
ابعاد یخچال ۷ فوت الکترواستیل,0,1,0,10
یخچال کمبی یعنی چی,0,1,0,10
لوازم خانگی حسینی,0,1,0,11
یخچال فریزر کمبی ۲۷ فوت های کلاس,0,1,0,13
ماشین لباس شویی کلور,0,1,0,14
زامروتی دیجی کالا,0,1,0,16
اسپرسو ساز دونالکس,0,1,0,17
وام حامی کارت,0,1,0,17
کولر آبی ریتون ۱۶۰۰۰,0,1,0,18
طرح دیپوینت باجت,0,1,0,20
lm9170,0,1,0,23
اسپرسو دونالکس,0,1,0,23
لباسشویی 9170,0,1,0,26
ماشین لباسشویی کلور ۹ کیلویی,0,1,0,26
سرخ کن دونالکس 950,0,1,0,27
یخچال کوچک برای مغازه,0,1,0,27
ثبت نام وام خرید کالا بانک ملت,0,1,0,28
ماشین اصلاح پرو امگا t10,0,1,0,28
ماشین ظرفشویی ۱۵ نفره,0,1,0,29
وام خرید کالا بانک ملت,0,1,0,29
برند دیپوینت,0,1,0,34
سامانه بتا بانک رفاه خرید اقساطی,0,1,0,34
ماشین قسطی اهواز,0,1,0,34
وام کالا بانک ملت,0,1,0,39
تفاوت کولر سلولزی و پوشالی,0,1,0,44
کولر آبی ریتون ۷۰۰۰,0,1,0,49
الکترو استیل فیوچر,0,1,0,50
دستگاه مخلوط کن,0,1,0,60
بهترین مارک ایرفرایر,0,1,0,62
ابعاد یخچال دو قلو,0,1,0,66
کولر آبی پرتابل,0,1,0,73
قیمت لباسشویی دوو,0,1,0,78
بهترین برند ایرفرایر ایرانی,0,1,0,80
سرخ کن,0,1,0,91
خرید اقساطی با چک صیاد,0,1,0,96
سرخ کن بدون روغن,0,1,0,96
خشک کردن میوه در ایرفرایر,0,1,0,100
وام خرید تلویزیون با اقساط ۶۰ ماهه,0,1,0,100'''

pages_raw = '''https://hosseinykala.ir/,31,59,0.5254,2.93
https://hosseinykala.ir/bajet-tejarat-refah-300m-appliances/,17,184,0.0924,9.69
https://hosseinykala.ir/refah-bank-beta-installment-guide/,12,130,0.0923,10.25
https://hosseinykala.ir/washing-machine-8kg-vs-9kg-guide/,12,111,0.1081,6.51
https://hosseinykala.ir/about-us/,11,57,0.193,5.65
https://hosseinykala.ir/mellat-bank-200m-appliances-loan-guide/,10,177,0.0565,9.24
https://hosseinykala.ir/contact-us/,9,68,0.1324,4.19
https://hosseinykala.ir/product/clover-bmw-t2-washing-machine-9kg/,8,96,0.0833,7.08
https://hosseinykala.ir/product/clover-fantasy-patterned-10ft-mini-refrigerator/,5,41,0.122,2.66
https://hosseinykala.ir/راهنمای-خرید-کولر-آبی-سلولزی-و-پرتابل؛/,5,36,0.1389,8.47
https://hosseinykala.ir/twin-refrigerator-buying-guide/,4,23,0.1739,6.87
https://hosseinykala.ir/category/راهنمای-خرید/,4,20,0.2,4.35
https://hosseinykala.ir/story/,4,20,0.2,4.95
https://hosseinykala.ir/product/clover-glory-plus-lm70-twin-refrigerator/,3,41,0.0732,8.54
https://hosseinykala.ir/لباسشویی-۸-کیلویی-بخریم-یا-۹-کیلویی؟-مق/,3,39,0.0769,9.69
https://hosseinykala.ir/product-category/اصلاح-و-زیبایی/اصلاح-موی-سر/pro-omega-hair-clippers/,3,30,0.1,8.8
https://hosseinykala.ir/mehr-iran-kalacard-bnpl-appliances-guide/,3,10,0.3,4.5
https://hosseinykala.ir/product-category/اصلاح-و-زیبایی/سشوار/pro-omega-hair-dryers/,3,4,0.75,8
https://hosseinykala.ir/product/pro-omega-t5-hair-clipper/,2,101,0.0198,7.5
https://hosseinykala.ir/راهنمای-خرید-یخچال-فریزر-دوقلو-در-سال-۱/,2,77,0.026,8.49
https://hosseinykala.ir/راهنمای-خرید-یخچال-کوچک-هتلی/,2,60,0.0333,6.8
https://hosseinykala.ir/product/clover-bmw-t3-washing-machine-8kg/,2,47,0.0426,7.13
https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-44-فوت-کلور-مدل-54-فوت-glory-plus-lm70/,2,42,0.0476,6.55
https://hosseinykala.ir/product/pro-omega-t7-hair-clipper/,2,33,0.0606,7.7
https://hosseinykala.ir/product/clover-economy-27ft-twin-refrigerator/,2,22,0.0909,4.55
https://hosseinykala.ir/combi-vs-twin-refrigerator-guide/,2,22,0.0909,6.09
https://hosseinykala.ir/product/ماشین-لباسشویی-9-کیلوگرم-اتوماتیک-کلور/,2,21,0.0952,6.43
https://hosseinykala.ir/product/daewoo-lm-9170-washing-machine-9kg/,2,17,0.1176,18.82
https://hosseinykala.ir/sayadi-cheque-installment-buying-guide/,2,12,0.1667,15.83
https://hosseinykala.ir/product/bost-bvc-pc18b-vacuum-cleaner/,1,193,0.0052,46.33
https://hosseinykala.ir/product-category/یخچال-فریزر/electrosteel-refrigerators/,1,72,0.0139,45.31
https://hosseinykala.ir/product/یخچال-10-فوت-کلور-مدل-mini-refrigerator/,1,47,0.0213,7.79
https://hosseinykala.ir/clover-brand-review/,1,30,0.0333,8.47
https://hosseinykala.ir/product/donallex-dn-275-hand-blender/,1,28,0.0357,12.82
https://hosseinykala.ir/blog/page/2/,1,26,0.0385,5.69
https://hosseinykala.ir/product/electrosteel-future-twin-refrigerator-21ft/,1,22,0.0455,9.27
https://hosseinykala.ir/product/یخچال-و-فریزر-27-فوت-کلور-مدل-كمبي-فريزر-پ/,1,21,0.0476,8.1
https://hosseinykala.ir/mini-hotel-refrigerator-buying-guide/,1,21,0.0476,8.95
https://hosseinykala.ir/product-category/washing-cleaning/ماشین-ظرفشویی/clover-dishwashers/,1,20,0.05,12.55
https://hosseinykala.ir/product/clover-bucket-vacuum-cleaner/,1,19,0.0526,2.84
https://hosseinykala.ir/product/reyton-vento-16000-portable-air-cooler/,1,19,0.0526,12.21
https://hosseinykala.ir/product/ماشین-لباسشویی-8-کیلوگرم-اتوماتیک-کلور/,1,16,0.0625,5.44
https://hosseinykala.ir/home-appliances-installment-buying-guide/,1,16,0.0625,12
https://hosseinykala.ir/product/delmonti-dn580-toaster-oven/,1,15,0.0667,7.13
https://hosseinykala.ir/product/depoint-boss-pro-refrigerator-30ft/,1,9,0.1111,5
https://hosseinykala.ir/product/سرخکن-8-لیتر-دونالکس-مدل-dn-950/,1,9,0.1111,8.44
https://hosseinykala.ir/product-category/drink-makers/مخلوط-کن/donallex-blenders/,1,8,0.125,6.38
https://hosseinykala.ir/product/ericsson-1-8l-electric-kettle/,1,7,0.1429,9.86
https://hosseinykala.ir/product-category/اسپرسو-ساز/donallex-espresso-makers/,1,7,0.1429,17.14
https://hosseinykala.ir/product/clover-rnt101-fnt101-twin-refrigerator-36ft/,1,6,0.1667,4.67
https://hosseinykala.ir/product/ماشین-لباسشویی-هوشمند-9-کیلوگرم-اتومات/,1,6,0.1667,5.83
https://hosseinykala.ir/product/reyton-vento-7000-air-cooler/,1,6,0.1667,22.67
https://hosseinykala.ir/product/اتو-بخار-۲۵۰۰-وات-دونالکس-مدل-815/,1,4,0.25,8.5
https://hosseinykala.ir/product/generalfit-cutie-4300-canister-vacuum-cleaner/,1,3,0.3333,6.67
https://hosseinykala.ir/product/maier-mr4099-digital-conical-burr-coffee-grinder/,1,1,1,9
https://hosseinykala.ir/product/جاروبرقی-بست-مدل-bvc-pc18b/,0,103,0,43.87
https://hosseinykala.ir/product-category/washing-cleaning/جاروبرقی/bost-vacuum-cleaners/,0,84,0,27.81
https://hosseinykala.ir/product-category/یخچال-فریزر/eastcool-refrigerators/,0,53,0,44.75
https://hosseinykala.ir/product-category/washing-cleaning/ماشین-لباسشویی/clover-washing-machines/,0,33,0,8.06
https://hosseinykala.ir/depoint-refrigerator-brand-review/,0,33,0,8.58
https://hosseinykala.ir/product/donallex-dn475-espresso-maker/,0,28,0,7.68
https://hosseinykala.ir/15-place-dishwasher-buying-guide/,0,18,0,8.39
https://hosseinykala.ir/راهنمای-خرید-ماشین-ظرفشویی-۱۵-نفره/,0,17,0,8.47
https://hosseinykala.ir/product/golden-luxe-gas-heater/,0,16,0,8.12
https://hosseinykala.ir/product/pro-omega-8806-hair-dryer/,0,15,0,7.67
https://hosseinykala.ir/product/ماشین-اصلاح-موی-سر-و-صورت-پرو-امگا-مدل-t7/,0,13,0,12.23
https://hosseinykala.ir/یخچال-کمبی-یا-دوقلو/,0,12,0,10.83
https://hosseinykala.ir/product-category/لوازم-برقی-آشپزخانه/گوشت-کوب-برقی/donallex-hand-blenders/,0,12,0,11.25
https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-21-فوت-الکترواستیل-مدل/,0,12,0,11.75
https://hosseinykala.ir/product-category/سرخ-کن/donallex-air-fryers/,0,11,0,7.55
https://hosseinykala.ir/product-category/یخچال-فریزر/clover-refrigerators/,0,11,0,9.64
https://hosseinykala.ir/product/himalia-ice-pool-60mw-twin-refrigerator/,0,10,0,6.9
https://hosseinykala.ir/product/ماشین-اصلاح-موی-سر-و-صورت-پرو-امگا-مدل-t5/,0,10,0,7.7
https://hosseinykala.ir/product/donallex-dn480-espresso-maker/,0,10,0,9.1
https://hosseinykala.ir/product/clover-mini-refrigerator-10ft/,0,9,0,9.44
https://hosseinykala.ir/product-category/گوشت-کوب-برقی/,0,9,0,9.56
https://hosseinykala.ir/product/گوشت-کوب-برقی-دونالکس-مدل-dn-275/,0,9,0,9.89
https://hosseinykala.ir/economical-dowry-checklist-guide/,0,9,0,15.56
https://hosseinykala.ir/portable-cellulose-air-cooler-guide/,0,9,0,22.56
https://hosseinykala.ir/product/willez-2015-tea-maker-2/,0,8,0,7.75
https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-40-فوت-کلور-مدل-گلوری-پ/,0,8,0,9
https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-34-فوت-دیپوینت-مدل-max-du-_-مک/,0,8,0,9.38
https://hosseinykala.ir/?add-to-cart=3305,0,8,0,89.62
https://hosseinykala.ir/product/eastcool-2919-hotel-refrigerator-9ft/,0,7,0,4.14
https://hosseinykala.ir/product/clover-rosso-plus-w60-twin-refrigerator-40ft/,0,7,0,5.57
https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-40-فوت-کلور-مدل-گلوری-ع/,0,7,0,6
https://hosseinykala.ir/product/haverson-75-inch-4k-smart-tv/,0,7,0,6
https://hosseinykala.ir/product-category/یخچال-فریزر/,0,7,0,6.14
https://hosseinykala.ir/product/کولر-آبی-سلولزی-16000-ریتون-مدل-کولر-پرتابل/,0,7,0,8.86
https://hosseinykala.ir/product/یخچال-و-فریزر-27-فوت-کلور-مدل-كمبي-هوم-بار/,0,7,0,9.29
https://hosseinykala.ir/product-category/drink-makers/اسپرسو-ساز/donallex-espresso-makers/,0,7,0,14.86
https://hosseinykala.ir/air-fryer-buying-guide/,0,7,0,39.43'''

def parse_csv(text):
    res = []
    for line in text.strip().split('\n'):
        parts = line.split(',')
        if len(parts) >= 5:
            res.append({
                'item': parts[0].strip('\"'),
                'clicks': int(parts[1]),
                'impr': int(parts[2]),
                'ctr': float(parts[3]) if parts[3] else 0.0,
                'pos': float(parts[4]) if parts[4] else 0.0
            })
    return res

q_list = parse_csv(queries_raw)
p_list = parse_csv(pages_raw)

print(f"Total queries analyzed: {len(q_list)}")
print(f"Total pages analyzed: {len(p_list)}")

# 1. Striking distance queries (Pos 4.0 - 15.0, Impr >= 3)
striking = [q for q in q_list if 4.0 <= q['pos'] <= 15.0 and q['impr'] >= 3]
striking.sort(key=lambda x: x['impr'], reverse=True)
print("\n--- TOP STRIKING DISTANCE QUERIES (Pos 4-15, Impr >= 3) ---")
for s in striking:
    print(f"Query: {s['item']} | Pos: {s['pos']} | Impr: {s['impr']} | Clicks: {s['clicks']} | CTR: {s['ctr']*100:.1f}%")

# 2. Loan & Installment Intent Queries
loan_keywords = ['بانک', 'کارت', 'وام', 'اقساط', 'بتا', 'باجت', 'قسطی', 'حامی']
loan_queries = [q for q in q_list if any(k in q['item'] for k in loan_keywords)]
loan_impr = sum(q['impr'] for q in loan_queries)
loan_clicks = sum(q['clicks'] for q in loan_queries)
print(f"\n--- LOAN & INSTALLMENT QUERIES: Total Impr: {loan_impr}, Total Clicks: {loan_clicks} ---")
for lq in sorted(loan_queries, key=lambda x: x['impr'], reverse=True):
    print(f"Query: {lq['item']} | Pos: {lq['pos']} | Impr: {lq['impr']} | Clicks: {lq['clicks']} | CTR: {lq['ctr']*100:.1f}%")

# 3. Top High Opportunity Pages (High Impr, CTR < 10% or Pos > 6)
print("\n--- HIGH OPPORTUNITY PAGES (Underperforming CTR or Near Top 3) ---")
opp_pages = [p for p in p_list if p['impr'] >= 20 and p['ctr'] < 0.10]
opp_pages.sort(key=lambda x: x['impr'], reverse=True)
for op in opp_pages:
    print(f"URL: {op['item']} | Impr: {op['impr']} | Clicks: {op['clicks']} | CTR: {op['ctr']*100:.1f}% | Pos: {op['pos']}")

# 4. Canonical / Duplicate Pairs
print("\n--- DUPLICATE / CANNIBALIZATION PAIRS FOUND ---")
persian_pages = [p for p in p_list if '%D' in p['item'] or any(ord(c) > 127 for c in p['item'].split('/')[-2])]
for pp in persian_pages:
    print(f"Persian/Old URL in GSC: {pp['item']} (Impr: {pp['impr']}, Clicks: {pp['clicks']}, Pos: {pp['pos']})")
