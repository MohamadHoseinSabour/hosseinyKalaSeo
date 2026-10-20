"""
update_website_products_requested.py
====================================
اسکریپت به‌روزرسانی محصولات روی سایت حسینی کالا بر اساس درخواست کاربر:
۱. محصول ۳۶۲۶: تبدیل به «آبمیوه‌گیری ۴ کاره دونالکس مدل DN-290» با اسلاگ donalex-dn290-4in1-juicer و دسته‌بندی آبمیوه گیری
۲. محصول ۴۰۹۵: تبدیل به «سرخ‌کن بدون روغن ساپر 7.2 لیتر مدل SAF-1710» با اصلاح کامل متون از هواپز به سرخ‌کن بدون روغن
۳. محصول ۳۴۹۴: تبدیل به «شیور و ماشین اصلاح ۵ کاره پرومارون مدل RL-614 ضدآب» با اسلاگ promaron-rl614-shaver-grooming-kit و تمرکز بر شیور
۴. محصول ۳۷۰۹ و ۴۰۶۸ (پتوشور پاکیزان): موجود کردن (instock) و تنظیم قیمت ۲۸ میلیون تومان با ۵٪ تخفیف (۲۶.۶ میلیون تومان) روی محصول ساده و تنوع‌های محصول متغیر
"""

import os
import sys
import json
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}
WC_URL = 'https://hosseinykala.ir/wp-json/wc/v3/products'

def update_product_3626():
    print("=== ۱. به‌روزرسانی محصول ۳۶۲۶ (آبمیوه‌گیری ۲۹۰ دونالکس) ===")
    short_desc = """<ul>
<li><strong>نوع دستگاه:</strong> آبمیوه‌گیری چندکاره پرقدرت ۸۰۰ وات ۴ کاره دونالکس</li>
<li><strong>عملکردها:</strong> آبمیوه‌گیری، مخلوط‌کن، خردکن و آسیاب برقی</li>
<li><strong>تیغه و فیلتر:</strong> تیغه‌های تمام استیل ضدزنگ با فیلتر میکرومش جهت آبگیری کامل انواع میوه</li>
<li><strong>بدنه و متریال:</strong> بدنه مقاوم استیل ضدزنگ و مخزن تفاله‌گیر بزرگ مجزا</li>
<li><strong>ضمانت و اصالت:</strong> ضمانت اصالت فیزیکی کالا در فروشگاه لوازم خانگی حسینی اهواز</li>
</ul>"""

    desc = """<h2>بررسی تخصصی و راهنمای خرید آبمیوه‌گیری ۴ کاره دونالکس مدل DN-290</h2>
<p>تهیه آبمیوه طبیعی و تازه، همراه با آماده‌سازی سریع اسموتی، خرد کردن مواد اولیه و آسیاب دانه‌ها نیازمند دستگاهی همه‌کاره و پرتوان در آشپزخانه است. <strong>آبمیوه‌گیری ۴ کاره دونالکس مدل DN-290</strong> از برند معتبر <strong>دونالکس (Donalex)</strong>، انتخابی ایده‌آل برای بانوانی است که می‌خواهند با یک دستگاه جمع‌وجور، چندین کارایی متنوع را با بالاترین راندمان تجربه کنند.</p>

<h3>ویژگی‌های برجسته آبمیوه‌گیری چندکاره دونالکس ۲۹۰</h3>
<ul>
<li><strong>موتور پرتوان و کم‌صدا:</strong> موتور قدرتمند ۸۰۰ وات با راندمان بالا و مصرف بهینه، به راحتی سخت‌ترین میوه‌ها و سبزیجات (سیب، هویج، کرفس) را آبگیری می‌کند.</li>
<li><strong>تیغه و فیلتر استیل ضدزنگ:</strong> شبکه فیلتر میکرومش تفاله‌ها را به شکل حداکثری خشک کرده و بیشترین میزان آب زلال را تحویل می‌دهد.</li>
<li><strong>مجموعه ۴ کاره کامل:</strong> دارای پارچ مخلوط‌کن، مخزن خردکن پیرکس و محفظه آسیاب جهت خرد کردن آجیل، ادویه و سبزیجات.</li>
<li><strong>سیستم ایمنی ضدلغزش:</strong> پایه‌های مکنده محکم از لرزش و حرکت دستگاه روی کابینت جلوگیری می‌نمایند.</li>
</ul>

<h2>جدول مشخصات فنی آبمیوه‌گیری دونالکس مدل DN-290</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">دونالکس (Donalex)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">DN-290</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">آبمیوه‌گیری ۴ کاره (آبمیوه‌گیر، مخلوط‌کن، خردکن، آسیاب)</td></tr>
<tr><td style="padding: 8px;"><strong>توان مصرفی</strong></td><td style="padding: 8px;">۸۰۰ وات</td></tr>
<tr><td style="padding: 8px;"><strong>جنس تیغه</strong></td><td style="padding: 8px;">استیل ضدزنگ SUS304</td></tr>
<tr><td style="padding: 8px;"><strong>تنظیمات سرعت</strong></td><td style="padding: 8px;">چندسردعته به همراه عملکرد لحظه‌ای (Pulse)</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی و اصالت</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت فیزیکی از فروشگاه حسینی</td></tr>
</tbody>
</table>

<p>شما می‌توانید این محصول باکیفیت را با اطمینان خاطر و بهترین قیمت از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> سفارش دهید یا برای خرید حضوری به شعب ما در <strong>اهواز</strong> مراجعه فرمایید.</p>"""

    payload = {
        'name': 'آبمیوه‌گیری ۴ کاره دونالکس مدل DN-290',
        'slug': 'donalex-dn290-4in1-juicer',
        'categories': [{'id': 120}, {'id': 165}, {'id': 240}],
        'short_description': short_desc,
        'description': desc
    }

    r = requests.put(f'{WC_URL}/3626', auth=AUTH, headers=HEADERS, json=payload, timeout=20)
    if r.status_code == 200:
        print("   ✓ محصول ۳۶۲۶ با موفقیت به‌روزرسانی شد.")
        print(f"     نام: {r.json()['name']} | اسلاگ: {r.json()['slug']}")
    else:
        print(f"   ❌ خطا در به‌روزرسانی ۳۶۲۶: {r.status_code} - {r.text}")


