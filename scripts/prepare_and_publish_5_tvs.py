import os
import sys
import json
import time
import shutil
import requests
from requests.auth import HTTPBasicAuth

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEW_PRODS_DIR = os.path.join(PROJECT_DIR, 'data', 'new_products')
PROCESSED_IMG_DIR = os.path.join(PROJECT_DIR, 'scratch', 'new_tvs_processed')
OUTPUT_RESULT = os.path.join(PROJECT_DIR, 'scratch', 'published_5_tvs_result.json')

AUTH = HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
WP_BASE = 'https://hosseinykala.ir'
MEDIA_API = f'{WP_BASE}/wp-json/wp/v2/media'
WC_PRODUCTS_API = f'{WP_BASE}/wp-json/wc/v3/products'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

TVS_DATA = [
    {
        "slug": "xvision-43-inch-43xt515-smart-tv",
        "name": "تلویزیون هوشمند 43 اینچ ال ای دی ایکس ویژن مدل 43XT515",
        "brand_fa": "ایکس ویژن",
        "brand_en": "X-Vision",
        "model": "43XT515",
        "img_file": "xvision-43-inch-43xt515-smart-tv.webp",
        "focus_keyword": "تلویزیون ایکس ویژن 43XT515",
        "meta_description": "خرید تلویزیون هوشمند ۴۳ اینچ ال‌ای‌دی ایکس ویژن مدل 43XT515 مجهز به کیفیت Full HD، سیستم‌عامل اندروید، گیرنده دیجیتال DVB-T2 با گارانتی مادیران از فروشگاه حسینی اهواز.",
        "tags": ["تلویزیون ایکس ویژن", "تلویزیون هوشمند ایکس ویژن", "تلویزیون ۴۳ اینچ ایکس ویژن", "تلویزیون مادیران", "ایکس ویژن 43XT515"],
        "attributes": [
            {"name": "برند", "visible": True, "options": ["ایکس ویژن (X-Vision)"]},
            {"name": "مدل", "visible": True, "options": ["43XT515"]},
            {"name": "سایز صفحه نمایش", "visible": True, "options": ["۴۳ اینچ"]},
            {"name": "کیفیت تصویر", "visible": True, "options": ["Full HD (1080p)"]},
            {"name": "سیستم‌عامل", "visible": True, "options": ["اندروید هوشمند (Android)"]},
            {"name": "توان صوتی", "visible": True, "options": ["۲۰ وات (دو بلندگوی ۱۰ وات)"]},
            {"name": "گیرنده دیجیتال", "visible": True, "options": ["DVB-T2 با پشتیبانی از HEVC"]},
            {"name": "درگاه‌های ارتباطی", "visible": True, "options": ["HDMI، USB، LAN، Wi-Fi"]}
        ],
        "short_description": """<ul>
  <li><strong>صفحه نمایش ۴۳ اینچ Full HD:</strong> وضوح تصویر ۱۹۲۰×۱۰۸۰ با زاویه دید گسترده ۱۷۸ درجه برای تماشای بدون افت کیفیت از تمام زوایا</li>
  <li><strong>سیستم‌عامل اندروید هوشمند (Smart Android):</strong> امکان نصب انواع برنامه‌های کاربردی، اپلیکیشن‌های پخش آنلاین فیلم، موسیقی و بازی</li>
  <li><strong>سیستم صوتی دو کاناله قدرتمند ۲۰ وات:</strong> بلندگوهای پرقدرت با پشتیبانی از فناوری دالبی دیجیتال برای صدایی تفکیک‌شده و شفاف</li>
  <li><strong>گیرنده دیجیتال داخلی DVB-T2:</strong> دریافت سریع تمامی شبکه‌های دیجیتالی سراسری و استانی بدون نیاز به گیرنده جانبی</li>
  <li><strong>درگاه‌های کامل اتصالی:</strong> مجهز به درگاه‌های ورودی HDMI، پورت USB با قابلیت پخش فیلم، موزیک و عکس و اتصال بی‌سیم Wi-Fi</li>
</ul>""",
        "description": """<p>اگر برای فضاهای مسکونی با ابعاد متوسط، اتاق خواب یا محل کار به دنبال یک تلویزیون باکیفیت و هوشمند در دسته <a href="https://hosseinykala.ir/product-category/audio-video/television/">تلویزیون</a> هستید، <strong>تلویزیون هوشمند 43 اینچ ال ای دی ایکس ویژن مدل 43XT515</strong> یکی از شناخته‌شده‌ترین گزینه‌های بازار ایران به شمار می‌رود. برند نام‌آشنای ایکس‌ویژن تحت پوشش خدمات پس از فروش و ضمانت معتبر شرکت مادیران، همواره گزینه‌ای اقتصادی و مطمئن برای خانواده‌ها بوده است.</p>

<h3>ویژگی‌ها و مزایای برجسته تلویزیون ایکس ویژن مدل 43XT515</h3>
<ul>
  <li><strong>کیفیت تصویر Full HD:</strong> نمایش تصاویر زنده با کنتراست پویا و روشنایی ایده‌آل برای مشاهده مسابقات ورزشی و فیلم‌های سینمایی.</li>
  <li><strong>محیط هوشمند اندرویدی:</strong> رابط کاربری کاربرپسند برای وبگردی، مشاهده آنلاین سریال‌ها و استفاده از نرم‌افزارهای اشتراک تصویر.</li>
  <li><strong>ماشین زمان (Time Shift) و ضبط برنامه (PVR):</strong> ثبت و ضبط برنامه‌های زنده تلویزیونی روی فلش مموری برای مشاهده مجدد.</li>
  <li><strong>طراحی مدرن و باریک:</strong> قاب مشکی شکیل همراه با پایه‌های مقاوم رومیزی و قابلیت نصب دیواری با براکت استاندارد VESA.</li>
</ul>

<h3>مشخصات فنی تلویزیون هوشمند ۴۳ اینچ ایکس ویژن مدل 43XT515</h3>
<table style='width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px;'>
  <tbody>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9; width: 35%;'>برند</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>ایکس ویژن (X-Vision) / گارانتی مادیران</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>مدل</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>43XT515</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>سایز صفحه نمایش</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>۴۳ اینچ (تکنولوژی D-LED)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>کیفیت تصویر</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>Full HD (۱۹۲۰ × ۱۰۸۰ پیکسل)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>سیستم‌عامل</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>اندروید هوشمند (Android)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>توان سیستم صوتی</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>۲۰ وات (دو کاناله ۱۰ وات دالبی)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>گیرنده دیجیتال</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>DVB-T2 با پشتیبانی از کدک‌های جدید</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>پورت‌های ارتباطی</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>۲ عدد HDMI، ۲ عدد USB، ورودی کامپوزیت، پورت LAN و خروجی صوتی اپتیکال</td></tr>
  </tbody>
</table>

<h3>خرید حضوری و اینترنتی از فروشگاه حسینی</h3>
<p>شما می‌توانید <strong>تلویزیون هوشمند 43 اینچ ال ای دی ایکس ویژن مدل 43XT515</strong> را با تضمین اصالت فیزیکی و قطعات اصلی از <strong><a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a></strong> تهیه کنید. فروشگاه حسینی با داشتن شعب حضوری در شهر <strong>اهواز</strong>، خریدی آسوده همراه با ارسال سریع و بسته‌بندی ایمن به سراسر خوزستان و سراسر کشور را برای هموطنان فراهم می‌سازد.</p>"""
    },
    {
        "slug": "toshiba-50-inch-50l2300ee-led-tv",
        "name": "تلویزیون 50 اینچ ال ای دی توشیبا مدل 50L2300EE",
        "brand_fa": "توشیبا",
        "brand_en": "Toshiba",
        "model": "50L2300EE",
        "img_file": "toshiba-50-inch-50l2300ee-led-tv.webp",
        "focus_keyword": "تلویزیون توشیبا 50L2300EE",
        "meta_description": "خرید تلویزیون ۵۰ اینچ ال ای دی توشیبا مدل 50L2300EE با موتور پردازش تصویر REGZA، کیفیت Full HD، نرخ نوسازی ClearScan و پنل بادوام ژاپنی از فروشگاه حسینی اهواز.",
        "tags": ["تلویزیون توشیبا", "تلویزیون ۵۰ اینچ توشیبا", "تلویزیون Full HD توشیبا", "توشیبا 50L2300EE", "موتور تصویر REGZA"],
        "attributes": [
            {"name": "برند", "visible": True, "options": ["توشیبا (Toshiba)"]},
            {"name": "مدل", "visible": True, "options": ["50L2300EE"]},
            {"name": "سایز صفحه نمایش", "visible": True, "options": ["۵۰ اینچ"]},
            {"name": "کیفیت تصویر", "visible": True, "options": ["Full HD (1080p)"]},
            {"name": "موتور پردازش تصویر", "visible": True, "options": ["REGZA Engine"]},
            {"name": "نرخ به‌روزرسانی", "visible": True, "options": ["ClearScan 100Hz"]},
            {"name": "توان خروجی صدا", "visible": True, "options": ["۲۰ وات (Power Bass Booster)"]},
            {"name": "درگاه‌های ورودی", "visible": True, "options": ["HDMI، پورت USB، کامپوننت و کامپوزیت"]}
        ],
        "short_description": """<ul>
  <li><strong>صفحه نمایش ۵۰ اینچ عریض Full HD:</strong> رزولوشن ۱۰۸۰×۱۹۲۰ با نور پس‌زمینه مستقیم Direct LED برای روشنایی یکدست صفحه</li>
  <li><strong>موتور پردازش تصویر انحصاری REGZA Engine:</strong> بهینه‌سازی خودکار وضوح، کنتراست پویا و زنده کردن رنگ‌ها با عمق رنگ ۱۰ بیتی</li>
  <li><strong>فناوری حرکت روان ClearScan 100Hz:</strong> جلوگیری از تاری و بریدگی تصویر در صحنه‌های پرتحرک اکشن و بازی‌های ورزشی</li>
  <li><strong>سیستم صوتی مجهز به Power Bass Booster:</strong> بیس عمیق و تفکیک عالی صدا در گفتگوهای فیلم‌ها بدون افت کیفیت</li>
  <li><strong>درگاه‌های کاربردی HDMI و پورت USB:</strong> اتصال آسان انواع گیرنده‌ها، کنسول بازی و پخش فایل‌های چندرسانه‌ای از روی حافظه جانبی</li>
</ul>""",
        "description": """<p>اگر اصالت تصویر، ماندگاری قطعات ژاپنی و کیفیت ساخت بالا برای شما اولویت دارد، <strong>تلویزیون 50 اینچ ال ای دی توشیبا مدل 50L2300EE</strong> در دسته <a href="https://hosseinykala.ir/product-category/audio-video/television/">تلویزیون</a> گزینه‌ای برجسته و بی‌رقیب است. شرکت معتبر توشیبا با بهره‌گیری از موتور پردازش تصویر شهیر REGZA، کیفیتی پایدار و درخشان را برای سال‌ها استفاده بی‌دغدغه تضمین می‌کند.</p>

<h3>ویژگی‌ها و مزایای برجسته تلویزیون توشیبا مدل 50L2300EE</h3>
<ul>
  <li><strong>موتور اختصاصی REGZA Engine:</strong> تفکیک و پردازش پیکسل به پیکسل تصاویر برای ارائه واقعی‌ترین پالت رنگی و حذف نویزهای تصویر.</li>
  <li><strong>تکنولوژی ClearScan:</strong> رفرش‌ریت بالای پنل که تماشای فوتبال و فیلم‌های پرسرعت را بدون تار شدن یا جا ماندن سایه لذت‌بخش می‌سازد.</li>
  <li><strong>پایداری و طول عمر قطعات:</strong> استفاده از مادربرد و پنل صنعتی مقاوم در برابر نوسانات برق و کارکرد طولانی‌مدت.</li>
  <li><strong>طراحی باوقار با پایه مستطیلی:</strong> زیبایی کلاسیک و هماهنگ با دکوراسیون هر نوع منزل و محیط کار.</li>
</ul>

<h3>مشخصات فنی تلویزیون ۵۰ اینچ ال ای دی توشیبا مدل 50L2300EE</h3>
<table style='width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px;'>
  <tbody>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9; width: 35%;'>برند</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>توشیبا (Toshiba)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>مدل</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>50L2300EE</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>سایز صفحه نمایش</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>۵۰ اینچ (Direct LED)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>کیفیت تصویر</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>Full HD (۱۹۲۰ × ۱۰۸۰)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>موتور پردازش تصویر</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>REGZA Engine با عمق ۱۰ بیتی</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>فناوری حرکت تصویر</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>ClearScan 100Hz / 120Hz</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>سیستم صوتی</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>۲۰ وات استریو با تقویت‌کننده Bass Booster</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>درگاه‌های اتصالی</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>درگاه‌های HDMI، پورت USB، ورودی کامپوننت و کامپوزیت AV</td></tr>
  </tbody>
</table>

<h3>خرید حضوری و اینترنتی از فروشگاه حسینی</h3>
<p>شما می‌توانید <strong>تلویزیون 50 اینچ ال ای دی توشیبا مدل 50L2300EE</strong> را با اطمینان از اصالت دستگاه از <strong><a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a></strong> خریداری فرمایید. فروشگاه حسینی در شهر <strong>اهواز</strong> امکان بازدید حضوری و ارسال سریع و مطمئن به تمامی شهرستان‌های استان خوزستان و سراسر ایران را برای مشتریان فراهم آورده است.</p>"""
    },
    {
        "slug": "toshiba-55-inch-4k-smart-led-tv",
        "name": "تلویزیون 55 اینچ ال ای دی هوشمند 4K توشیبا مدل 55C350RP",
        "brand_fa": "توشیبا",
        "brand_en": "Toshiba",
        "model": "55C350RP",
        "img_file": "toshiba-55-inch-4k-smart-led-tv.webp",
        "focus_keyword": "تلویزیون توشیبا 55C350RP",
        "meta_description": "خرید تلویزیون ۵۵ اینچ ال ای دی هوشمند 4K توشیبا مدل 55C350RP مجهز به پردازشگر هوشمند REGZA، پشتیبانی از Dolby Vision، سیستم صوتی دالبی اتموس و گارانتی معتبر از فروشگاه حسینی اهواز.",
        "tags": ["تلویزیون توشیبا", "تلویزیون ۵۵ اینچ توشیبا", "تلویزیون 4K توشیبا", "توشیبا 55C350RP", "تلویزیون هوشمند توشیبا"],
        "attributes": [
            {"name": "برند", "visible": True, "options": ["توشیبا (Toshiba)"]},
            {"name": "مدل", "visible": True, "options": ["55C350RP"]},
            {"name": "سایز صفحه نمایش", "visible": True, "options": ["۵۵ اینچ"]},
            {"name": "کیفیت تصویر", "visible": True, "options": ["4K Ultra HD (2160p)"]},
            {"name": "پردازنده تصویر", "visible": True, "options": ["REGZA Engine 4K"]},
            {"name": "فناوری تصویر", "visible": True, "options": ["Dolby Vision و HDR10"]},
            {"name": "سیستم صوتی", "visible": True, "options": ["Dolby Atmos و DTS Virtual:X"]},
            {"name": "سیستم‌عامل", "visible": True, "options": ["سیستم هوشمند VIDAA"]}
        ],
        "short_description": """<ul>
  <li><strong>صفحه نمایش ۵۵ اینچ 4K Ultra HD:</strong> رزولوشن خارق‌العاده ۲۱۶۰×۳۸۴۰ پیکسل با بیش از ۸.۳ میلیون پیکسل برای نمایش خیره‌کننده جزئیات</li>
  <li><strong>پردازشگر اختصاصی هوشمند REGZA Engine 4K:</strong> ارتقای هوشمند محتواهای با کیفیت پایین‌تر (4K Upscaling) به وضوح نزدیک به فورکی</li>
  <li><strong>فناوری‌های سینمایی Dolby Vision و HDR10:</strong> بازتولید طیف وسیع رنگی، تاریکی‌های مطلق و روشنایی‌های درخشان با عمق رنگ ۱۰ بیتی</li>
  <li><strong>سیستم صوتی سه‌بعدی Dolby Atmos:</strong> صدای فراگیر و همه‌جانبه متناسب با ابعاد سالن برای خلق تجربه سینمایی در خانه</li>
  <li><strong>طراحی بدون حاشیه (Bezel-less):</strong> نسبت صفحه نمایش به بدنه حداکثری و قاب مینیمال فوق‌العاده مدرن</li>
  <li><strong>امکانات ارتباطی سریع:</strong> ۳ پورت HDMI، ۲ پورت USB، بلوتوث نسخه ۵ و اتصال بی‌سیم وای‌فای دوبانده</li>
</ul>""",
        "description": """<p>برای تجربه سینمای خانگی با بالاترین کیفیت تصویر در دسته <a href="https://hosseinykala.ir/product-category/audio-video/television/">تلویزیون</a>، <strong>تلویزیون 55 اینچ ال ای دی هوشمند 4K توشیبا مدل 55C350RP</strong> انتخابی مدرن و درخشان است. توشیبا با تلفیق هنر مهندسی ژاپنی و فناوری‌های پیشرفته Dolby Vision و پردازشگر REGZA 4K، تصاویری تماشایی و صدای سینمایی فراگیر را به خانه شما می‌آورد.</p>

<h3>ویژگی‌ها و مزایای برجسته تلویزیون ۵۵ اینچ فورکی توشیبا مدل 55C350RP</h3>
<ul>
  <li><strong>رزولوشن خیره‌کننده 4K:</strong> شفافیت ۴ برابری نسبت به Full HD با تفکیک عمیق رنگ‌ها و بافت‌ها.</li>
  <li><strong>ارتقا دهنده هوشمند تصویر (AI 4K Upscaler):</strong> بازسازی و ارتقای شفافیت شبکه‌های تلویزیونی معمولی به کیفیتی نزدیک به 4K.</li>
  <li><strong>صدای چندبعدی دالبی اتموس:</strong> غوطه‌وری در فیلم‌ها و موسیقی با صدای استریوی فراگیر و بیس کنترل‌شده.</li>
  <li><strong>رابط هوشمند و سریع VIDAA:</strong> دسترسی آنی به اپلیکیشن‌های بین‌المللی و داخلی تماشای فیلم با سرعت لودینگ فوق‌العاده بالا.</li>
  <li><strong>قاب بی‌نهایت باریک:</strong> طراحی فریم‌لس که تمام تمرکز بیننده را روی قاب تصویر معطوف نگه می‌دارد.</li>
</ul>

<h3>مشخصات فنی تلویزیون ۵۵ اینچ ال ای دی هوشمند 4K توشیبا</h3>
<table style='width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px;'>
  <tbody>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9; width: 35%;'>برند</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>توشیبا (Toshiba)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>مدل</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>55C350RP</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>سایز صفحه نمایش</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>۵۵ اینچ (پنل DLED گرید A)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>کیفیت تصویر</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>4K Ultra HD (۲۱۶۰ × ۳۸۴۰ پیکسل)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>پردازنده تصویر</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>REGZA Engine 4K با فناوری هوش مصنوعی</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>استانداردهای HDR</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>Dolby Vision، HDR10 و HLG</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>فناوری‌های صوتی</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>Dolby Atmos و DTS Virtual:X</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>سیستم‌عامل</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>سیستم هوشمند اختصاصی VIDAA</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>درگاه‌های اتصالی</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>۳ درگاه HDMI (پشتیبانی از eARC)، ۲ درگاه USB، وای‌فای، بلوتوث و خروجی اپتیکال</td></tr>
  </tbody>
</table>

<h3>خرید حضوری و اینترنتی از فروشگاه حسینی</h3>
<p>شما می‌توانید <strong>تلویزیون 55 اینچ ال ای دی هوشمند 4K توشیبا مدل 55C350RP</strong> را با گارانتی معتبر و تضمین اصالت فیزیکی کالا از <strong><a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a></strong> خریداری فرمایید. فروشگاه حسینی با استقرار شعب در شهر <strong>اهواز</strong>، خدمات ارسال سریع، بسته‌بندی مطمئن و پشتیبانی تخصصی به خریداران محترم ارائه می‌دهد.</p>"""
    },
    {
        "slug": "toshiba-43-inch-fhd-led-tv",
        "name": "تلویزیون 43 اینچ ال ای دی هوشمند توشیبا مدل 43V35RP",
        "brand_fa": "توشیبا",
        "brand_en": "Toshiba",
        "model": "43V35RP",
        "img_file": "toshiba-43-inch-fhd-led-tv.webp",
        "focus_keyword": "تلویزیون توشیبا 43V35RP",
        "meta_description": "خرید تلویزیون ۴۳ اینچ ال ای دی هوشمند توشیبا مدل 43V35RP با کیفیت تصویر Full HD، صدای دالبی دیجیتال، گیرنده دیجیتال داخلی و طراحی باریک از فروشگاه لوازم خانگی حسینی اهواز.",
        "tags": ["تلویزیون توشیبا", "تلویزیون ۴۳ اینچ توشیبا", "تلویزیون هوشمند توشیبا", "توشیبا 43V35RP", "تلویزیون Full HD توشیبا"],
        "attributes": [
            {"name": "برند", "visible": True, "options": ["توشیبا (Toshiba)"]},
            {"name": "مدل", "visible": True, "options": ["43V35RP"]},
            {"name": "سایز صفحه نمایش", "visible": True, "options": ["۴۳ اینچ"]},
            {"name": "کیفیت تصویر", "visible": True, "options": ["Full HD (1080p)"]},
            {"name": "سیستم صوتی", "visible": True, "options": ["Dolby Audio استریو دو کاناله"]},
            {"name": "گیرنده دیجیتال", "visible": True, "options": ["DVB-T2 با پشتیبانی از HEVC"]},
            {"name": "سیستم‌عامل", "visible": True, "options": ["سیستم هوشمند VIDAA"]},
            {"name": "درگاه‌ها", "visible": True, "options": ["۲ عدد HDMI، ۲ عدد USB، Wi-Fi"]}
        ],
        "short_description": """<ul>
  <li><strong>صفحه نمایش ۴۳ اینچ Full HD:</strong> نمایش واضح و پرجزئیات برنامه‌های تلویزیونی و فیلم‌ها با رزولوشن ۱۰۸۰×۱۹۲۰ پیکسل</li>
  <li><strong>موتور پردازش تصویر REGZA Engine HG:</strong> ارتقای شفافیت تصویر، کاهش خودکار نویز سیگنال و بهبود رنگ‌ها</li>
  <li><strong>صدای شفاف Dolby Audio:</strong> تقویت صدای مکالمات و جلوه‌های صوتی برای لذت بیشتر در تماشای برنامه‌ها</li>
  <li><strong>گیرنده داخلی نسل جدید DVB-T2:</strong> پشتیبانی کامل از تمامی کانال‌های باکیفیت صدا و سیما بدون نیاز به ستاپ‌باکس</li>
  <li><strong>طراحی باریک و کم‌حاشیه:</strong> مناسب برای سالن‌های نقلی، اتاق‌های خواب و محیط‌های اداری و تجاری</li>
</ul>""",
        "description": """<p>اگر برای فضاهای مسکونی با ابعاد جمع‌وجور، اتاق خواب یا هتل‌ها به دنبال تلویزیونی بادوام، باکیفیت و ساخت برند اصیل ژاپنی در دسته <a href="https://hosseinykala.ir/product-category/audio-video/television/">تلویزیون</a> هستید، <strong>تلویزیون 43 اینچ ال ای دی هوشمند توشیبا مدل 43V35RP</strong> انتخابی هوشمندانه و مطمئن است. مهندسی توشیبا در این مدل، تصویری بدون نویز با پنل مستحکم را به همراه کاربری آسان تضمین می‌کند.</p>

<h3>ویژگی‌ها و مزایای برجسته تلویزیون توشیبا مدل 43V35RP</h3>
<ul>
  <li><strong>وضوح مطلوب تصویر Full HD:</strong> عملکرد عالی در نمایش محتواهای باکیفیت و برنامه‌های ورزشی با زاویه دید گسترده.</li>
  <li><strong>پردازش تصویر پیشرفته REGZA:</strong> جلوگیری از مات شدن لبه‌های اجسام و تفکیک زنده طیف رنگ‌های طبیعی.</li>
  <li><strong>امکانات ارتباطی کامل:</strong> پورت‌های HDMI برای اتصال انواع گیرنده‌ها و کنسول‌ها و پورت USB برای تماشای فایل‌های تصویری.</li>
  <li><strong>سیستم صوتی استاندارد دالبی:</strong> انتقال متوازن امواج صوتی در محیط برای داشتن صدایی رسا و شفاف.</li>
</ul>

<h3>مشخصات فنی تلویزیون ۴۳ اینچ ال ای دی توشیبا مدل 43V35RP</h3>
<table style='width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px;'>
  <tbody>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9; width: 35%;'>برند</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>توشیبا (Toshiba)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>مدل</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>43V35RP</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>سایز صفحه نمایش</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>۴۳ اینچ (LED)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>کیفیت تصویر</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>Full HD (۱۹۲۰ × ۱۰۸۰)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>پردازنده تصویر</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>REGZA Engine HG</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>سیستم صوتی</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>Dolby Audio دو کاناله ۱۶ وات</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>گیرنده دیجیتال</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>DVB-T2 با پشتیبانی کامل از HEVC</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>درگاه‌های اتصالی</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>۲ عدد HDMI، ۲ عدد USB، خروجی صدا، ورودی آنتن و Wi-Fi</td></tr>
  </tbody>
</table>

<h3>خرید حضوری و اینترنتی از فروشگاه حسینی</h3>
<p>شما می‌توانید <strong>تلویزیون 43 اینچ ال ای دی هوشمند توشیبا مدل 43V35RP</strong> را با تضمین اصالت و سلامت کامل کالا از <strong><a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a></strong> خریداری فرمایید. فروشگاه حسینی در شهر <strong>اهواز</strong> با ارائه خدمات ارسال سریع و ایمن به سراسر کشور، خریدی راحت و مطمئن را برای شما فراهم می‌آورد.</p>"""
    },
    {
        "slug": "hisense-43-inch-4k-smart-tv",
        "name": "تلویزیون هوشمند 43 اینچ 4K هایسنس مدل 43A61Q",
        "brand_fa": "هایسنس",
        "brand_en": "Hisense",
        "model": "43A61Q",
        "img_file": "hisense-43-inch-4k-smart-tv.webp",
        "focus_keyword": "تلویزیون هایسنس 43A61Q 4K",
        "meta_description": "خرید تلویزیون هوشمند ۴۳ اینچ 4K هایسنس مدل 43A61Q با رزولوشن Ultra HD، سیستم‌عامل هوشمند VIDAA، پشتیبانی از HDR10 و صدای فراگیر دالبی از فروشگاه لوازم خانگی حسینی اهواز.",
        "tags": ["تلویزیون هایسنس", "تلویزیون ۴۳ اینچ هایسنس", "تلویزیون 4K هایسنس", "هایسنس 43A61Q", "تلویزیون هوشمند هایسنس"],
        "attributes": [
            {"name": "برند", "visible": True, "options": ["هایسنس (Hisense)"]},
            {"name": "مدل", "visible": True, "options": ["43A61Q (سری A6)"]},
            {"name": "سایز صفحه نمایش", "visible": True, "options": ["۴۳ اینچ"]},
            {"name": "کیفیت تصویر", "visible": True, "options": ["4K Ultra HD (2160p)"]},
            {"name": "استاندارد HDR", "visible": True, "options": ["HDR10 و HLG"]},
            {"name": "سیستم صوتی", "visible": True, "options": ["DTS Virtual:X و Dolby Digital"]},
            {"name": "سیستم‌عامل", "visible": True, "options": ["سیستم هوشمند VIDAA U"]},
            {"name": "درگاه‌های ارتباطی", "visible": True, "options": ["۳ عدد HDMI، ۲ عدد USB، بلوتوث و وای‌فای"]}
        ],
        "short_description": """<ul>
  <li><strong>کیفیت تصویر خیره‌کننده 4K Ultra HD:</strong> وضوح ۴ برابری نسبت به نمایشگرهای FHD با رزولوشن ۲۱۶۰×۳۸۴۰ برای مشاهده تمامی جزئیات ریز تصاویر</li>
  <li><strong>پشتیبانی از فناوری‌های HDR10 و HLG:</strong> کنتراست فوق‌العاده و تفکیک دقیق بین روشن‌ترین و تاریک‌ترین بخش‌های تصویر</li>
  <li><strong>صدای سینمایی فراگیر DTS Virtual:X:</strong> شبیه‌سازی صدای سه‌بعدی و فراگیر بدون نیاز به بلندگوهای جانبی</li>
  <li><strong>سیستم‌عامل روان و سریع VIDAA U:</strong> اتصال مستقیم و سریع به اینترنت، سرویس‌های ویدیویی و قابلیت اشتراک صفحه گوشی (Anyview Cast)</li>
  <li><strong>حالت اختصاصی بازی (Game Mode) و ورزش (Sports Mode):</strong> تاخیر ورودی پایین و نمایش فوق‌العاده نرم حرکات سریع در بازی‌ها و مسابقات</li>
</ul>""",
        "description": """<p>اگر در ابعاد جمع‌وجور ۴۳ اینچ به دنبال نهایت شفافیت و کیفیت تصویر در دسته <a href="https://hosseinykala.ir/product-category/audio-video/television/">تلویزیون</a> هستید، <strong>تلویزیون هوشمند 43 اینچ 4K هایسنس مدل 43A61Q</strong> یکی از معدود و درخشان‌ترین تلویزیون‌های ۴۳ اینچ 4K بازار محسوب می‌شود. هایسنس به عنوان یکی از غول‌های صوتی و تصویری جهان، در این مدل امکانات یک پرچمدار را در ابعادی مناسب اتاق و سالن‌های مدرن عرضه کرده است.</p>

<h3>ویژگی‌ها و مزایای برجسته تلویزیون ۴۳ اینچ فورکی هایسنس مدل 43A61Q</h3>
<ul>
  <li><strong>تراکم پیکسلی بسیار بالا:</strong> کیفیت 4K در ابعاد ۴۳ اینچ باعث می‌شود تصاویر از فواصل نزدیک نیز بسیار شارپ، شفاف و بدون پیکسل‌بندی دیده شوند.</li>
  <li><strong>فناوری Precision Colour:</strong> نمایش غنی و زنده‌ی رنگ‌ها با عمق و غلظت طبیعی.</li>
  <li><strong>صدای چندکاناله فراگیر:</strong> پردازش صوتی DTS Virtual:X که گفتگوها را کاملاً از صدای پس‌زمینه و موسیقی فیلم جدا می‌کند.</li>
  <li><strong>اشتراک بی‌سیم صفحه موبایل:</strong> پخش بی‌وقفه بازی‌ها، عکس‌ها و فایل‌های شخصی از گوشی‌های اندروید و آیفون روی صفحه تلویزیون.</li>
</ul>

<h3>مشخصات فنی تلویزیون هوشمند ۴۳ اینچ 4K هایسنس مدل 43A61Q</h3>
<table style='width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px;'>
  <tbody>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9; width: 35%;'>برند</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>هایسنس (Hisense)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>مدل</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>43A61Q (سری A6)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>سایز صفحه نمایش</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>۴۳ اینچ (DLED)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>کیفیت تصویر</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>4K Ultra HD (۲۱۶۰ × ۳۸۴۰)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>استانداردهای HDR</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>HDR10 و HLG</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>فناوری‌های صوتی</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>DTS Virtual:X و Dolby Digital (۱۴ وات)</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>سیستم‌عامل</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>سیستم‌عامل هوشمند VIDAA U</td></tr>
    <tr><th style='text-align: right; padding: 8px; border: 1px solid #e0e0e0; background: #f9f9f9;'>درگاه‌های اتصالی</th><td style='padding: 8px; border: 1px solid #e0e0e0;'>۳ درگاه HDMI (پشتیبانی از ALLM)، ۲ درگاه USB، بلوتوث، وای‌فای، ورودی AV و خروجی اپتیکال</td></tr>
  </tbody>
</table>

<h3>خرید حضوری و اینترنتی از فروشگاه حسینی</h3>
<p>شما می‌توانید <strong>تلویزیون هوشمند 43 اینچ 4K هایسنس مدل 43A61Q</strong> را با تضمین اصالت و سلامت فیزیکی از <strong><a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a></strong> تهیه کنید. فروشگاه حسینی با داشتن شعب در شهر <strong>اهواز</strong>، خدمات ارسال سریع و تضمینی به سراسر خوزستان و تمامی استان‌های کشور را با افتخار ارائه می‌نماید.</p>"""
    }
]

