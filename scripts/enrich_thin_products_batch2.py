import requests
import json
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Content-Type': 'application/json'
}

PRODUCTS_BATCH2 = {
    2457: {
        'title': 'یخچال فریزر دوقلو 40 فوت کلور مدل روسو پلاس (Rosso Plus) عرض 60',
        'slug': 'clover-rosso-plus-w60-twin-refrigerator-40ft',
        'content': '''<h2>بررسی تخصصی یخچال فریزر دوقلو کلور مدل روسو پلاس (Rosso Plus) عرض ۶۰</h2>
<p>کلور همواره به عنوان یکی از پیشگامان تولید یخچال‌فریزرهای فوق‌مدرن با موتورهای کم‌صدا و کم‌مصرف اینورتر در ایران شناخته می‌شود. <strong>یخچال فریزر دوقلو ۴۰ فوت کلور مدل روسو پلاس (Rosso Plus)</strong> با عرض ۶۰ سانتی‌متر برای هر لنگه، پاسخی دقیق به نیاز خانواده‌هایی است که می‌خواهند با کمترین اشغال فضای عرضی در کابینت‌های آشپزخانه، بیشترین ظرفیت مفید سرمایشی را تجربه کنند.</p>

<p>این مدل مجهز به کمپرسور نسل جدید اینورتر دیجیتال است که با تنظیم دور موتور بر اساس دمای محیط، مصرف انرژی را به رده +A رسانده و صدای کارکرد دستگاه را به سطح نجواگونه ۳۸ دسی‌بل کاهش می‌دهد. سیستم عایق‌بندی فوم سیکلوپنتان، جریان هوای چندگانه هوشمند و سیستم نوفراست کامل، ماندگاری و طراوت مواد غذایی را تا چند برابر نسبت به یخچال‌های معمولی افزایش می‌دهد.</p>

<h3>ویژگی‌های متمایز یخچال دوقلو کلور روسو پلاس</h3>
<ul>
    <li><strong>موتور هوشمند اینورتر دیجیتال:</strong> تنظیم هوشمندانه دور موتور، افزایش طول عمر کمپرسور و کاهش چشمگیر هزینه برق.</li>
    <li><strong>سیستم خنک‌کننده Twin Cooling:</strong> تبرید مستقل یخچال و فریزر بدون انتقال بو میان کابین‌ها.</li>
    <li><strong>کشوهای ریلی آرام‌بند با کنترل رطوبت:</strong> حفظ سبزیجات و میوه‌ها به مدت طولانی با تازگی روز اول.</li>
    <li><strong>آبسردکن و یخساز بیرونی:</strong> دسترسی سریع و آسان بدون نیاز به باز کردن مکرر درب یخچال.</li>
    <li><strong>ضمانت معتبر ۳۰ ماهه کلور:</strong> گارانتی سراسری و پشتیبانی فنی کارخانجات صنایع الکترونیک کلور.</li>
</ul>

<h3>جدول مشخصات فنی یخچال دوقلو کلور روسو پلاس</h3>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; text-align: right;" border="1">
    <tbody>
        <tr style="background-color: #f8f9fa;">
            <th style="padding: 10px; border: 1px solid #ddd; width: 35%;">مشخصه فنی</th>
            <th style="padding: 10px; border: 1px solid #ddd;">توضیحات و مقادیر</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">برند سازنده</td>
            <td style="padding: 10px; border: 1px solid #ddd;">کلور (Clover)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">مدل فنی دستگاه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Rosso Plus W60 (دوقلو عرض ۶۰)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">ظرفیت اسمی کل</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۴۰ فوت (۲۰ فوت یخچال + ۲۰ فوت فریزر)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">نوع موتور</td>
            <td style="padding: 10px; border: 1px solid #ddd;">کمپرسور اینورتر دیجیتال کم‌صدا و کم‌مصرف</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">رده مصرف انرژی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">+A</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">سیستم ضد برفک</td>
            <td style="padding: 10px; border: 1px solid #ddd;">نوفراست ۱۰۰٪ با جریان هوای چندگانه اختصاصی</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">تعداد کشوهای فریزر</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۷ کشوی ریلی مقاوم با تحمل وزن بالا</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">مدت زمان گارانتی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۳۰ ماه ضمانت رسمی قطعات و کمپرسور کلور سرویس</td>
        </tr>
    </tbody>
</table>'''
    },

    2431: {
        'title': 'یخچال 10 فوت کلور مدل مینی هتلی (Mini Refrigerator)',
        'slug': 'clover-mini-refrigerator-10ft',
        'content': '''<h2>بررسی تخصصی یخچال ۱۰ فوت مینی هتلی کلور</h2>
<p>برای اتاق خواب، دفتر کار، مطب پزشکان، اتاق دانشجویی یا سوئیت‌های اداری و اقامتی، یک یخچال کوچک، کم‌صدا و شیک که به راحتی در هر گوشه‌ای جای بگیرد نعمتی بزرگ است. <strong>یخچال ۱۰ فوت کلور مدل مینی هتلی</strong> با طراحی فشرده و ارگونومیک، سرمایشی پرقدرت و یکنواخت را در ابعادی کوچک و متناسب در اختیارتان می‌گذارد.</p>

<p>کلور در این مدل از عایق‌بندی ضخیم و کمپرسور بسیار بی‌صدا استفاده کرده تا در هنگام استراحت یا کار، هیچ صدای آزاردهنده‌ای در فضا حس نشود. این مینی یخچال علاوه بر طبقات شیشه‌ای مستحکم برای نگهداری انواع بطری، نوشیدنی و ظروف غذا، دارای یک محفظه یخدان (فریزر کوچک) در بخش بالایی است که برای قالب‌های یخ و بستنی بسیار کاربردی است.</p>

<h3>مزایای یخچال ۱۰ فوت مینی کلور</h3>
<ul>
    <li><strong>فوق‌العاده کم‌صدا و آرام:</strong> عملکرد بی‌صدا و بدون لرزش، کاملاً مناسب برای قرارگیری در کنار تختخواب یا میز کار.</li>
    <li><strong>دارای جایگاه بطری‌های بزرگ:</strong> طراحی درب به شکلی که بطری‌های بلند آب و نوشیدنی به سادگی در آن قرار می‌گیرند.</li>
    <li><strong>مصرف برق بسیار پایین:</strong> رده انرژی اقتصادی که باعث می‌شود هیچ فشاری به قبض برق وارد نشود.</li>
    <li><strong>طبقات شیشه‌ای نشکن:</strong> تحمل وزن بالا و قابلیت شستشو و جابجایی آسان در چند ارتفاع مختلف.</li>
    <li><strong>گارانتی رسمی کلور:</strong> ۲۴ ماه ضمانت معتبر شرکتی در حسینی کالا.</li>
</ul>

<h3>جدول مشخصات فنی یخچال ۱۰ فوت مینی کلور</h3>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; text-align: right;" border="1">
    <tbody>
        <tr style="background-color: #f8f9fa;">
            <th style="padding: 10px; border: 1px solid #ddd; width: 35%;">مشخصه فنی</th>
            <th style="padding: 10px; border: 1px solid #ddd;">توضیحات و مقادیر</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">برند سازنده</td>
            <td style="padding: 10px; border: 1px solid #ddd;">کلور (Clover)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">مدل دستگاه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Mini Refrigerator 10ft (مینی هتلی)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">ظرفیت اسمی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۱۰ فوت مفید</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">محفظه جایخی / فریزر</td>
            <td style="padding: 10px; border: 1px solid #ddd;">دارد (محفظه کوچک درب‌دار در بالای کابین)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">رده مصرف انرژی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">رده A (کم‌مصرف)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">گاز مبرد</td>
            <td style="padding: 10px; border: 1px solid #ddd;">R600a دوستدار محیط زیست</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">کاربری مناسب</td>
            <td style="padding: 10px; border: 1px solid #ddd;">هتل‌ها، دفاتر کار، اتاق خواب، مطب و خوابگاه‌ها</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">گارانتی و خدمات</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۲۴ ماه ضمانت رسمی صنایع الکترونیک کلور</td>
        </tr>
    </tbody>
</table>'''
    },

    3312: {
        'title': 'آبسردکن ایستاده نیکایی مدل NWD-1400R یخچال دار',
        'slug': 'nikai-nwd1400r-water-dispenser',
        'content': '''<h2>بررسی تخصصی آبسردکن ایستاده نیکایی مدل NWD-1400R یخچال‌دار</h2>
<p>دسترسی سریع به آب خنک و گوارا در گرمای تابستان و آب جوش فوری برای چای و نسکافه، لازمه هر اداره، شرکت، فروشگاه و حتی منزل مدرن است. <strong>آبسردکن ایستاده نیکایی مدل NWD-1400R</strong> محصولی پرقدرت و خوش‌ساخت از برند معتبر نیکایی (Nikai) است که علاوه بر دو خروجی آب سرد و گرم، یک محفظه یخچال‌دار کاربردی در قسمت پایین خود دارد.</p>

<p>کمپرسور قدرتمند و رادیاتور تقویت‌شده این دستگاه آب را تا دمای خنک و گوارای ۶ تا ۱۰ درجه سانتی‌گراد می‌رساند. بخش آب گرم نیز با المنت سرعتی، آب را تا دمای بالای ۹۰ درجه سانتی‌گراد داغ می‌کند و دارای قفل کودک ایمن است تا از سوختگی اتفاقی دست کودکان جلوگیری شود. محفظه یخچال پایینی فضایی فوق‌العاده برای خنک نگه داشتن میوه، بطری‌های نوشیدنی یا ناهار پرسنل است.</p>

<h3>ویژگی‌های کلیدی آبسردکن نیکایی NWD-1400R</h3>
<ul>
    <li><strong>دارای یخچال خنک‌کننده در بخش پایین:</strong> نگهداری میوه، دارو، لبنیات و نوشیدنی‌های پرسنل.</li>
    <li><strong>مخزن استیل ضد زنگ ۳۰۴:</strong> آب کاملاً بهداشتی، بدون بو و تغییر مزه حتی در استفاده طولانی‌مدت.</li>
    <li><strong>کلید ایمنی کودک روی شیر آب جوش:</strong> جلوگیری کامل از خروج تصادفی آب داغ.</li>
    <li><strong>کمپرسور پرقدرت و کم‌صدا:</strong> عملکرد مداوم در دمای بالای محیط بدون افت راندمان.</li>
    <li><strong>سینی چکه‌گیر متحرک:</strong> شستشوی آسان و جلوگیری از ریختن قطرات آب روی زمین.</li>
</ul>

<h3>جدول مشخصات فنی آبسردکن نیکایی NWD-1400R</h3>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; text-align: right;" border="1">
    <tbody>
        <tr style="background-color: #f8f9fa;">
            <th style="padding: 10px; border: 1px solid #ddd; width: 35%;">مشخصه فنی</th>
            <th style="padding: 10px; border: 1px solid #ddd;">توضیحات و مقادیر</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">برند سازنده</td>
            <td style="padding: 10px; border: 1px solid #ddd;">نیکایی (Nikai)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">مدل فنی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">NWD-1400R</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">نوع دستگاه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">ایستاده دو منظوره همراه با کابینت یخچال</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">توان سرمایش / گرمایش</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۱۰۰ وات سرمایش / ۵۰۰ وات گرمایش سریع</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">دمای خروجی آب</td>
            <td style="padding: 10px; border: 1px solid #ddd;">سرد: ۶ الی ۱۰ درجه سانتی‌گراد | داغ: ۸۸ الی ۹۵ درجه</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">جنس مخزن داخلی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">استیل ضد زنگ ضد زنگ ضد رسوب SUS304</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">منبع ورودی آب</td>
            <td style="padding: 10px; border: 1px solid #ddd;">قابلیت نصب مخزن ساده، مخزن فیلتردار و اتصال به تصفیه آب</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">گارانتی و ضمانت</td>
            <td style="padding: 10px; border: 1px solid #ddd;">گارانتی سلامت فیزیکی و اصالت کالا از حسینی کالا</td>
        </tr>
    </tbody>
</table>'''
    },

    3457: {
        'title': 'چای ساز لمسی دونالکس مدل DN-185 شیشه ای پیرکس',
        'slug': 'donalex-dn185-tea-maker',
        'content': '''<h2>بررسی تخصصی چای‌ساز لمسی دونالکس مدل DN-185 پیرکس</h2>
<p>دم کشیدن اصولی چای ایرانی نیازمند حرارت ملایم و بخار کنترل‌شده است تا رنگ و عطر چای کاملاً شفاف و دلپذیر باقی بماند. <strong>چای‌ساز روهمی لمسی دونالکس مدل DN-185</strong> با طراحی مدرن مشکی-سیلور و قوری و کتری از جنس پیرکس فوق‌مقاوم آلمانی، همان کیفیت دمیِ سنتی را در سریع‌ترین زمان ممکن به آشپزخانه شما می‌آورد.</p>

<p>المنت قدرتمند ۲۲۰۰ واتی این دستگاه آب کتری را تنها ظرف چند دقیقه به نقطه جوش می‌رساند. پس از جوش آمدن، سیستم هوشمند سنسور استیم به طور خودکار به حالت گرم‌نگه‌دار (Keep Warm) تغییر وضعیت می‌دهد تا هم در مصرف برق صرفه‌جویی شود و هم چای به آرامی دم کشیده و نسوزد. پنل کنترل لمسی دستگاه با نمایشگر دیجیتال، امکان تنظیم دقیق دما را برای انواع دمنوش‌ها و چای سبز فراهم می‌سازد.</p>

<h3>امکانات کلیدی چای‌ساز دونالکس DN-185</h3>
<ul>
    <li><strong>پیرکس بروسیلیکات ضد شوک حرارتی:</strong> مقاومت کامل در برابر تغییرات ناگهانی دما بدون کوچک‌ترین ترک‌خوردگی.</li>
    <li><strong>نورپردازی LED آبی زیبا:</strong> جلوه بصری فوق‌العاده درون کتری هنگام جوشیدن آب.</li>
    <li><strong>صافی استیل ضد زنگ لیزری:</strong> تفاله‌گیر عمیق درون قوری با منافذ ریز جهت داشتن چایی کاملاً زلال.</li>
    <li><strong>پایه ۳۶۰ درجه بدون سیم:</strong> چرخش آسان کتری و قوری و استفاده راحت برای افراد راست‌دست و چپ‌دست.</li>
    <li><strong>سیستم ایمنی خاموشی خودکار:</strong> خاموش شدن خودکار در صورت نبود آب (Boil-Dry Protection).</li>
</ul>

<h3>جدول مشخصات فنی چای‌ساز دونالکس DN-185</h3>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; text-align: right;" border="1">
    <tbody>
        <tr style="background-color: #f8f9fa;">
            <th style="padding: 10px; border: 1px solid #ddd; width: 35%;">مشخصه فنی</th>
            <th style="padding: 10px; border: 1px solid #ddd;">توضیحات و مقادیر</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">برند سازنده</td>
            <td style="padding: 10px; border: 1px solid #ddd;">دونالکس (Donalex)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">مدل دستگاه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">DN-185</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">توان مصرفی المنت</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۲۲۰۰ وات واقعی با جوش‌آوری فوق‌سریع</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">ظرفیت کتری و قوری</td>
            <td style="padding: 10px; border: 1px solid #ddd;">کتری ۲.۵ لیتری + قوری ۱.۰ لیتری</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">جنس بدنه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">پیرکس شفاف نشکن همراه با قطعات استیل ضد زنگ</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">پنل تنظیمات</td>
            <td style="padding: 10px; border: 1px solid #ddd;">لمسی دیجیتال با قابلیت انتخاب دمای دمنوش</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">سیستم خاموشی ایمن</td>
            <td style="padding: 10px; border: 1px solid #ddd;">دارد (قطع خودکار در نقطه جوش و بی‌آبی)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">گارانتی رسمی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۲۴ ماه ضمانت شرکتی دونالکس در حسینی کالا</td>
        </tr>
    </tbody>
</table>'''
    },

    3019: {
        'title': 'آبمیوه‌گیری ۴ کاره ۱۰۰۰ وات دونالکس مدل DN-120 چندکاره',
        'slug': 'donalex-dn120-4in1-juicer',
        'content': '''<h2>بررسی تخصصی آبمیوه‌گیری ۴ کاره ۱۰۰۰ وات دونالکس مدل DN-120</h2>
<p>خرید دستگاه‌های مجزا برای آبمیوه‌گیری، مخلوط‌کن، آسیاب و خردکن علاوه بر هزینه سنگین، فضای زیادی از کابینت‌های آشپزخانه را اشغال می‌کند. <strong>آبمیوه‌گیری ۴ کاره دونالکس مدل DN-120 با توان ۱۰۰۰ وات</strong> یک دستیار حرفه‌ای همه‌فن‌حریف است که چهار عملیات اساسی آماده‌سازی غذا و نوشیدنی را در قالبی شکیل و مستحکم پوشش می‌دهد.</p>

<p>موتور توربو ۱۰۰۰ واتی با پروانه‌های خنک‌کننده، راندمان آبگیری را به بیش از ۸۵ درصد رسانده است. پارچ شیشه‌ای پیرکس مخلوط‌کن ۱.۵ لیتری برای تهیه انواع اسموتی و سوپ، ظرف خردکن شیشه‌ای برای گوشت و سبزیجات، و آسیاب پرقدرت برای مغزیجات و دانه‌های قهوه، این پکیج را به انتخابی بی‌رقیب برای جهیزیه و آشپزخانه‌های مدرن تبدیل کرده است.</p>

<h3>قابلیت‌های ۴ گانه دونالکس مدل DN-120</h3>
<ul>
    <li><strong>آبمیوه‌گیری دهانه بزرگ:</strong> آبگیری سیب، هویج و انار کامل بدون نیاز به برش.</li>
    <li><strong>مخلوط‌کن شیشه‌ای پیرکس:</strong> تیغه‌های ۶ پره یخ‌شکن برای ساخت اسموتی و کوکتل‌های خنک.</li>
    <li><strong>خردکن همه‌کاره:</strong> خرد کردن سریع گوشت، مرغ، پیاز و سبزیجات بدون له کردن بافت.</li>
    <li><strong>آسیاب سخت‌زن:</strong> پودر کردن هل، زعفران، دانه فلفل و قهوه در چند ثانیه.</li>
    <li><strong>بدنه تمام استیل ضد زنگ:</strong> دوام بالا، نظافت آسان و زیبایی چشم‌نواز روی پیشخوان.</li>
</ul>

<h3>جدول مشخصات فنی آبمیوه‌گیری ۴ کاره دونالکس DN-120</h3>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; text-align: right;" border="1">
    <tbody>
        <tr style="background-color: #f8f9fa;">
            <th style="padding: 10px; border: 1px solid #ddd; width: 35%;">مشخصه فنی</th>
            <th style="padding: 10px; border: 1px solid #ddd;">توضیحات و مقادیر</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">برند سازنده</td>
            <td style="padding: 10px; border: 1px solid #ddd;">دونالکس (Donalex)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">مدل دستگاه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">DN-120 4-in-1 Juicer</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">توان واقعی موتور</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۱۰۰۰ وات سیم‌پیچ مسی توربو</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">کارکردها</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۴ کاره (آبمیوه‌گیری، مخلوط‌کن، خردکن، آسیاب)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">جنس ظروف جانبی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">شیشه پیرکس ضخیم نشکن و بهداشتی</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">جنس تیغه‌ها</td>
            <td style="padding: 10px; border: 1px solid #ddd;">تیغه‌های تیتانیومی-استیل ضد زنگ ۳۰۴ ضد سایش</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">تنظیمات سرعت</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۲ سرعته دیجیتال همراه با کلید عملکرد لحظه‌ای (Pulse)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">گارانتی رسمی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۲۴ ماه ضمانت معتبر شرکتی دونالکس در حسینی کالا</td>
        </tr>
    </tbody>
</table>'''
    },

    3357: {
        'title': 'سرویس پخت و پز 10 پارچه اویز مدل سلین گرانیتی',
        'slug': 'oviz-celine-10pcs-cookware-set',
        'content': '''<h2>بررسی تخصصی سرویس قابلمه ۱۰ پارچه گرانیتی اویز مدل سلین (Celine)</h2>
<p>آشپزی سالم و لذت‌بخش در گرو استفاده از ظروفی است که مواد غذایی به کف آن نچسبد، مصرف روغن را به حداقل برساند و هیچ‌گونه ماده شیمیایی مضری در حرارت بالا آزاد نکند. <strong>سرویس پخت و پز ۱۰ پارچه اویز مدل سلین (Celine)</strong> با پوشش نانو گرانیت ایتالیایی چندلایه و بدنه آلومینیوم دایکست (چدن فشرده)، از باکیفیت‌ترین و استانداردترین ست‌های پخت‌وپز برای مصارف روزمره و جهیزیه است.</p>

<p>کف این قابلمه‌ها دارای اینداکشن رینگی ضخیم است که حرارت شعله گاز را با تعادل کامل در سراسر دیواره‌ها پخش می‌کند و مانع از سوختن نقطه‌ای خورش یا ته گرفتگی برنج می‌شود. دسته‌های این ست به صورت یکپارچه با بدنه ریخته‌گری شده‌اند؛ بنابراین هیچ پیچی شل نمی‌شود و مقاومت حرارتی فوق‌العاده‌ای دارد. درب‌های شیشه‌ای سوپاپ‌دار از جنس پیرکس دورسیلیکونی نیز امکان مشاهده مراحل پخت بدون برداشتن مکرر درب را فراهم می‌سازند.</p>

<h3>اقلام و ویژگی‌های سرویس ۱۰ پارچه اویز سلین</h3>
<ul>
    <li><strong>پوشش گرانیتی مقاوم به خط و خش:</strong> پوشش نانو گیاهی بدون فلزات سنگین (PFOA Free) با نچسبی استثنایی.</li>
    <li><strong>شامل سایزهای کاربردی:</strong> ۳ قابلمه در ابعاد استاندارد (سایزهای ۲۰، ۲۴ و ۲۸) به همراه یک تابه دو دسته ۲۸ و تابه تک‌دسته.</li>
    <li><strong>دسته‌های متصل نسوز:</strong> قابلیت استفاده آسان حتی درون فر بدون هیچ‌گونه سوختگی و بوی پلاستیک.</li>
    <li><strong>قابلیت شستشوی آسان:</strong> پاک شدن اثر سوختگی و چربی تنها با یک اسفنج نرم یا ماشین ظرفشویی.</li>
    <li><strong>طراحی مدرن اروپایی:</strong> ترکیب رنگ‌های مات و متالیک سازگار با دکوراسیون آشپزخانه‌های لوکس.</li>
</ul>

<h3>جدول مشخصات سرویس قابلمه اویز مدل سلین</h3>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; text-align: right;" border="1">
    <tbody>
        <tr style="background-color: #f8f9fa;">
            <th style="padding: 10px; border: 1px solid #ddd; width: 35%;">مشخصه فنی</th>
            <th style="padding: 10px; border: 1px solid #ddd;">توضیحات و مقادیر</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">برند سازنده</td>
            <td style="padding: 10px; border: 1px solid #ddd;">اویز (Oviz Cookware)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">مدل ست</td>
            <td style="padding: 10px; border: 1px solid #ddd;">سلین (Celine 10-Piece)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">تعداد پارچه‌ها</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۱۰ پارچه (شامل قابلمه‌ها، تابه‌ها و درب‌های پیرکس)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">جنس بدنه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">آلومینیوم دایکست چدن با ضخامت ۵ میلی‌متر</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">نوع پوشش داخلی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">گرانیت چندلایه نچسب فاقد کادمیوم و سرب</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">جنس درب‌ها</td>
            <td style="padding: 10px; border: 1px solid #ddd;">پیرکس مقاوم حرارتی با رینگ استیل و سوپاپ خروج بخار</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">شستشو در ماشین ظرفشویی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">کاملاً مجاز و مقاوم</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">ضمانت کالا</td>
            <td style="padding: 10px; border: 1px solid #ddd;">ضمانت اصالت و سلامت فیزیکی رسمی حسینی کالا</td>
        </tr>
    </tbody>
</table>'''
    },

    3318: {
        'title': 'سرویس پخت و پز 11 پارچه اویز پلاس مدل ویولا گرانیتی',
        'slug': 'oviz-plus-viola-11pcs-cookware-set',
        'content': '''<h2>بررسی تخصصی سرویس قابلمه ۱۱ پارچه گرانیتی اویز پلاس مدل ویولا (Viola)</h2>
<p>آشپزی حرفه‌ای بدون داشتن سایزبندی کامل قابلمه‌ها ممکن نیست. <strong>سرویس پخت و پز ۱۱ پارچه اویز پلاس مدل ویولا (Viola)</strong> با پوشش ضخیم گرانیت ماربل (طرح سنگ مرمر) و بدنه چدن دایکست تقویت‌شده، پکیجی کامل، بادوام و چشم‌نواز را برای تمام وعده‌های غذایی روزانه و مهمانی‌های خانوادگی مهیا کرده است.</p>

<p>اویلا در سری پلاس با استفاده از تکنولوژی کفه چندلایه کپسولی، انتقال حرارت را به حداکثر رسانده است. لایه نانو گرانیتی سطحی به غایت صیقلی دارد که شستشوی آن را در کسری از دقیقه ممکن می‌سازد و اجازه می‌دهد حتی با چند قطره روغن، انواع کوکو، کتلت و ماهی را بدون ذره‌ای چسبندگی برشته کنید. رینگ سیلیکونی اطراف درب‌های پیرکس نیز مانع از لب‌پر شدن شیشه و فرار بخار معطر غذا می‌شود.</p>

<h3>ویژگی‌های متمایز سرویس ۱۱ پارچه اویز پلاس ویولا</h3>
<ul>
    <li><strong>پوشش گرانیت ماربل ضد سایش:</strong> پایداری بالا در برابر کفگیر و قاشق‌های چوبی با ماندگاری چندساله.</li>
    <li><strong>دارای ۴ قابلمه در سایزهای استاندارد:</strong> سایزهای ۲۰ (دو نفره)، ۲۴ (چهار نفره)، ۲۸ (شش تا هشت نفره) و ۳۲ (مهمانی بزرگ).</li>
    <li><strong>تابه دو دسته دیواره بلند سایز ۲۸:</strong> مناسب انواع خوراک، تفت دادن گوشت و سرخ‌کردنی‌های حجیم.</li>
    <li><strong>دستگیره‌های سیلیکونی نسوز همراه:</strong> جابجایی ایمن و آسان قابلمه‌ها از روی اجاق به روی سفره.</li>
    <li><strong>سازگار با انواع اجاق‌ها:</strong> کارکرد عالی روی اجاق‌های گازی، برقی، سرامیکی و هالوژنی.</li>
</ul>

<h3>جدول مشخصات سرویس قابلمه ۱۱ پارچه اویز پلاس ویولا</h3>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; text-align: right;" border="1">
    <tbody>
        <tr style="background-color: #f8f9fa;">
            <th style="padding: 10px; border: 1px solid #ddd; width: 35%;">مشخصه فنی</th>
            <th style="padding: 10px; border: 1px solid #ddd;">توضیحات و مقادیر</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">برند سازنده</td>
            <td style="padding: 10px; border: 1px solid #ddd;">اویز پلاس (Oviz Plus)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">مدل فنی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">ویولا (Viola 11-Piece)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">تعداد پارچه‌ها</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۱۱ پارچه (۴ قابلمه، ۱ تابه دیواره بلند، ۵ درب پیرکس و دستگیره)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">جنس متریال بدنه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">چدن دایکست با چگالی بالا و ضخامت دیواره ۴.۵ میلی‌متر</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">نوع روکش نچسب</td>
            <td style="padding: 10px; border: 1px solid #ddd;">گرانیت ماربل چندلایه ارگانیک ضد حساسیت</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">درب پیرکس آنتی‌شوک</td>
            <td style="padding: 10px; border: 1px solid #ddd;">دارد (با لبه استیل محافظ و سوپاپ بخار)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">ایمنی بهداشتی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">فاقد PFOA، کادمیوم، سرب و مواد شیمیایی سمی</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">گارانتی و ضمانت</td>
            <td style="padding: 10px; border: 1px solid #ddd;">تضمین سلامت فیزیکی و اصالت کالا در فروشگاه حسینی</td>
        </tr>
    </tbody>
</table>'''
    },

    3354: {
        'title': 'سرویس پخت و پز 10 پارچه تمام استیل لوکس اینداکشن',
        'slug': 'stainless-steel-10pcs-cookware-set',
        'content': '''<h2>بررسی تخصصی سرویس قابلمه ۱۰ پارچه استیل لوکس ضد زنگ</h2>
<p>سرآشپزهای حرفه‌ای در سراسر جهان همواره ظروف استیل را به دلیل ماندگاری مادام‌العمر، بالاترین سطح بهداشت و حفظ طعم واقعی مواد غذایی به هر پوشش دیگری ترجیح می‌دهند. <strong>سرویس پخت و پز ۱۰ پارچه تمام استیل لوکس</strong> از ورق استیل فوق‌مرغوب نگیر با خلوص بالا (Cr-Ni 18/10) ساخته شده که هیچ‌گونه واکنشی با اسیدهای غذایی مانند گوجه‌فرنگی و لیمو نشان نمی‌دهد.</p>

<p>کفه این قابلمه‌ها دارای ساختار ۳ لایه کپسولی (استیل + آلومینیوم فشرده + استیل مغناطیسی) است. این طراحی هوشمندانه نقطه ضعف سنتی استیل را برطرف کرده و گرما را سریع و یکنواخت توزیع می‌کند تا غذا با حرارت ملایم و حفظ کامل املاح و ویتامین‌ها پخته شود. دستگیره‌های ارگونومیک استیل توخالی نیز در حین پخت بر روی گاز خنک می‌مانند و کار با قابلمه‌ها را بسیار ایمن می‌سازند.</p>

<h3>نقاط قوت سرویس ۱۰ پارچه استیل لوکس</h3>
<ul>
    <li><strong>استیل ضد زنگ ضد لک ۱۸/۱۰:</strong> ضد زنگ‌زدگی، ضد پوسته شدن و ضد خش با درخشندگی همیشگی.</li>
    <li><strong>کفه کپسولی ۳ لایه ضخیم:</strong> توزیع بهینه حرارت و سازگاری با تمامی اجاق‌های گازی و اینداکشن برقی.</li>
    <li><strong>حفظ خواص و ویتامین‌های غذا:</strong> ایده‌آل‌ترین گزینه برای پخت سوپ، خورش، حبوبات و غذای کودک.</li>
    <li><strong>دستگیره‌های خنک‌شونده ارگونومیک:</strong> پرچ شده محکم با مقاومت کششی بالا و ایمنی کامل.</li>
    <li><strong>طول عمر مادام‌العمر:</strong> بدون نگرانی از پاک شدن یا خراشیدگی لایه‌های نچسب.</li>
</ul>

<h3>جدول مشخصات فنی سرویس استیل ۱۰ پارچه</h3>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; text-align: right;" border="1">
    <tbody>
        <tr style="background-color: #f8f9fa;">
            <th style="padding: 10px; border: 1px solid #ddd; width: 35%;">مشخصه فنی</th>
            <th style="padding: 10px; border: 1px solid #ddd;">توضیحات و مقادیر</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">نوع کالا</td>
            <td style="padding: 10px; border: 1px solid #ddd;">سرویس پخت و پز ۱۰ پارچه تمام استیل</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">جنس متریال اصلی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">استیل استنلس ۱۸/۱۰ (۳۰۴ نگیر با بالاترین خلوص کروم-نیکل)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">ساختار کفه قابلمه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">کپسولی ۳ لایه با مغزی آلومینیوم جهت هدایت سریع حرارت</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">تعداد پارچه‌ها</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۱۰ پارچه (شامل قابلمه‌ها در سایزهای کاربردی، تابه و درب‌ها)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">جنس درب‌ها</td>
            <td style="padding: 10px; border: 1px solid #ddd;">شیشه نشکن پیرکس با زه استیل و سوپاپ خروج بخار</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">شستشو در ماشین ظرفشویی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۱۰۰٪ مجاز بدون کدر شدن یا لکه‌گیری</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">ضمانت کالا</td>
            <td style="padding: 10px; border: 1px solid #ddd;">تضمین سلامت فیزیکی و اصالت کالا در حسینی کالا</td>
        </tr>
    </tbody>
</table>'''
    }
}

print(f"Loaded Batch 2 enrichment content for {len(PRODUCTS_BATCH2)} products.")

# Update products on site
updated = 0
for pid, data in PRODUCTS_BATCH2.items():
    url = f"https://hosseinykala.ir/wp-json/wp/v2/product/{pid}"
    payload = {
        'title': data['title'],
        'slug': data['slug'],
        'content': data['content']
    }
    try:
        r = requests.post(url, json=payload, auth=AUTH, headers=HEADERS, timeout=20)
        if r.status_code == 200:
            print(f"[SUCCESS] Updated Product {pid}: {data['title'][:35]} -> Words: {len(data['content'].split())}")
            updated += 1
        else:
            print(f"[FAIL] Product {pid} HTTP {r.status_code}: {r.text[:150]}")
    except Exception as e:
        print(f"[ERR] Product {pid}: {e}")
    time.sleep(1)

print(f"\nFinished updating {updated} / {len(PRODUCTS_BATCH2)} Batch 2 products successfully!")