def update_product_4095():
    print("\n=== ۲. به‌روزرسانی محصول ۴۰۹۵ (سرخ‌کن بدون روغن ساپر) ===")
    short_desc = """<ul>
<li><strong>نوع دستگاه:</strong> سرخ‌کن بدون روغن (ایرفرایر) ساپر با ظرفیت جادار ۷.۲ لیتر</li>
<li><strong>فناوری پخت:</strong> گردش هوای داغ ۳۶۰ درجه برای پخت ترد و سالم با کاهش ۸۵٪ مصرف روغن</li>
<li><strong>توان و کنترل:</strong> موتور قدرتمند با پنل تنظیم دقیق دما و زمان پخت</li>
<li><strong>مخزن و پوشش:</strong> دیگ نچسب ضدخش با قابلیت شستشوی سریع و آسان</li>
<li><strong>تضمین اصالت:</strong> ضمانت ۱۰۰٪ اصالت کالا و ارسال سریع از فروشگاه لوازم خانگی حسینی</li>
</ul>
<p>با سرخ‌کن بدون روغن ساپر 7.2 لیتر مدل SAF-1710، انواع غذاهای رژیمی و لذیذ را با کمترین روغن و بهترین کیفیت در خانه آماده کنید.</p>"""

    desc = """<h2>بررسی تخصصی و عملکرد سرخ‌کن بدون روغن ساپر 7.2 لیتر مدل SAF-1710</h2>
<p>سرعت و سلامت در آشپزی روزانه زمانی محقق می‌شود که از وسایل استاندارد و مدرن استفاده کنید. <strong>سرخ‌کن بدون روغن ساپر 7.2 لیتر مدل SAF-1710</strong> ساخت برند معتبر <strong>ساپر (Saper)</strong> ابزاری ایده‌آل برای آماده‌سازی غذاهای برشته، ترد و کاملاً رژیمی با حذف تا ۸۵ درصد چربی اضافی است.</p>

<h3>مزایای سرخ‌کن بدون روغن ساپر مدل 1710</h3>
<ul>
<li><strong>ظرفیت فوق‌العاده ۷.۲ لیتر:</strong> مناسب برای خانواده‌های پرجمعیت و پخت همزمان مرغ درسته، کیک، پیتزا و انواع اسنک.</li>
<li><strong>گردش هوای پرسرعت Rapid Air:</strong> سیستم کانوکشن پیشرفته هوای داغ را به طور همگن در سرتاسر محفظه به گردش درمی‌آورد تا بدون نیاز به غوطه‌ور کردن در روغن، غذایی طلایی و آبدار تحویل بگیرید.</li>
<li><strong>سبد تفلون نچسب جداشونده:</strong> شستشوی سریع بدون چسبیدن مواد غذایی و سازگار با ماشین ظرفشویی.</li>
<li><strong>تایمر و ترموستات قابل‌تنظیم:</strong> قابلیت تعیین دقیق دما تا ۲۰۰ درجه سانتی‌گراد متناسب با دستور پخت‌های گوناگون.</li>
</ul>

<h2>جدول مشخصات فنی سرخ‌کن بدون روغن ساپر 7.2 لیتر مدل SAF-1710</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">ساپر (Saper)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">SAF-1710</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">سرخ‌کن بدون روغن / رژیمی (Air Fryer)</td></tr>
<tr><td style="padding: 8px;"><strong>ظرفیت مخزن</strong></td><td style="padding: 8px;">۷.۲ لیتر</td></tr>
<tr><td style="padding: 8px;"><strong>پوشش کاسه</strong></td><td style="padding: 8px;">تفلون نچسب ضدخش</td></tr>
<tr><td style="padding: 8px;"><strong>قابلیت تنظیم دما</strong></td><td style="padding: 8px;">۸۰ تا ۲۰۰ درجه سانتی‌گراد</td></tr>
<tr><td style="padding: 8px;"><strong>ضمانت</strong></td><td style="padding: 8px;">تضمین اصالت کالا توسط فروشگاه حسینی اهواز</td></tr>
</tbody>
</table>

<p>جهت تهیه و ثبت سفارش این سرخ‌کن رژیمی به <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> مراجعه نمایید.</p>"""

    payload = {
        'name': 'سرخ‌کن بدون روغن ساپر 7.2 لیتر مدل SAF-1710',
        'slug': 'saper-saf1710-air-fryer-7-2l',
        'categories': [{'id': 121}, {'id': 216}],
        'short_description': short_desc,
        'description': desc
    }

    r = requests.put(f'{WC_URL}/4095', auth=AUTH, headers=HEADERS, json=payload, timeout=20)
    if r.status_code == 200:
        print("   ✓ محصول ۴۰۹۵ با موفقیت به‌روزرسانی شد.")
        print(f"     نام: {r.json()['name']} | اسلاگ: {r.json()['slug']}")
    else:
        print(f"   ❌ خطا در به‌روزرسانی ۴۰۹۵: {r.status_code} - {r.text}")


