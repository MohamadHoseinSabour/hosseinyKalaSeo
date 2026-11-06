import os
import sys
import json
import shutil

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEW_PRODS_DIR = os.path.join(PROJECT_DIR, 'data', 'new_products')

# Product 1: Candy KCV-325 G
slug_candy = "candy-kcv-325-g-vacuum-cleaner"
dir_candy = os.path.join(NEW_PRODS_DIR, slug_candy)
os.makedirs(os.path.join(dir_candy, 'images'), exist_ok=True)
shutil.copy2('scratch/new_2_prods/candy_featured.webp', os.path.join(dir_candy, 'images', 'featured.webp'))

candy_short_desc = """<ul>
  <li><strong>توان پرقدرت ۲۵۰۰ وات سوپر سایلنت:</strong> مکش قدرتمند برای انواع فرش‌های ضخیم، موکت و سرامیک با کمترین تولید صدا</li>
  <li><strong>مخزن جادار سایز XXL (۶ لیتر):</strong> ظرفیت بسیار بالا جهت کاهش دفعات تخلیه و سازگاری با پاکت‌های PowerProtect ضد نشت</li>
  <li><strong>فیلتر بهداشتی قابل شست‌وشوی ضد آلرژی (HEPA):</strong> تصفیه کامل هوای خروجی و حذف گرد و غبار معلق؛ ایده‌آل برای کودکان و افراد دارای حساسیت</li>
  <li><strong>شعاع عملکرد گسترده ۱۵ متر:</strong> کابل برق بلند، لوله تلسکوپی ارگونومیک و ۴ چرخ روان ۳۶۰ درجه با ضربه‌گیر محافظ مبلمان (AirBumper)</li>
  <li><strong>سنسور الکترونیکی نشانگر پر بودن کیسه:</strong> جلوگیری از افت مکش و محافظت از سلامت موتور در درازمدت</li>
</ul>"""

candy_desc = """<p>اگر برای نظافت روزمره خانه به دنبال دستگاهی با توان مکش فوق‌العاده، صدای کنترل‌شده و دوام بالا در دسته <a href="https://hosseinykala.ir/product-category/washing-cleaning/%d8%ac%d8%a7%d8%b1%d9%88%d8%a8%d8%b1%d9%82%db%8c/">جاروبرقی</a> هستید، <strong>جاروبرقی کیسه ای 2500 وات کندی مدل KCV-325 G</strong> یکی از مطمئن‌ترین انتخاب‌ها است. برند معتبر کندی (Candy) تحت نظارت فنی و خدمات پس از فروش گسترده گروه صنعتی پاکشوما، این محصول را با بالاترین کیفیت قطعات و استانداردهای روز اروپا روانه بازار کرده است.</p>

<h3>ویژگی‌ها و مزایای برجسته جاروبرقی کندی مدل KCV-325 G</h3>
<ul>
  <li><strong>موتور پرقدرت ۲۵۰۰ وات:</strong> تضمین نظافت عمیق پرزهای فرش و شیارهای سرامیک حتی از ریزترین ذرات خاک و موی حیوانات خانگی.</li>
  <li><strong>طراحی فوق کم‌صدا (Super Silent):</strong> عایق‌بندی مهندسی‌شده محفظه موتور که کارکردی ملایم و آرام با میزان صدای حدود ۶۵ دسی‌بل را فراهم می‌آورد.</li>
  <li><strong>فیلتر ضد آلرژی هپا:</strong> با فیلتراسیون هوای خروجی، از بازگشت ذرات میکرونی آلرژی‌زا به فضای منزل جلوگیری می‌کند.</li>
  <li><strong>کیسه بزرگ ۶ لیتری با دوام:</strong> آزادی عمل در استفاده از پاکت‌های دائمی قابل شست‌وشو یا پاکت‌های یک‌بار مصرف استاندارد Type G.</li>
  <li><strong>نوار محافظ ضربه‌گیر AirBumper:</strong> لایه محافظ نرم پیرامون بدنه که از خط افتادن روی مبلمان و پایه‌های چوبی هنگام حرکت سریع جلوگیری می‌کند.</li>
</ul>

<h3>مشخصات فنی جاروبرقی ۲۵۰۰ وات کندی مدل KCV-325 G</h3>
<table style='width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px;'>
  <tbody>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9; width: 35%;'>برند</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>کندی (Candy) / ضمانت پاکشوما</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>مدل</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>KCV-325 G (یا KCV 325)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>نوع دستگاه</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>جاروبرقی کیسه‌ای خانگی</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>توان موتور</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>۲۵۰۰ وات</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>میزان صدا</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>سوپر سایلنت (حدود ۶۵ دسی‌بل)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>گنجایش مخزن کیسه</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>۶ لیتر (سایز XXL)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>نوع فیلتر خروجی</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>فیلتر بهداشتی قابل شست‌وشو ضد حساسیت (HEPA)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>شعاع عملکرد</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>۱۵ متر</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>نشانگر پر بودن کیسه</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>دارد (الکترونیکی)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>تنظیم الکترونیکی توان مکش</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>دارد (ولومی روی بدنه)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>رنگ بدنه</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>خاکستری روشن / طوسی (Light Grey)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>اقلام همراه</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>سری پارویی فرش و پارکت، نازل گوشه‌گیر باریک، برس مبلمان</td></tr>
  </tbody>
</table>

<h3>خرید حضوری و اینترنتی از فروشگاه حسینی</h3>
<p>شما می‌توانید <strong>جاروبرقی کیسه ای 2500 وات کندی مدل KCV-325 G</strong> را با ضمانت اصالت کالا و گارانتی رسمی پاک‌سرویس از <strong><a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a></strong> تهیه کنید. فروشگاه حسینی با سابقه درخشان و شعب حضوری در شهر <strong>اهواز</strong>، امکان خرید حضوری و همچنین ارسال سریع و مطمئن به سراسر استان خوزستان و سراسر ایران را برای مشتریان گرامی فراهم کرده است.</p>"""