def upload_image(image_path, slug):
    print(f"در حال آپلود تصویر برای {slug}...", flush=True)
    with open(image_path, 'rb') as img_f:
        img_bytes = img_f.read()

    media_headers = dict(HEADERS)
    media_headers.update({
        'Content-Disposition': f'attachment; filename="{slug}.webp"',
        'Content-Type': 'image/webp'
    })

    res = requests.post(MEDIA_API, data=img_bytes, headers=media_headers, auth=AUTH, timeout=40)
    if res.status_code in (200, 201):
        media_data = res.json()
        media_id = media_data.get('id')
        media_url = media_data.get('source_url', '')
        print(f"✓ تصویر با شناسه {media_id} آپلود شد.", flush=True)
        return media_id, media_url
    else:
        raise Exception(f"خطای آپلود مدیا ({res.status_code}): {res.text[:200]}")

def publish_tv(tv_item):
    slug = tv_item['slug']
    p_dir = os.path.join(NEW_PRODS_DIR, slug)
    os.makedirs(os.path.join(p_dir, 'images'), exist_ok=True)
    
    # Copy processed image
    src_img = os.path.join(PROCESSED_IMG_DIR, tv_item['img_file'])
    dst_img = os.path.join(p_dir, 'images', 'featured.webp')
    shutil.copy2(src_img, dst_img)

    # Save info.json
    info_data = {
        "id_key": slug.replace('-', '_'),
        "name": tv_item['name'],
        "slug": slug,
        "brand_fa": tv_item['brand_fa'],
        "brand_en": tv_item['brand_en'],
        "category_id": 243,
        "category_slug": "television",
        "model": tv_item['model'],
        "qty": 0,
        "stock_status": "outofstock",
        "focus_keyword": tv_item['focus_keyword'],
        "meta_description": tv_item['meta_description'],
        "tags": tv_item['tags'],
        "short_description": tv_item['short_description'],
        "description": tv_item['description'],
        "attributes": tv_item['attributes'],
        "images": ["images/featured.webp"],
        "wc_category_ids": [243, 242],
        "wc_category_name": "تلویزیون",
        "wc_canonical_url": "https://hosseinykala.ir/product-category/audio-video/television/"
    }
    with open(os.path.join(p_dir, 'info.json'), 'w', encoding='utf-8') as f:
        json.dump(info_data, f, ensure_ascii=False, indent=2)

    with open(os.path.join(p_dir, 'content.md'), 'w', encoding='utf-8') as f:
        f.write(tv_item['description'])

    # Upload Media
    media_id, media_url = upload_image(dst_img, slug)

    sku = f"HK-{slug.upper()}"
    cat_list = [{'id': 243}, {'id': 242}]
    tag_list = [{'name': t} for t in tv_item['tags']]

    payload = {
        'name': tv_item['name'],
        'slug': slug,
        'type': 'simple',
        'status': 'publish',
        'catalog_visibility': 'visible',
        'description': tv_item['description'],
        'short_description': tv_item['short_description'],
        'sku': sku,
        'price': '',
        'regular_price': '',
        'manage_stock': False,
        'stock_status': 'outofstock',
        'images': [{'id': media_id}],
        'categories': cat_list,
        'tags': tag_list,
        'attributes': tv_item['attributes'],
        'meta_data': [
            {'key': 'rank_math_focus_keyword', 'value': tv_item['focus_keyword']},
            {'key': 'rank_math_description', 'value': tv_item['meta_description']},
            {'key': '_yoast_wpseo_focuskw', 'value': tv_item['focus_keyword']},
            {'key': '_yoast_wpseo_metadesc', 'value': tv_item['meta_description']}
        ]
    }

    print(f"در حال ایجاد محصول ووکامرس برای {slug}...", flush=True)
    res = requests.post(WC_PRODUCTS_API, json=payload, headers=HEADERS, auth=AUTH, timeout=40)
    if res.status_code in (200, 201):
        prod_data = res.json()
        pid = prod_data.get('id')
        permalink = prod_data.get('permalink', f"{WP_BASE}/product/{slug}/")
        print(f"🎉 منتشر شد (PID {pid}): {tv_item['name']}", flush=True)
        return {
            'slug': slug,
            'name': tv_item['name'],
            'product_id': pid,
            'permalink': permalink,
            'media_id': media_id,
            'media_url': media_url,
            'status': 'publish',
            'stock_status': 'outofstock',
            'sku': sku,
            'brand': tv_item['brand_fa'],
            'published_at': time.strftime("%Y-%m-%d %H:%M:%S")
        }
    else:
        raise Exception(f"خطای ایجاد محصول ({res.status_code}): {res.text[:300]}")

def main():
    print("=== انتشار ۵ تلویزیون جدید در وب‌سایت حسینی کالا ===", flush=True)
    results = {}
    for item in TVS_DATA:
        res = publish_tv(item)
        results[item['slug']] = res
        time.sleep(1)

    os.makedirs(os.path.dirname(OUTPUT_RESULT), exist_ok=True)
    with open(OUTPUT_RESULT, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ نتایج انتشار ۵ تلویزیون در {os.path.basename(OUTPUT_RESULT)} ذخیره شد.", flush=True)

if __name__ == '__main__':
    main()