def update_product_3494():
    print("\n=== ۳. به‌روزرسانی محصول ۳۴۹۴ (شیور شارژی ۵ کاره پرومارون) ===")
    short_desc = """<ul>
<li><strong>کاربرد:</strong> ست اصلاح و شیور شارژی ۵ کاره حرفه‌ای صورت و بدن</li>
<li><strong>سری‌ها:</strong> سری شیور اصلاح فویلی ضدحساسیت، سری تریمر موزن، سوهان پدیکور پا، برس پاکسازی پوست و سری ماساژور</li>
<li><strong>طراحی و استاندارد:</strong> بدنه ارگونومیک ۱۰۰٪ ضدآب (قابلیت استفاده خشک و مرطوب زیر دوش)</li>
<li><strong>باتری:</strong> باتری لیتیومی شارژی با شارژدهی بالا و چراغ هوشمند LED برای دیدن ریزترین موها</li>
<li><strong>ضمانت و اصالت:</strong> تضمین اصالت و سلامت کالا در فروشگاه لوازم خانگی حسینی اهواز</li>
</ul>"""

    desc = """<h2>بررسی تخصصی و راهنمای خرید شیور و ماشین اصلاح ۵ کاره پرومارون مدل RL-614 ضدآب</h2>
<p>آراستگی روزمره و پیرایش بهداشتی صورت و بدن نیازمند ابزاری چندمنظوره، دقیق و ایمن است که بدون ایجاد سوزش، قرمزی یا خراش روی پوست، نتایجی حرفه‌ای به ارمغان آورد. <strong>شیور و ماشین اصلاح شارژی ۵ کاره پرومارون مدل RL-614 ضدآب</strong> ساخت برند معتبر <strong>پرومارون (Promaron)</strong>، یک پکیج جامع پیرایش است که نیاز شما به سالن‌های زیبایی را به طور کامل برطرف می‌سازد.</p>

<h3>امکانات و قابلیت‌های شیور ۵ کاره پرومارون مدل 614</h3>
<ul>
<li><strong>سری شیور فویلی تیتانیومی:</strong> اصلاحی یکدست، روان و بدون ایجاد التهاب پوستی را برای تمامی نقاط حساس بدن فراهم می‌سازد.</li>
<li><strong>سری تریمر و موکن دقیق:</strong> کوتاه کردن و اصلاح خطوط ظریف با بالاترین دقت.</li>
<li><strong>ضدآب کامل (IPX):</strong> قابلیت استفاده در حمام، شستشوی مستقیم دستگاه زیر شیر آب و سازگاری با فوم یا ژل اصلاح.</li>
<li><strong>سری سوهان غلتکی و براش صورت:</strong> لایه‌برداری ملایم از پاشنه پا و پاکسازی عمیق منافذ پوست صورت.</li>
<li><strong>چراغ روشنایی LED:</strong> متمرکز بر ناحیه اصلاح تا هیچ تار موی باریکی از دید پنهان نماند.</li>
</ul>

<h2>جدول مشخصات فنی شیور شارژی ۵ کاره پرومارون مدل RL-614</h2>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px;" border="1">
<tbody>
<tr><td style="padding: 8px; width: 35%;"><strong>برند</strong></td><td style="padding: 8px;">پرومارون (Promaron)</td></tr>
<tr><td style="padding: 8px;"><strong>مدل</strong></td><td style="padding: 8px;">RL-614</td></tr>
<tr><td style="padding: 8px;"><strong>نوع دستگاه</strong></td><td style="padding: 8px;">شیور و ماشین اصلاح ۵ کاره شارژی</td></tr>
<tr><td style="padding: 8px;"><strong>منبع تغذیه</strong></td><td style="padding: 8px;">باتری لیتیومی قابل شارژ</td></tr>
<tr><td style="padding: 8px;"><strong>مقاومت در برابر آب</strong></td><td style="padding: 8px;">بله (ضدآب و قابل شستشو)</td></tr>
<tr><td style="padding: 8px;"><strong>تعداد سری‌ها</strong></td><td style="padding: 8px;">۵ سری کاربردی مجزا</td></tr>
<tr><td style="padding: 8px;"><strong>گارانتی</strong></td><td style="padding: 8px;">ضمانت اصالت و سلامت از فروشگاه لوازم خانگی حسینی</td></tr>
</tbody>
</table>

<p>شما می‌توانید این کالا را با ضمانت اصالت و سلامت فیزیکی از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> تهیه فرموده یا جهت خرید حضوری به شعب ما در <strong>اهواز</strong> مراجعه نمایید.</p>"""

    payload = {
        'name': 'شیور و ماشین اصلاح ۵ کاره پرومارون مدل RL-614 ضدآب',
        'slug': 'promaron-rl614-shaver-grooming-kit',
        'categories': [{'id': 212}, {'id': 126}],
        'short_description': short_desc,
        'description': desc
    }

    r = requests.put(f'{WC_URL}/3494', auth=AUTH, headers=HEADERS, json=payload, timeout=20)
    if r.status_code == 200:
        print("   ✓ محصول ۳۴۹۴ با موفقیت به‌روزرسانی شد.")
        print(f"     نام: {r.json()['name']} | اسلاگ: {r.json()['slug']}")
    else:
        print(f"   ❌ خطا در به‌روزرسانی ۳۴۹۴: {r.status_code} - {r.text}")