info_candy = {
    "id_key": "candy_kcv_325_g",
    "raw_title": "جاروبرقی کندی KCV 325 G",
    "name": "جاروبرقی کیسه ای 2500 وات کندی مدل KCV-325 G",
    "slug": slug_candy,
    "brand_fa": "کندی",
    "brand_en": "Candy",
    "category_id": 21,
    "category_slug": "vacuum-cleaner",
    "subcat_id": 21,
    "model": "KCV-325 G",
    "qty": 0,
    "stock_status": "outofstock",
    "focus_keyword": "جاروبرقی کندی KCV 325",
    "meta_description": "خرید جاروبرقی ۲۵۰۰ وات کندی مدل KCV-325 G با موتور سوپر سایلنت، کیسه ۶ لیتری XXL و فیلتر هپا با گارانتی پاک سرویس از فروشگاه لوازم خانگی حسینی اهواز.",
    "tags": [
        "جاروبرقی کندی",
        "جاروبرقی کندی KCV 325",
        "جاروبرقی ۲۵۰۰ وات",
        "جاروبرقی پاکشوما",
        "جاروبرقی سوپر سایلنت"
    ],
    "short_description": candy_short_desc,
    "description": candy_desc,
    "attributes": [
        {"name": "برند", "visible": True, "options": ["کندی (Candy)"]},
        {"name": "مدل", "visible": True, "options": ["KCV-325 G"]},
        {"name": "توان موتور", "visible": True, "options": ["۲۵۰۰ وات"]},
        {"name": "نوع جاروبرقی", "visible": True, "options": ["کیسه‌ای"]},
        {"name": "گنجایش مخزن", "visible": True, "options": ["۶ لیتر"]},
        {"name": "فیلتر بهداشتی", "visible": True, "options": ["فیلتر هپا (HEPA) قابل شست‌وشو"]},
        {"name": "شعاع عملکرد", "visible": True, "options": ["۱۵ متر"]},
        {"name": "رنگ", "visible": True, "options": ["طوسی / خاکستری"]}
    ],
    "images": ["images/featured.webp"],
    "wc_category_ids": [21, 239],
    "wc_category_name": "جاروبرقی",
    "wc_canonical_url": "https://hosseinykala.ir/product-category/washing-cleaning/%d8%ac%d8%a7%d8%b1%d9%88%d8%a8%d8%b1%d9%82%db%8c/"
}

with open(os.path.join(dir_candy, 'info.json'), 'w', encoding='utf-8') as f:
    json.dump(info_candy, f, ensure_ascii=False, indent=2)

with open(os.path.join(dir_candy, 'content.md'), 'w', encoding='utf-8') as f:
    f.write(candy_desc)

print("✓ پوشه و فایل‌های جاروبرقی کندی آماده شد.")


