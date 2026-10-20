import requests
import json
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/json'
}

# 16 Thin Products Content Dictionary
PRODUCTS_ENRICHMENT = {
    3453: {
        'title': 'یخچال فریزر دوقلو 21 فوت الکترواستیل مدل فیوچر (Future)',
        'slug': 'electrosteel-future-twin-refrigerator-21ft',
        'content': '''<h2>بررسی تخصصی یخچال و فریزر دوقلو الکترواستیل مدل فیوچر (Future)</h2>
<p>اگر برای آشپزخانه خود به دنبال یخچالی جادار، مدرن و با دوام فوق‌العاده هستید که سال‌ها بدون افت سرما کار کند، <strong>یخچال فریزر دوقلو الکترواستیل مدل فیوچر (Future)</strong> از خوش‌ساخت‌ترین گزینه‌های بازار ایران است. این محصول با مجموع ظرفیت ۴۲ فوت (۲۱ فوت یخچال و ۲۱ فوت فریزر)، فضای بی‌نظیری را در اختیارتان می‌گذارد تا دیگر هیچ نگرانی بابت جا دادن خریدهای ماهانه، سبزیجات تازه یا بسته‌های بزرگ فریزر نداشته باشید.</p>

<p>الکترواستیل در مدل فیوچر از کمپرسور اروپایی بسیار کم‌صدا و کم‌مصرف استفاده کرده که لرزش دستگاه را به حداقل رسانده است. سیستم گردش هوای چندگانه (Multi Air Flow) سرما را به شکل یکنواخت به تمام طبقات می‌رساند؛ بنابراین میوه‌ها و مواد غذایی در طبقات بالایی و پایینی با کیفیتی کاملاً یکدست تازه می‌مانند. مجهز بودن به آبسردکن و یخساز، نمایشگر لمسی دیجیتال و سیستم کاملاً بدون برفک (No Frost) از دیگر مزایای رقابتی این دوقلوی محبوب است.</p>

<h3>ویژگی‌های برجسته یخچال دوقلو الکترواستیل فیوچر</h3>
<ul>
    <li><strong>سیستم نوفراست ۱۰۰٪:</strong> بدون ذره‌ای تشکیل یخ‌زدگی و برفک در کابین یخچال یا کشوهای فریزر.</li>
    <li><strong>کشوهای نشکن و عمیق:</strong> فریزر مجهز به کشوهای شفاف و مقاوم از جنس پلی‌کربنات مرغوب با دسترسی آسان.</li>
    <li><strong>فیلتر بوگیر و آنتی‌باکتریال:</strong> جلوگیری از پخش شدن بوی مواد غذایی در فضای داخلی یخچال.</li>
    <li><strong>روشنایی LED کم‌مصرف:</strong> نور ملایم و سراسری بدون تولید گرمای اضافی در داخل کابین.</li>
    <li><strong>گارانتی و خدمات رسمی:</strong> ۴۰ ماه ضمانت معتبر شرکت الکترواستیل و ۱۰ سال خدمات پس از فروش در سراسر کشور.</li>
</ul>

<h3>جدول مشخصات فنی یخچال دوقلو الکترواستیل فیوچر</h3>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; text-align: right;" border="1">
    <tbody>
        <tr style="background-color: #f8f9fa;">
            <th style="padding: 10px; border: 1px solid #ddd; width: 35%;">مشخصه فنی</th>
            <th style="padding: 10px; border: 1px solid #ddd;">توضیحات و مقادیر</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">برند سازنده</td>
            <td style="padding: 10px; border: 1px solid #ddd;">الکترواستیل (Electrosteel)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">مدل دستگاه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">فیوچر (Future ESF21 / ESR21)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">ظرفیت اسمی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">مجموعاً ۴۲ فوت (۲۱ فوت یخچال + ۲۱ فوت فریزر)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">نوع سیستم خنک‌کننده</td>
            <td style="padding: 10px; border: 1px solid #ddd;">نوفراست کامل (بدون برفک) با گردش هوای چندگانه</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">رده مصرف انرژی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">+A (فوق‌العاده اقتصادی)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">نوع موتور</td>
            <td style="padding: 10px; border: 1px solid #ddd;">کمپرسور کم‌صدا با گاز مبرد R600a دوستدار محیط زیست</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">تعداد کشوهای فریزر</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۷ کشوی جادار و عمیق به همراه طبقه یخساز</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">رنگ‌بندی بدنه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">سفید چرمی و تیتانیومی ضد لک</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">مدت زمان گارانتی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۴۰ ماه ضمانت رسمی الکترواستیل با نصب رایگان</td>
        </tr>
    </tbody>
</table>'''
    },

    3266: {
        'title': 'کولر گازی اسپلیت دیواری 18000 دور ثابت پاکشوما مدل TPA-18CH',
        'slug': 'pakshoma-18000-split-air-conditioner',
        'content': '''<h2>بررسی تخصصی کولر گازی اسپلیت دیواری ۱۸۰۰۰ پاکشوما مدل TPA-18CH</h2>
<p>تحمل گرمای سوزان تابستان و ایجاد هوای مطبوع در زمستان، نیازمند دستگاهی است که توان بازدهی واقعی داشته باشد. <strong>کولر گازی ۱۸۰۰۰ دور ثابت پاکشوما مدل TPA-18CH</strong> با بهره‌گیری از کمپرسور پرقدرت روتاری و قابلیت دومنظوره سرمایش و گرمایش، فضاهای مسکونی و اداری با مساحت ۲۵ تا ۴۵ مترمربع را در سریع‌ترین زمان ممکن به دمای مطلوب می‌رساند.</p>

<p>پاکشوما در ساخت رادیاتور و کندانسور این اسپلیت از پوشش طلایی <strong>Golden Fin</strong> استفاده کرده است. این فناوری سدی نفوذناپذیر در برابر زنگ‌زدگی، نمک، رطوبت بالا و ذرات معلق هوا ایجاد می‌کند و باعث می‌شود طول عمر مفید دستگاه به ویژه در اقلیم‌های شرجی و گرمسیری نظیر جنوب کشور چند برابر شود. گاز مبرد استاندارد R410a نیز علاوه بر راندمان خنک‌کنندگی سریع‌تر، هیچ آسیبی به لایه ازون وارد نمی‌سازد.</p>

<h3>امکانات برجسته اسپلیت ۱۸۰۰۰ پاکشوما</h3>
<ul>
    <li><strong>پرتاب باد چهارجهته (3D Air Flow):</strong> توزیع یکپارچه جریان باد خنک در تمام زوایای اتاق بدون ایجاد باد موضعی آزاردهنده.</li>
    <li><strong>فیلترهای تصفیه هوای چندلایه:</strong> جذب گردوغبار، ذرات آلرژی‌زا و بوی نامطبوع محیط.</li>
    <li><strong>حالت توربو (Turbo Cooling):</strong> خنک‌سازی فوق‌سریع محیط تنها ظرف چند دقیقه پس از روشن شدن.</li>
    <li><strong>حالت خواب آرام (Sleep Mode):</strong> تنظیم اتوماتیک دما در طول شب جهت کاهش مصرف برق و جلوگیری از سرماخوردگی.</li>
    <li><strong>گارانتی معتبر پاک‌سرویس:</strong> ۵ سال ضمانت کمپرسور و ۱۸ ماه ضمانت قطعات الکترونیکی با شبکه خدمات گسترده.</li>
</ul>

<h3>جدول مشخصات فنی اسپلیت ۱۸۰۰۰ پاکشوما TPA-18CH</h3>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; text-align: right;" border="1">
    <tbody>
        <tr style="background-color: #f8f9fa;">
            <th style="padding: 10px; border: 1px solid #ddd; width: 35%;">مشخصه فنی</th>
            <th style="padding: 10px; border: 1px solid #ddd;">توضیحات و مقادیر</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">برند سازنده</td>
            <td style="padding: 10px; border: 1px solid #ddd;">پاکشوما (Pakshoma)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">مدل فنی دستگاه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">TPA-18CH</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">ظرفیت سرمایش / گرمایش</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۱۸,۰۰۰ BTU/h (سرمایش و گرمایش)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">نوع کمپرسور</td>
            <td style="padding: 10px; border: 1px solid #ddd;">کمپرسور روتاری پرقدرت (Rotary)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">نوع گاز مبرد</td>
            <td style="padding: 10px; border: 1px solid #ddd;">گاز مبرد سازگار با محیط زیست R410a</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">پوشش رادیاتور</td>
            <td style="padding: 10px; border: 1px solid #ddd;">پره‌های طلایی ضد فرسایش (Golden Fin)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">فضای تحت پوشش مناسب</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۲۵ تا ۴۵ مترمربع استاندارد</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">رده مصرف انرژی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Grade A</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">شرایط گارانتی رسمی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۶۰ ماه ضمانت کمپرسور + ۱۸ ماه قطعات پاک‌سرویس</td>
        </tr>
    </tbody>
</table>'''
    },

    3707: {
        'title': 'ماشین لباسشویی دوقلو ۲۱ کیلوگرم نیمه‌اتوماتیک پاکشوما مدل PWT-2154AJ',
        'slug': 'pakshoma-21kg-twin-tub-washer',
        'content': '''<h2>بررسی تخصصی ماشین لباسشویی دوقلو ۲۱ کیلویی پاکشوما مدل PWT-2154AJ</h2>
<p>شستشوی پتوهای دونفره ضخیم، روفرشی‌های سنگین، پرده‌های بلند و حجم زیادی از البسه خانواده‌های پرجمعیت همواره چالش بزرگی در ماشین‌های لباسشویی اتوماتیک معمولی است. <strong>ماشین لباسشویی دوقلو ۲۱ کیلوگرم نیمه‌اتوماتیک پاکشوما مدل PWT-2154AJ</strong> قدرتمندترین و بزرگ‌ترین غول شستشوی خانگی پاکشوماست که این دغدغه را برای همیشه برطرف می‌کند.</p>

<p>این لباسشویی مجهز به دو موتور مجزا با سیم‌پیچی تقویت‌شده است: موتور شستشوی قدرتمند با قابلیت ایجاد گرداب پرفشار آب و موتور خشک‌کن پرسرعت با توان دورگیری فوق‌العاده بالا. بدنه این دستگاه از پلاستیک دولایه فشرده و نشکن ساخته شده که کاملاً در برابر زنگ‌زدگی، پوسیدگی و برق‌گرفتگی در محیط‌های مرطوب (مانند حمام و رختشوی‌خانه) مقاوم است.</p>

<h3>مزایای منحصربه‌فرد لباسشویی ۲۱ کیلویی پاکشوما</h3>
<ul>
    <li><strong>گنجایش شگفت‌انگیز ۲۱ کیلوگرم:</strong> شستشوی آسان همزمان ۲ تخته پتوی دو نفره ضخیم یا کوهی از لباس‌های کار و ورزشی.</li>
    <li><strong>خشک‌کن با قدرت آبگیری ۹۰٪:</strong> دیگ خشک‌کن بزرگ با چرخش پرسرعت جهت آبگیری کامل البسه ضخیم.</li>
    <li><strong>پمپ تخلیه قدرتمند:</strong> تخلیه سریع آب در کمترین زمان بدون نیاز به شیب‌بندی دستی.</li>
    <li><strong>فیلتر جذب پرز البسه:</strong> پاکسازی کامل پرزها و موهای چسبیده به بافت پتو و لباس در حین شستشو.</li>
    <li><strong>گارانتی ۲۴ ماهه پاک‌سرویس:</strong> ضمانت معتبر و پشتیبانی قطعات در سراسر شهرهای ایران.</li>
</ul>

<h3>جدول مشخصات فنی ماشین لباسشویی دوقلو پاکشوما PWT-2154AJ</h3>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; text-align: right;" border="1">
    <tbody>
        <tr style="background-color: #f8f9fa;">
            <th style="padding: 10px; border: 1px solid #ddd; width: 35%;">مشخصه فنی</th>
            <th style="padding: 10px; border: 1px solid #ddd;">توضیحات و مقادیر</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">برند سازنده</td>
            <td style="padding: 10px; border: 1px solid #ddd;">پاکشوما (Pakshoma)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">مدل دستگاه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">PWT-2154AJ</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">ظرفیت مخزن شستشو</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۲۱ کیلوگرم واقعی (پتوشور خانگی و کارگاهی)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">سیستم عملکرد</td>
            <td style="padding: 10px; border: 1px solid #ddd;">نیمه‌اتوماتیک دوقلو (شستشو + خشک‌کن مجزا)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">جنس بدنه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">پلاستیک دولایه فشرده ضد زنگ و ضد برق‌گرفتگی</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">تعداد برنامه‌های شستشو</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۳ برنامه (شستشوی ملایم، معمولی، سنگین و پتو)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">پمپ تخلیه خودکار</td>
            <td style="padding: 10px; border: 1px solid #ddd;">دارد (با خروجی شیلنگ استاندارد)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">گارانتی و خدمات</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۲۴ ماه ضمانت رسمی شرکت پاک‌سرویس</td>
        </tr>
    </tbody>
</table>'''
    },

    3709: {
        'title': 'پتوشور صنعتی و خانگی کد 40 تمام استیل پاکیزان',
        'slug': 'pakizan-40kg-heavy-duty-washer',
        'content': '''<h2>بررسی تخصصی پتوشور خانگی و صنعتی ۴۰ کیلو تمام استیل پاکیزان</h2>
<p>شستن پتوهای سنگین گلبافت، روفرشی‌های ۱۲ متری و البسه پرحجم با دست فشار شدیدی به کمر و زانو وارد می‌کند و استفاده از ماشین‌های اتوماتیک معمولی نیز آسیب‌های سنگینی به دیگ و بلبرینگ آن‌ها وارد می‌سازد. <strong>پتوشور صنعتی و خانگی ۴۰ کیلوگرم تمام استیل پاکیزان</strong> یک دستگاه اختصاصی، جان‌سخت و تمام‌عیار است که برای پاکسازی پرقدرت انواع پتو، روفرشی، ملحفه و پرده طراحی شده است.</p>

<p>بدنه و دیگ این پتوشور به صورت کامل از <strong>ورق استیل ضد زنگ نگیر (Stainless Steel)</strong> با ضخامت مهندسی‌شده ساخته شده که در تماس مداوم با آب، کف صابون و مواد شوینده به هیچ عنوان دچار زنگ‌زدگی یا تغییر رنگ نمی‌شود. موتور پرقدرت این دستگاه با پروانه بزرگ کفی، جریان آب گردابی دوفازی (چپ‌گرد و راست‌گرد) ایجاد می‌کند تا تار و پود ضخیم‌ترین پتوها بدون چروک‌خوردگی کاملاً پاکیزه و تمیز شوند.</p>

<h3>نقاط قوت پتوشور تمام استیل پاکیزان ۴۰ کیلو</h3>
<ul>
    <li><strong>موتور گیربکسی تقویت‌شده:</strong> توان چرخش بالا حتی هنگام بارگذاری کامل پتوهای خیس و سنگین.</li>
    <li><strong>دیگ فوق‌العاده جادار:</strong> گنجایش استاندارد برای شستشوی همزمان ۲ پتوی دونفره یا یک روفرشی ضخیم.</li>
    <li><strong>پایه‌های لرزه‌گیر لاستیکی:</strong> جلوگیری از حرکت و تکان‌های ناگهانی دستگاه در هنگام شستشو.</li>
    <li><strong>شیلنگ تخلیه پرسرعت:</strong> تخلیه آسان پساب با بالاترین سرعت و بدون رسوب‌گیری.</li>
    <li><strong>مناسب مصارف خانگی و نیمه‌صنعتی:</strong> گزینه‌ای ایده‌آل برای منازل بزرگ، اقامتگاه‌ها، هتل‌ها و خشکشویی‌ها.</li>
</ul>

<h3>جدول مشخصات فنی پتوشور تمام استیل پاکیزان ۴۰ کیلو</h3>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; text-align: right;" border="1">
    <tbody>
        <tr style="background-color: #f8f9fa;">
            <th style="padding: 10px; border: 1px solid #ddd; width: 35%;">مشخصه فنی</th>
            <th style="padding: 10px; border: 1px solid #ddd;">توضیحات و مقادیر</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">برند سازنده</td>
            <td style="padding: 10px; border: 1px solid #ddd;">پاکیزان (Pakizan)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">کد و ظرفیت دستگاه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">کد 40 (ظرفیت ۴۰ کیلوگرم اسمی)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">جنس دیگ و بدنه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">تمام استیل ضد زنگ نگیر براق و بهداشتی</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">نوع موتور</td>
            <td style="padding: 10px; border: 1px solid #ddd;">موتور سیم‌پیچ مسی گیربکسی چپ‌گرد و راست‌گرد</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">پروانه شستشو</td>
            <td style="padding: 10px; border: 1px solid #ddd;">پروانه کفی بزرگ فشرده مقاوم در برابر سایش</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">کاربری دستگاه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">شستشوی پتو، روفرشی، پرده، چادر و لباس‌های حجیم</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">سیستم تخلیه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">شیلنگ تخلیه خروجی استاندارد با جریان ثقلی سریع</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">گارانتی و ضمانت</td>
            <td style="padding: 10px; border: 1px solid #ddd;">گارانتی معتبر شرکتی پاکیزان با تضمین سلامت فیزیکی</td>
        </tr>
    </tbody>
</table>'''
    },

    3711: {
        'title': 'آبمیوه‌گیری تک‌کاره ۸۰۰ وات دونالکس مدل DN-120',
        'slug': 'donalex-dn120-single-juicer',
        'content': '''<h2>بررسی تخصصی آبمیوه‌گیری تک‌کاره دونالکس مدل DN-120</h2>
<p>نوشیدن یک لیوان آبمیوه طبیعی و سرشار از ویتامین در شروع روز، انرژی بی‌نظیری به شما می‌بخشد. <strong>آبمیوه‌گیری تک‌کاره ۸۰۰ وات دونالکس مدل DN-120</strong> محصولی خوش‌دست، قدرتمند و با طراحی لوکس ایتالیایی است که منحصراً برای عصاره‌گیری پرسرعت میوه‌ها با بالاترین درصد آبگیری و خشک‌ترین تفاله ممکن مهندسی شده است.</p>

<p>این آبمیوه‌گیری با موتور قدرتمند ۸۰۰ وات و سیم‌پیچی تمام مس، به راحتی از پس میوه‌های سفت مانند سیب، هویج و چغندر برمی‌آید. دهانه ورودی دستگاه با قطر بزرگ XXL طراحی شده تا نیازی به خرد کردن زمان‌بر میوه‌ها نداشته باشید و بتوانید یک سیب یا گلابی درسته را درون دستگاه بیندازید. تیغه‌ها و فیلتر توری از جنس استیل ضد زنگ ۳۰۴ ضد اسید تولید شده‌اند که هیچ‌گونه تغییر طعم یا اکسیداسیونی در آبمیوه ایجاد نمی‌کنند.</p>

<h3>ویژگی‌های کلیدی آبمیوه‌گیری دونالکس DN-120</h3>
<ul>
    <li><strong>دهانه ورودی فوق‌عریض (XXL):</strong> ورود آسان میوه‌های کامل بدون نیاز به تکه تکه کردن قبلی.</li>
    <li><strong>سیستم ضد چکه هوشمند (Anti-Drip):</strong> چرخش خروجی آبمیوه جهت تمیز ماندن پیشخوان آشپزخانه.</li>
    <li><strong>مخزن تفاله‌گیر بزرگ ۲ لیتری:</strong> آبگیری پیوسته حجم زیادی از میوه‌ها بدون نیاز به تخلیه مکرر تفاله.</li>
    <li><strong>پایه‌های ضد لغزش سیلیکونی:</strong> پایداری کامل و جلوگیری از هرگونه لرزش و صدا در بالاترین سرعت.</li>
    <li><strong>۲ سرعته به همراه عملکرد پالس:</strong> تنظیم دقیق سرعت برای میوه‌های نرم (مانند مرکبات و هندوانه) و سخت.</li>
</ul>

<h3>جدول مشخصات فنی آبمیوه‌گیری دونالکس DN-120</h3>
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
            <td style="padding: 10px; border: 1px solid #ddd;">DN-120 Single Juicer</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">توان مصرفی موتور</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۸۰۰ وات واقعی با موتور کم‌صدا و کم‌لرزش</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">جنس تیغه و فیلتر</td>
            <td style="padding: 10px; border: 1px solid #ddd;">استیل ضد زنگ ۳۰۴ ضد اسید با برش لیزری</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">جنس بدنه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">ترکیب استیل مات ضد لک و پلاستیک فشرده ABS</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">ظرفیت مخزن تفاله</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۲ لیتر مجزا با قابلیت جداسازی آسان</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">پارچ آبمیوه همراه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">دارد (۱ لیتر مدرج با جداکننده کف میوه)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">گارانتی رسمی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۲۴ ماه ضمانت معتبر شرکتی دونالکس در حسینی کالا</td>
        </tr>
    </tbody>
</table>'''
    },

    3380: {
        'title': 'اجاق گاز ۵ شعله فردار آلتون مدل MD5S تمام استیل',
        'slug': 'alton-md5s-gas-stove',
        'content': '''<h2>بررسی تخصصی اجاق گاز ۵ شعله مبله فردار آلتون مدل MD5S</h2>
<p>آشپزی اصیل ایرانی نیازمند اجاق گازی است که علاوه بر شعله‌های پرحرارت و باثبات، فری مجهز و جادار برای پخت انواع کیک، شیرینی، پیتزا و کباب‌های لذیذ داشته باشد. <strong>اجاق گاز ۵ شعله فردار آلتون مدل MD5S</strong> با بدنه تمام استیل ضد زنگ و طراحی ایتالیایی، یکی از برترین و بادوام‌ترین شاهکارهای کارخانجات صنعتی آلبا گاز (آلتون) در رده گازهای مبله است.</p>

<p>فر این اجاق گاز به <strong>فن کانوکشن (Convection Fan)</strong> مجهز شده که گرمای یکنواخت را در تمام محفظه به گردش درمی‌آورد و مانع از سوختن زیر غذا یا خام ماندن سطح رویی کیک می‌شود. دو موتور جوجه‌گردان پرقدرت، لعاب داخلی با پوشش سلف‌کلین (آسان‌پاک‌شو)، فندک اتوماتیک سرشعله‌ها و سیستم ترموکوپل فوق‌سریع تاپ‌تایم، استاندارد ایمنی این شاهکار را به سطحی مثال‌زدنی ارتقا داده است.</p>

<h3>امکانات برجسته اجاق گاز مبله آلتون MD5S</h3>
<ul>
    <li><strong>پوشش تمام استیل ضد لک:</strong> بدنه مقاوم و براق که اثر چربی و لکه‌ها به سادگی با یک دستمال نم‌دار از روی آن پاک می‌شود.</li>
    <li><strong>شعله پلوپز وسط پرقدرت:</strong> حرارت متمرکز و یکنواخت جهت پخت ایده‌آل برنج و قابلمه‌های سنگین مهمانی.</li>
    <li><strong>شبکه چدنی یکپارچه سناتور:</strong> پایداری کامل انواع ظروف و عدم لق زدن قابلمه‌ها در حین آشپزی.</li>
    <li><strong>درب فر با شیشه دو جداره جداشونده:</strong> عایق‌بندی حرارتی کامل و امکان شستشوی آسان شیشه‌های داخلی.</li>
    <li><strong>تایمر دیجیتال لمسی:</strong> قابلیت زمان‌بندی دقیق و قطع خودکار شعله پس از اتمام پخت.</li>
</ul>

<h3>جدول مشخصات فنی اجاق گاز آلتون مدل MD5S</h3>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; text-align: right;" border="1">
    <tbody>
        <tr style="background-color: #f8f9fa;">
            <th style="padding: 10px; border: 1px solid #ddd; width: 35%;">مشخصه فنی</th>
            <th style="padding: 10px; border: 1px solid #ddd;">توضیحات و مقادیر</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">برند سازنده</td>
            <td style="padding: 10px; border: 1px solid #ddd;">آلتون (Alton - آلبا گاز)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">مدل دستگاه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">MD5S (مبله ۵ شعله)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">ابعاد بیرونی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">عرض ۹۰ × عمق ۶۰ × ارتفاع ۹۰ سانتی‌متر</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">جنس رویه و بدنه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">تمام استیل ضد زنگ مات با شاسی تقویت‌شده</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">امکانات محفظه فر</td>
            <td style="padding: 10px; border: 1px solid #ddd;">فن کانوکشن، دو سیخ جوجه‌گردان، گریل گازی و لعاب Easy Clean</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">سیستم ایمنی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">ترموکوپل تاپ‌تایم سریع صفر ثانیه روی تمام سرشعله‌ها و فر</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">رده مصرف انرژی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">رده A (فوق‌العاده کم‌مصرف)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">گارانتی و خدمات</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۲۴ ماه ضمانت رسمی آلتون و ۱۰ سال خدمات پس از فروش</td>
        </tr>
    </tbody>
</table>'''
    },

    3383: {
        'title': 'اجاق گاز صفحه ای توکار ۵ شعله آلتون مدل S517N استیل',
        'slug': 'alton-s517n-gas-hob',
        'content': '''<h2>بررسی تخصصی گاز صفحه‌ای توکار آلتون مدل S517N استیل</h2>
<p>آشپزخانه‌های امروزی با گازهای توکار استیل جلوه‌ای فوق‌العاده مدرن، خلوت و چشم‌نواز پیدا می‌کنند. <strong>اجاق گاز صفحه‌ای ۵ شعله آلتون مدل S517N</strong> با طراحی ارگونومیک، ابعاد استاندارد ۹۰ سانتی‌متری و استیل مرغوب ضد خش، انتخابی بی‌نظیر برای افرادی است که کیفیت ساخت سرشعله‌ها و تمیزی آسان صفحه برایشان اولویت اصلی است.</p>

<p>آلتون در مدل S517N سرشعله‌های پرقدرت با راندمان حرارتی بالا را در کنار شعله پلوپز مرکزی قرار داده تا بتوانید بدون افت فشار گاز، ظروف بزرگ برنج یا ماهیتابه‌های سنگین را روی آن قرار دهید. سطح استیل مقاوم دستگاه با فینیش ضد لک نانو پرداخت شده و چدن‌های یکپارچه لعاب‌دار آن به راحتی در ماشین ظرفشویی قابل شستشو هستند. سیستم ایمنی ترموکوپل فوق‌سریع کستل ایتالیا نیز آرامش خاطر کامل را در هنگام قطع احتمالی گاز یا سر رفتن شیر فراهم می‌سازد.</p>

<h3>مزایای گاز توکار ۵ شعله آلتون S517N</h3>
<ul>
    <li><strong>صفحه استیل ضد زنگ AISI 304:</strong> مقاومت فوق‌العاده در برابر خط‌وخش، حرارت مستقیم و مواد اسیدی آشپزخانه.</li>
    <li><strong>ترموکوپل تاپ‌تایم صفر ثانیه:</strong> قطع بلافاصله جریان گاز در صورت خاموش شدن اتفاقی شعله با باد یا سرریز مایعات.</li>
    <li><strong>پلوپز پرقدرت ۳.۸ کیلووات:</strong> توان حرارتی ایده‌آل برای جوش آوردن سریع آب و سرخ کردن تند مواد غذایی.</li>
    <li><strong>شبکه چدنی داکتیل مقاوم:</strong> تحمل وزن سنگین‌ترین قابلمه‌ها بدون تغییر فرم و رنگ.</li>
    <li><strong>فندک اتوماتیک تعبیه‌شده در ولوم:</strong> روشن شدن سریع شعله‌ها تنها با چرخاندن ملایم دستگیره.</li>
</ul>

<h3>جدول مشخصات فنی گاز صفحه‌ای آلتون S517N</h3>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; text-align: right;" border="1">
    <tbody>
        <tr style="background-color: #f8f9fa;">
            <th style="padding: 10px; border: 1px solid #ddd; width: 35%;">مشخصه فنی</th>
            <th style="padding: 10px; border: 1px solid #ddd;">توضیحات و مقادیر</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">برند سازنده</td>
            <td style="padding: 10px; border: 1px solid #ddd;">آلتون (Alton)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">مدل فنی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">S517N (توکار صفحه استیل)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">ابعاد محصول</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۹۰ در ۵۰ سانتی‌متر (ابعاد برش: ۸۷.۴ در ۴۷.۴ سانتی‌متر)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">تعداد شعله‌ها</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۵ شعله (پلوپز، بزرگ، ۲ متوسط، کوچک)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">موقعیت شعله پلوپز</td>
            <td style="padding: 10px; border: 1px solid #ddd;">مرکز با توان حرارتی ماکسیمم ۳.۸ کیلووات</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">جنس شبکه</td>
            <td style="padding: 10px; border: 1px solid #ddd;">چدن داکتیل لعاب‌دار مقاوم در برابر شوک حرارتی</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">نوع سرشعله‌ها</td>
            <td style="padding: 10px; border: 1px solid #ddd;">سرشعله‌های راندمان بالا با احتراق کامل گاز</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">گارانتی رسمی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۲۴ ماه ضمانت آلبا گاز با نصب رایگان</td>
        </tr>
    </tbody>
</table>'''
    },

    3389: {
        'title': 'یخچال و فریزر 24 فوت بست مدل BRB241-10 نوفراست',
        'slug': 'bost-brb241-refrigerator-freezer',
        'content': '''<h2>بررسی تخصصی یخچال و فریزر ۲۴ فوت کمبی بست مدل BRB241-10</h2>
<p>برای خانواده‌های کم‌جمعیت، زوج‌های جوان یا منازلی که فضای آشپزخانه محدودی دارند، انتخاب یخچالی که هم جای کمی بگیرد و هم سرمایش باکیفیتی داشته باشد اهمیت زیادی دارد. <strong>یخچال و فریزر ۲۴ فوت بست مدل BRB241-10</strong> از محبوب‌ترین محصولات اقتصادی گروه صنعتی انتخاب الکترونیک (تولیدکننده اسنوا و دوو) است که ترکیبی هوشمندانه از قیمت منصفانه، کیفیت ساخت بالا و کارایی تضمین‌شده را ارائه می‌دهد.</p>

<p>طراحی این یخچال به صورت کمبی (فریزر در پایین و یخچال در بالا) است که باعث دسترسی آسان و ارگونومیک به مواد پرمصرف روزانه بدون نیاز به خم شدن می‌شود. سیستم سرمایش این دستگاه ۱۰۰٪ بدون برفک (No Frost) بوده و فن گردش هوای هوشمند تعبیه‌شده در کابین، رطوبت مورد نیاز میوه‌ها و سبزیجات را حفظ می‌کند. موتور دستگاه از نوع بهینه‌سازی‌شده کم‌صدا است که مصرف انرژی آن در رده +A قرار دارد.</p>

<h3>مزایای یخچال ۲۴ فوت بست مدل BRB241-10</h3>
<ul>
    <li><strong>سیستم نوفراست واقعی:</strong> خداحافظی همیشگی با دردسرهای آب کردن یخ و برفک فریزر.</li>
    <li><strong>کشوهای فریزر ریلی مقاوم:</strong> چهار کشوی جادار از جنس پلاستیک نشکن بهداشتی برای دسته‌بندی مواد پروتئینی و سبزیجات.</li>
    <li><strong>آبسردکن باریک روی درب:</strong> دسترسی همیشگی به آب خنک بدون اتلاف سرمای درون یخچال.</li>
    <li><strong>نوار درزگیر آنتی‌باکتریال:</strong> جلوگیری از نفوذ میکروب‌ها، بوی نامطبوع و گردوغبار به داخل کابین.</li>
    <li><strong>پشتیبانی قدرتمند انتخاب الکترونیک:</strong> ۲۴ ماه ضمانت کلی و ۶۰ ماه ضمانت کمپرسور با سراسری‌ترین شبکه خدمات در کشور.</li>
</ul>

<h3>جدول مشخصات فنی یخچال ۲۴ فوت بست BRB241-10</h3>
<table style="width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; text-align: right;" border="1">
    <tbody>
        <tr style="background-color: #f8f9fa;">
            <th style="padding: 10px; border: 1px solid #ddd; width: 35%;">مشخصه فنی</th>
            <th style="padding: 10px; border: 1px solid #ddd;">توضیحات و مقادیر</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">برند سازنده</td>
            <td style="padding: 10px; border: 1px solid #ddd;">بُست (BOST - گروه انتخاب الکترونیک)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">مدل فنی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">BRB241-10 (کمبی فریزر پایین)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">ظرفیت اسمی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۲۴ فوت مفید (مناسب خانواده‌های ۲ تا ۴ نفره)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">سیستم خنک‌کننده</td>
            <td style="padding: 10px; border: 1px solid #ddd;">نوفراست کامل (بدون برفک) با فن یکنواخت‌ساز</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">رده مصرف انرژی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">+A (فوق‌العاده کم‌مصرف)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">تعداد کشوهای فریزر</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۴ کشوی ریلی عمیق</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">تجهیزات جانبی</td>
            <td style="padding: 10px; border: 1px solid #ddd;">آبسردکن مخزنی دستی، طبقات شیشه‌ای سکوریت نشکن</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">ضمانت و خدمات</td>
            <td style="padding: 10px; border: 1px solid #ddd;">۲۴ ماه ضمانت قطعات + ۶۰ ماه ضمانت کمپرسور انتخاب سرویس</td>
        </tr>
    </tbody>
</table>'''
    }
}

print(f"Loaded enrichment content for {len(PRODUCTS_ENRICHMENT)} critical products.")

# Update products on site
updated = 0
for pid, data in PRODUCTS_ENRICHMENT.items():
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

print(f"\nFinished updating {updated} / {len(PRODUCTS_ENRICHMENT)} products successfully!")