def update_pakizan_products():
    print("\n=== ۴. به‌روزرسانی پتوشور پاکیزان (موجودی و قیمت ۲۸ م با ۵٪ تخفیف) ===")
    reg_price = '28000000' # ۲۸ میلیون تومان
    sale_price = '26600000' # ۲۶.۶ میلیون تومان (۵٪ تخفیف)

    # الف) محصول ساده ۳۷۰۹
    payload_3709 = {
        'manage_stock': False,
        'stock_status': 'instock',
        'regular_price': reg_price,
        'sale_price': sale_price
    }
    r1 = requests.put(f'{WC_URL}/3709', auth=AUTH, headers=HEADERS, json=payload_3709, timeout=20)
    if r1.status_code == 200:
        d1 = r1.json()
        print(f"   ✓ محصول ۳۷۰۹ موجود شد | قیمت عادی: {d1.get('regular_price')} | قیمت حراج: {d1.get('sale_price')} | موجودی: {d1.get('stock_status')}")
    else:
        print(f"   ❌ خطا در به‌روزرسانی ۳۷۰۹: {r1.status_code} - {r1.text}")

    # ب) والد متغیر ۴۰۶۸
    payload_4068 = {
        'manage_stock': False,
        'stock_status': 'instock'
    }
    r2 = requests.put(f'{WC_URL}/4068', auth=AUTH, headers=HEADERS, json=payload_4068, timeout=20)
    if r2.status_code == 200:
        print(f"   ✓ والد ۴۰۶۸ موجود شد | موجودی: {r2.json().get('stock_status')}")
    else:
        print(f"   ❌ خطا در به‌روزرسانی ۴۰۶۸: {r2.status_code}")

    # ج) تنوع‌های ۴۰۶۹ (۳۰ کیلو) و ۴۰۷۰ (۴۰ کیلو)
    for vid in [4069, 4070]:
        payload_var = {
            'manage_stock': False,
            'stock_status': 'instock',
            'regular_price': reg_price,
            'sale_price': sale_price
        }
        r_var = requests.put(f'{WC_URL}/4068/variations/{vid}', auth=AUTH, headers=HEADERS, json=payload_var, timeout=20)
        if r_var.status_code == 200:
            dv = r_var.json()
            print(f"   ✓ تنوع {vid} موجود شد | قیمت عادی: {dv.get('regular_price')} | قیمت حراج: {dv.get('sale_price')} | موجودی: {dv.get('stock_status')}")
        else:
            print(f"   ❌ خطا در به‌روزرسانی تنوع {vid}: {r_var.status_code} - {r_var.text}")

if __name__ == '__main__':
    update_product_3626()
    update_product_4095()
    update_product_3494()
    update_pakizan_products()
    print("\n✅ به‌روزرسانی‌های وب‌سایت با موفقیت به پایان رسید.")