# Product 2: Olive OL-43FSS30 43-inch Smart TV
slug_olive = "olive-43-inch-ol-43fss30-smart-tv"
dir_olive = os.path.join(NEW_PRODS_DIR, slug_olive)
os.makedirs(os.path.join(dir_olive, 'images'), exist_ok=True)
shutil.copy2('scratch/new_2_prods/olive_featured.webp', os.path.join(dir_olive, 'images', 'featured.webp'))

olive_short_desc = """<ul>
  <li><strong>صفحه نمایش ۴۳ اینچ Full HD:</strong> وضوح تصویر ۱۹۲۰×۱۰۸۰ با پنل گرید A و زاویه دید گسترده ۱۷۸ درجه برای نمایش طبیعی‌ترین رنگ‌ها</li>
  <li><strong>سیستم‌عامل هوشمند اندروید ۱۴ (Android 14):</strong> دسترسی آسان و سریع به تمامی اپلیکیشن‌های پخش فیلم، بازی و شبکه‌های اجتماعی + اشتراک رایگان فیلیمو</li>
  <li><strong>سیستم صوتی استریو دالبی (Dolby Digital Plus):</strong> خروجی صدای شفاف، فراگیر و سینمایی متناسب با ابعاد سالن و اتاق</li>
  <li><strong>گیرنده دیجیتال داخلی پیشرفته DVB-T2 با کدک HEVC:</strong> دریافت کامل شبکه‌های تلویزیونی با کیفیت HD بدون نیاز به دستگاه ستاپ‌باکس جانبی</li>
  <li><strong>اتصال هوشمند بی‌سیم (Wi-Fi و Miracast):</strong> انتقال آنی تصویر، ویدیو و بازی‌های گوشی همراه روی نمایشگر بزرگ تلویزیون</li>
  <li><strong>درگاه‌های کامل HDMI و USB:</strong> امکان ضبط برنامه‌ها (PVR) و استفاده از قابلیت ماشین زمان (Time Shift) روی حافظه جانبی</li>
</ul>"""

olive_desc = """<p>اگر برای سالن پذیرایی، اتاق نشیمن یا محیط کار خود به دنبال تلویزیونی هوشمند، شیک و مجهز به جدیدترین فناوری‌های تصویری در دسته <a href="https://hosseinykala.ir/product-category/audio-video/television/">تلویزیون</a> هستید، <strong>تلویزیون هوشمند 43 اینچ الیو مدل OL-43FSS30 اندروید 14</strong> یکی از بهترین انتخاب‌های بازار به شمار می‌رود. برند خوش‌نام الیو (Olive) با ضمانت معتبر ۲۴ ماهه شرکت آسال سرویس، این محصول را با بهره‌گیری از پنل‌های باکیفیت و رابط کاربری مدرن اندروید به بازار عرضه کرده است.</p>

<h3>ویژگی‌ها و مزایای برجسته تلویزیون هوشمند الیو مدل OL-43FSS30</h3>
<ul>
  <li><strong>رزولوشن Full HD با وضوح تصویر بالا:</strong> تماشای فیلم‌ها و مسابقات ورزشی با جزئیات دقیق، کنتراست پویا و روشنایی متعادل.</li>
  <li><strong>رابط کاربری هوشمند Android 14:</strong> دسترسی به دنیای بی‌انتهای برنامه‌های اندرویدی، مرور وب، پلتفرم‌های تماشای آنلاین فیلم (همراه با اشتراک فیلیمو) و کنترل صوتی.</li>
  <li><strong>صدای شفاف دالبی (Dolby Audio):</strong> تفکیک صوتی فراگیر و مکالمات واضح در فیلم‌ها و موسیقی.</li>
  <li><strong>فناوری اشتراک هوشمند صفحه گوشی (Screen Mirroring):</strong> پخش لحظه‌ای عکس‌ها، ویدیوها و اسلایدهای کاری از گوشی هوشمند به صفحه ۴۳ اینچی تلویزیون بدون نیاز به کابل.</li>
  <li><strong>قابلیت ماشین زمان (Time Shift) و PVR:</strong> امکان توقف زنده برنامه‌های تلویزیونی و ضبط فیلم‌ها و مسابقات زنده روی فلش مموری.</li>
</ul>

<h3>مشخصات فنی تلویزیون ال‌ای‌دی هوشمند ۴۳ اینچ الیو مدل OL-43FSS30</h3>
<table style='width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px;'>
  <tbody>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9; width: 35%;'>برند</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>الیو (OLIVE) / ضمانت آسال سرویس</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>مدل</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>OL-43FSS30 (سری FSS30)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>سایز صفحه نمایش</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>۴۳ اینچ (تکنولوژی LED)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>کیفیت تصویر</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>Full HD (رزولوشن ۱۰۸۰ × ۱۹۲۰)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>سیستم‌عامل</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>اندروید نسخه ۱۴ (Android 14)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>پردازنده و حافظه</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>پردازنده ۴ هسته‌ای (Quad Core) / حافظه داخلی ۸ گیگابایت</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>فناوری صوتی</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>Dolby Digital Plus دو کاناله</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>گیرنده دیجیتال</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>DVB-T2 با پشتیبانی از کدک HEVC و HbbTV</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>اتصالات بی‌سیم</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>وای‌فای (Wi-Fi) و اشتراک بی‌سیم تصویر (Miracast)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>پورت‌های ارتباطی</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>درگاه‌های HDMI، پورت USB، خروجی صوتی دیجیتال اپتیکال، ورودی آنتن</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>طراحی بدنه</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>بدون فریم (Frameless) با پایه‌های شکیل رومیزی و قابلیت نصب روی دیوار</td></tr>
  </tbody>
</table>

<h3>خرید حضوری و اینترنتی از فروشگاه حسینی</h3>
<p>شما می‌توانید <strong>تلویزیون هوشمند 43 اینچ الیو مدل OL-43FSS30 اندروید 14</strong> را با اطمینان از اصالت کالا و گارانتی معتبر شرکتی از <strong><a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a></strong> خریداری فرمایید. فروشگاه حسینی با استقرار شعب حضوری در شهر <strong>اهواز</strong>، آماده ارائه خدمات مشاوره پیش از خرید و ارسال سریع به سراسر خوزستان و تمامی شهرهای کشور می‌باشد.</p>"""

info_olive = {
    "id_key": "olive_43fss30",
    "raw_title": "تلویزیون الیو 43FSS30",
    "name": "تلویزیون هوشمند 43 اینچ الیو مدل OL-43FSS30 اندروید 14",
    "slug": slug_olive,
    "brand_fa": "الیو",
    "brand_en": "Olive",
    "category_id": 243,
    "category_slug": "television",
    "subcat_id": 243,
    "model": "OL-43FSS30",
    "qty": 0,
    "stock_status": "outofstock",
    "focus_keyword": "تلویزیون هوشمند الیو OL-43FSS30",
    "meta_description": "خرید تلویزیون هوشمند ۴۳ اینچ الیو مدل OL-43FSS30 مجهز به اندروید ۱۴، کیفیت Full HD، سیستم صوتی دالبی و گارانتی آسال سرویس از فروشگاه لوازم خانگی حسینی اهواز.",
    "tags": [
        "تلویزیون الیو",
        "تلویزیون هوشمند الیو",
        "تلویزیون ۴۳ اینچ الیو",
        "تلویزیون اندروید ۱۴",
        "تلویزیون OL-43FSS30"
    ],
    "short_description": olive_short_desc,
    "description": olive_desc,
    "attributes": [
        {"name": "برند", "visible": True, "options": ["الیو (OLIVE)"]},
        {"name": "سایز صفحه نمایش", "visible": True, "options": ["۴۳ اینچ"]},
        {"name": "کیفیت تصویر", "visible": True, "options": ["Full HD (1080p)"]},
        {"name": "سیستم‌عامل", "visible": True, "options": ["اندروید ۱۴ (Android 14)"]},
        {"name": "فناوری صوتی", "visible": True, "options": ["Dolby Digital Plus"]},
        {"name": "گیرنده دیجیتال", "visible": True, "options": ["DVB-T2 با پشتیبانی از HEVC"]},
        {"name": "اتصال بی‌سیم", "visible": True, "options": ["وای‌فای (Wi-Fi) و Miracast"]}
    ],
    "images": ["images/featured.webp"],
    "wc_category_ids": [243, 242],
    "wc_category_name": "تلویزیون",
    "wc_canonical_url": "https://hosseinykala.ir/product-category/audio-video/television/"
}

with open(os.path.join(dir_olive, 'info.json'), 'w', encoding='utf-8') as f:
    json.dump(info_olive, f, ensure_ascii=False, indent=2)

with open(os.path.join(dir_olive, 'content.md'), 'w', encoding='utf-8') as f:
    f.write(olive_desc)

print("✓ پوشه و فایل‌های تلویزیون الیو آماده شد.")
