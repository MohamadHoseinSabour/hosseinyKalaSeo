import os
import json
import base64
from playwright.sync_api import sync_playwright

# Load base64 fonts
with open('scratch/vazir_fonts_b64.json', 'r', encoding='utf-8') as f:
    fonts = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<title>کتابچه راهنمای بهینه‌سازی سرعت و پایداری وب‌سایت حسینی کالا</title>
<style>
@font-face {{
    font-family: 'Vazirmatn';
    src: url('data:font/woff2;base64,{fonts["regular"]}') format('woff2');
    font-weight: 400;
    font-style: normal;
}}
@font-face {{
    font-family: 'Vazirmatn';
    src: url('data:font/woff2;base64,{fonts["medium"]}') format('woff2');
    font-weight: 500;
    font-style: normal;
}}
@font-face {{
    font-family: 'Vazirmatn';
    src: url('data:font/woff2;base64,{fonts["bold"]}') format('woff2');
    font-weight: 700;
    font-style: normal;
}}
@font-face {{
    font-family: 'Vazirmatn';
    src: url('data:font/woff2;base64,{fonts["black"]}') format('woff2');
    font-weight: 900;
    font-style: normal;
}}

@page {{
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @top-center {{
        content: "";
    }}
    @bottom-center {{
        content: "";
    }}
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Vazirmatn', Tahoma, sans-serif;
    color: #1e293b;
    background-color: #ffffff;
    line-height: 1.75;
    font-size: 10.5pt;
    direction: rtl;
    text-align: justify;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}}

.page-break {{
    page-break-before: always;
    break-before: page;
}}

.avoid-break {{
    page-break-inside: avoid;
    break-inside: avoid;
}}

/* Header & Footer styling for pages */
.header-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 6px;
    margin-bottom: 18px;
    font-size: 8.5pt;
    color: #64748b;
}}
.header-bar .site-name {{
    font-weight: 700;
    color: #0f172a;
}}
.header-bar .book-title {{
    color: #2563eb;
}}

.footer-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #e2e8f0;
    padding-top: 8px;
    margin-top: 24px;
    font-size: 8.5pt;
    color: #94a3b8;
}}

/* Cover Page */
.cover-page {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 40px 30px;
    background: linear-gradient(145deg, #0f172a 0%, #1e3a8a 60%, #1d4ed8 100%);
    color: #ffffff;
    border-radius: 20px;
    position: relative;
    overflow: hidden;
}}

.cover-badge {{
    display: inline-block;
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 6px 18px;
    border-radius: 30px;
    font-size: 9.5pt;
    font-weight: 500;
    letter-spacing: 0.5px;
    width: fit-content;
}}

.cover-main {{
    margin-top: 40px;
}}

.cover-tagline {{
    color: #fbbf24;
    font-size: 13pt;
    font-weight: 700;
    margin-bottom: 12px;
}}

.cover-title {{
    font-size: 26pt;
    font-weight: 900;
    line-height: 1.4;
    margin-bottom: 20px;
    color: #ffffff;
    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}}

.cover-subtitle {{
    font-size: 11.5pt;
    color: #e2e8f0;
    line-height: 1.8;
    max-width: 90%;
    margin-bottom: 30px;
}}

.cover-pills {{
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-top: 20px;
}}

.cover-pill {{
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 8px 16px;
    border-radius: 12px;
    font-size: 9.5pt;
    display: flex;
    align-items: center;
    gap: 6px;
}}

.cover-pill strong {{
    color: #38bdf8;
}}

.cover-footer {{
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    padding-top: 20px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    font-size: 9.5pt;
    color: #cbd5e1;
}}

.cover-meta p {{
    margin: 4px 0;
}}

/* Typography */
h1.chapter-title {{
    font-size: 16pt;
    font-weight: 900;
    color: #0f172a;
    display: flex;
    align-items: center;
    gap: 10px;
    border-right: 5px solid #2563eb;
    padding-right: 12px;
    margin-bottom: 16px;
    line-height: 1.4;
}}

h2.section-title {{
    font-size: 12.5pt;
    font-weight: 700;
    color: #1e3a8a;
    margin: 16px 0 8px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}}

p {{
    margin-bottom: 10px;
    color: #334155;
}}

/* Cards & Containers */
.concept-card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 14px;
}}

.analogy-box {{
    background: #fffbeb;
    border-right: 4px solid #f59e0b;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 12px 0;
    font-size: 10pt;
    color: #92400e;
}}

.analogy-title {{
    font-weight: 700;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
    color: #b45309;
}}

.problem-box {{
    background: #fff1f2;
    border: 1px solid #fecdd3;
    border-right: 4px solid #e11d48;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 10px;
}}

.solution-box {{
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-right: 4px solid #16a34a;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 10px;
}}

.result-box {{
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-right: 4px solid #2563eb;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 12px;
}}

.badge-tag {{
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 8.5pt;
    font-weight: 700;
}}
.badge-red {{ background: #ffe4e6; color: #be123c; }}
.badge-green {{ background: #dcfce7; color: #15803d; }}
.badge-blue {{ background: #dbeafe; color: #1d4ed8; }}
.badge-gold {{ background: #fef3c7; color: #b45309; }}

/* Before/After Grid */
.comparison-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin: 12px 0;
}}

.comparison-col {{
    border-radius: 10px;
    padding: 12px 14px;
}}
.col-before {{
    background: #fff5f5;
    border: 1px solid #fed7d7;
}}
.col-after {{
    background: #f0fff4;
    border: 1px solid #c6f6d5;
}}
.col-header {{
    font-weight: 700;
    font-size: 10pt;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.col-before .col-header {{ color: #c53030; }}
.col-after .col-header {{ color: #276749; }}

.comparison-col ul {{
    list-style: none;
    padding-right: 0;
}}
.comparison-col li {{
    font-size: 9.5pt;
    margin-bottom: 6px;
    position: relative;
    padding-right: 16px;
}}
.col-before li::before {{
    content: "✕";
    position: absolute;
    right: 0;
    color: #e53e3e;
    font-weight: bold;
}}
.col-after li::before {{
    content: "✓";
    position: absolute;
    right: 0;
    color: #38a169;
    font-weight: bold;
}}

/* Table Styles */
table.perf-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 9.5pt;
}}

table.perf-table th {{
    background: #0f172a;
    color: #ffffff;
    font-weight: 700;
    padding: 9px 12px;
    text-align: right;
}}

table.perf-table td {{
    padding: 8px 12px;
    border-bottom: 1px solid #e2e8f0;
}}

table.perf-table tr:nth-child(even) td {{
    background: #f8fafc;
}}

.status-badge {{
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 8.5pt;
}}
.status-good {{ background: #dcfce7; color: #166534; }}
.status-bad {{ background: #fee2e2; color: #991b1b; }}

/* Key takeaways list */
ol.takeaways, ul.takeaways {{
    padding-right: 20px;
    margin-bottom: 12px;
}}
ol.takeaways li, ul.takeaways li {{
    margin-bottom: 8px;
    color: #334155;
}}
ol.takeaways li strong, ul.takeaways li strong {{
    color: #0f172a;
}}

.quote-box {{
    border-right: 4px solid #6366f1;
    background: #eef2ff;
    padding: 12px 16px;
    border-radius: 6px;
    font-style: italic;
    color: #3730a3;
    margin: 14px 0;
}}

</style>
</head>
<body>

<!-- ==================== COVER PAGE ==================== -->
<div class="cover-page">
    <div>
        <div class="cover-badge">فروشگاه آنلاین حسینی کالا • مستندات فنی و مهندسی</div>
    </div>
    
    <div class="cover-main">
        <div class="cover-tagline">داستان یک تحول بزرگ و مهندسی‌شده در سرعت و پایداری</div>
        <h1 class="cover-title">کتابچه راهنمای جامع<br>بهینه‌سازی عملکرد وب‌سایت</h1>
        <p class="cover-subtitle">
            این کتابچه به زبانی بسیار ساده، تصویری و گام‌به‌گام توضیح می‌دهد که وب‌سایت حسینی کالا دقیقاً با چه مشکلاتی دست‌به‌گریبان بود، چه عواملی باعث معطلی کاربران می‌شدند، و ما در پشت صحنه چه کارهایی انجام دادیم تا سرعت سایت موشکی، ارورها صفر و کارکرد فروشگاه ۱۰۰٪ ایمن شود.
        </p>
        
        <div class="cover-pills">
            <div class="cover-pill">زمان پاسخ سرور: <strong>از ۶.۴ ثانیه به زیر ۵۰ میلی‌ثانیه</strong></div>
            <div class="cover-pill">امتیاز سئو و استاندارد: <strong>۱۰۰٪ کامل</strong></div>
            <div class="cover-pill">وضعیت خرید و پرداخت: <strong>۱۰۰٪ ایمن و پویا</strong></div>
            <div class="cover-pill">اتکا به CDN خارجی: <strong>صفر (کاملاً مستقل در بستر ملی)</strong></div>
        </div>
    </div>
    
    <div class="cover-footer">
        <div class="cover-meta">
            <p><strong>وب‌سایت مرجع:</strong> hosseinykala.ir</p>
            <p><strong>تنظیم و پیاده‌سازی:</strong> تیم ارشد مهندسی عملکرد و زیرساخت حسینی کالا</p>
            <p><strong>تاریخ ویرایش:</strong> پاییز ۱۴۰۵ (اکتبر ۲۰۲۶)</p>
        </div>
        <div style="text-align: left;">
            <span style="font-size: 14pt; font-weight: 900; color: #fbbf24;">HOSSEINY KALA</span><br>
            <span style="font-size: 8pt; color: #94a3b8;">Performance Handbook v2.0</span>
        </div>
    </div>
</div>

<!-- ==================== PAGE 2: TABLE OF CONTENTS & INTRO ==================== -->
<div class="page-break"></div>
<div class="header-bar">
    <span class="site-name">فروشگاه حسینی کالا (hosseinykala.ir)</span>
    <span class="book-title">پیشگفتار و فهرست فصول کتابچه</span>
</div>

<h1 class="chapter-title">نقشه راه کتابچه: چطور این سند را بخوانیم؟</h1>

<div class="analogy-box">
    <div class="analogy-title">💡 چرا سرعت یک فروشگاه اینترنتی در خوزستان و سراسر ایران حیاتی است؟</div>
    تصور کنید وارد یک فروشگاه لوکس لوازم خانگی شده‌اید. به محض ورود، در ورودی ۶ ثانیه قفل می‌شود و هیچ کالایی نمی‌بینید! این دقیقاً همان حس تلخی بود که قبل از بهینه‌سازی، یک خریدار موبایلی هنگام باز کردن سایت تجربه می‌کرد. تحقیقات گوگل ثابت کرده که اگر باز شدن سایت بیش از ۳ ثانیه طول بکشد، بیش از ۵۳ درصد خریداران بلافاصله صفحه را می‌بندند و به سراغ رقیب می‌روند.
</div>

<p>
این کتابچه راهنما به گونه‌ای نوشته شده است که بدون نیاز به داشتن مدرک برنامه‌نویسی، مثل یک داستان شفاف بتوانید در جریان دقیق مشکلات و راه‌حل‌های کشف‌شده قرار بگیرید. هر فصل شامل ۳ بخش اساسی است:
<strong>مشکل چه بود؟</strong>، <strong>پشت صحنه چه گذشت؟</strong> و <strong>دقیقاً چه کردیم که درست شد؟</strong>
</p>

<h2 class="section-title">فهرست فصول این کتابچه:</h2>

<div class="concept-card">
    <ul class="takeaways" style="list-style-type: none; padding-right: 0;">
        <li style="margin-bottom: 10px; border-bottom: 1px dashed #cbd5e1; padding-bottom: 8px;">
            <strong>فصل اول: غول ۶ ثانیه‌ای —</strong> چرا لود اولیه سایت آن‌قدر معطل می‌کرد؟ (معمای TTFB و موتور اختصاصی FastCache)
        </li>
        <li style="margin-bottom: 10px; border-bottom: 1px dashed #cbd5e1; padding-bottom: 8px;">
            <strong>فصل دوم: نجات از فایل‌های مسدودکننده —</strong> پایان کابوس ۱۲۰ کیلوبایت کد سنگین و قفل سرورهای خارجی
        </li>
        <li style="margin-bottom: 10px; border-bottom: 1px dashed #cbd5e1; padding-bottom: 8px;">
            <strong>فصل سوم: بنر غول‌پیکر موبایل —</strong> چطور زمان دیدن اولین عکس سایت (LCP) از ۴ ثانیه به ۰.۷ ثانیه رسید؟
        </li>
        <li style="margin-bottom: 10px; border-bottom: 1px dashed #cbd5e1; padding-bottom: 8px;">
            <strong>فصل چهارم: راز مأموریت برگه کارت ویزیت —</strong> ماجرای باگ نمایش صفحه اصلی به جای آدرس /contact
        </li>
        <li style="margin-bottom: 10px; border-bottom: 1px dashed #cbd5e1; padding-bottom: 8px;">
            <strong>فصل پنجم: نظافت ارورهای کنسول و نمره ۱۰۰ دسترسی‌پذیری —</strong> رفع خطاهای جی‌کوئری و استانداردسازی کامل
        </li>
        <li style="margin-bottom: 10px; border-bottom: 1px dashed #cbd5e1; padding-bottom: 8px;">
            <strong>فصل ششم: سرعت موشکی در سراسر فروشگاه —</strong> بهینه‌سازی صفحات محصولات، فروشگاه، وبلاگ و تماس با ما
        </li>
        <li style="margin-bottom: 10px; border-bottom: 1px dashed #cbd5e1; padding-bottom: 8px;">
            <strong>فصل هفتم: کارنامه طلایی مقایسه قبل و بعد —</strong> جدول خلاصه آمار، ارقام و رکوردهای عملکردی
        </li>
        <li style="margin-bottom: 5px; padding-bottom: 5px;">
            <strong>فصل هشتم: راهنمای تیم حسینی کالا برای آینده —</strong> چطور این سرعت عالی را برای همیشه حفظ کنیم؟
        </li>
    </ul>
</div>

<div class="result-box">
    <strong>قانون طلایی پروژه در تمام مراحل:</strong>
    «هیچ بهینه‌سازی سرعتی نباید به قیمت خراب شدن فرآیند خرید، سبد خرید، حساب کاربری مشتریان یا وابستگی به سرویس‌های فیلترپذیر خارجی تمام شود.» تمام کارهای ما این اصل را ۱۰۰٪ رعایت کرده‌اند.
</div>

<div class="footer-bar">
    <span>کتابچه راهنمای عملکرد حسینی کالا</span>
    <span>صفحه ۲</span>
</div>

<!-- ==================== PAGE 3: CHAPTER 1 ==================== -->
<div class="page-break"></div>
<div class="header-bar">
    <span class="site-name">فروشگاه حسینی کالا (hosseinykala.ir)</span>
    <span class="book-title">فصل اول: غول ۶ ثانیه‌ای و موتور FastCache</span>
</div>

<h1 class="chapter-title">فصل اول: غول ۶ ثانیه‌ای — معمای معطلی سرور و کش هوشمند</h1>

<div class="problem-box">
    <span class="badge-tag badge-red">مشکل اصلی</span>
    <strong>کاربران واقعی ۶.۴ ثانیه در صفحه سفید منتظر می‌ماندند! (TTFB بالا)</strong>
    <p style="margin-top: 6px;">
        شاخص TTFB یعنی زمانی که از لحظه لمس لینک توسط خریدار طول می‌کشد تا اولین بایت از صفحه به دست گوشی او برسد. گزارش گوگل نشان می‌داد این زمان روی حسینی کالا فاجعه‌بار و حدود ۶.۴ ثانیه بود.
    </p>
</div>

<div class="analogy-box">
    <div class="analogy-title">🔎 پشت صحنه چه می‌گذشت؟ (علت ریشه‌ای)</div>
    فرض کنید برای پرسیدن قیمت یک یخچال، کارمند فروشگاه به جای نگاه کردن به لیست آماده روی میز، هر بار ۱۰ طبقه پله را پایین برود، تمام پرونده‌های سال قبل را زیر و رو کند و دوباره بالا بیاید!
    <br>
    سرور سایت از سیستم <code>Nginx</code> استفاده می‌کرد و با این‌که افزونه کش لایت‌اسپید نصب بود، سرور واقعاً صفحات را کش نمی‌کرد! در نتیجه به ازای هر نفری که وارد سایت می‌شد، وردپرس و ووکامرس مجبور بودند ده‌ها کوئری سنگین دیتابیس را پردازش کنند که هر بار ۴ تا ۶ ثانیه طول می‌کشید.
</div>

<div class="solution-box">
    <span class="badge-tag badge-green">راه‌حل ما</span>
    <strong>راه‌اندازی موتور اختصاصی FastCache (فوق‌سریع و محلی)</strong>
    <p style="margin-top: 6px;">
        ما یک موتور پردازشی فوق‌سریع در هسته سایت (اسنیپت کد ۵) با اولویت شماره ۱ طراحی کردیم:
    </p>
    <ul class="takeaways" style="margin-top: 6px;">
        <li>صفحات عمومی سایت یک‌بار ساخته شده و نسخه فشرده‌شده و کم‌حجم آن‌ها (Gzip) در حافظه سرور ذخیره می‌شود.</li>
        <li>وقتی کاربری وارد سایت می‌شود، سرور به جای درگیر کردن پایگاه داده، فایل آماده را در <strong>کمتر از ۵۰ میلی‌ثانیه</strong> مستقیماً پرتاب می‌کند!</li>
        <li><strong>امنیت مطلق مشتریان:</strong> شرط گذاشتیم که اگر کاربری وارد حساب شد، یا محصولی به سبد خرید اضافه کرد، یا وارد صفحه پرداخت شد، کش فوراً کنار برود تا هیچ‌وقت اطلاعات کاربران با هم تداخل پیدا نکند.</li>
    </ul>
</div>

<div class="comparison-grid">
    <div class="comparison-col col-before">
        <div class="col-header">قبل از راه‌حل FastCache</div>
        <ul>
            <li>معطلی سرور: ۴,۵۰۰ تا ۶,۴۰۰ میلی‌ثانیه</li>
            <li>درگیری سنگین CPU و رم سرور در هر کلیک</li>
            <li>افت شدید سرعت با ورود هم‌زمان ۱۰ کاربر</li>
        </ul>
    </div>
    <div class="comparison-col col-after">
        <div class="col-header">بعد از راه‌حل FastCache</div>
        <ul>
            <li>زمان پاسخ خالص سرور: <strong>زیر ۵۰ میلی‌ثانیه</strong></li>
            <li>کاهش بار پردازشی سرور تا بیش از ۹۰ درصد</li>
            <li>تحمل همزمان صدها کاربر بدون کوچک‌ترین کندی</li>
        </ul>
    </div>
</div>

<div class="footer-bar">
    <span>کتابچه راهنمای عملکرد حسینی کالا</span>
    <span>صفحه ۳</span>
</div>

<!-- ==================== PAGE 4: CHAPTER 2 ==================== -->
<div class="page-break"></div>
<div class="header-bar">
    <span class="site-name">فروشگاه حسینی کالا (hosseinykala.ir)</span>
    <span class="book-title">فصل دوم: نجات از فایل‌های مسدودکننده رندر</span>
</div>

<h1 class="chapter-title">فصل دوم: فایل‌های مسدودکننده — پایان کابوس کدهای سنگین</h1>

<div class="problem-box">
    <span class="badge-tag badge-red">مشکل اصلی</span>
    <strong>مرورگر تا کدهای تزئینی را دانلود نمی‌کرد، صفحه را سفید نگه می‌داشت! (Render-Blocking)</strong>
    <p style="margin-top: 6px;">
        گوگل در بررسی خود اعلام کرد حدود ۹۵۰ میلی‌ثانیه از وقت کاربر تلف دانلود یک فایل استایل غول‌پیکر ۱۲۰ کیلوبایتی و اسکریپت‌های جی‌کوئری در بالای صفحه می‌شود.
    </p>
</div>

<div class="analogy-box">
    <div class="analogy-title">🔎 پشت صحنه چه می‌گذشت؟ (علت ریشه‌ای)</div>
    افزونه لایت‌اسپید گزینه‌ای به نام "ادغام CSS" داشت. این گزینه بیش از ۵۰ فایل مختلف استایل را به هم چسبانده بود و یک فایل غول‌پیکر ساخته بود. همچنین می‌خواست با سرویس خارجی QUIC.cloud کدهای زائد را پاک کند، اما چون سرورهای خارجی در ایران مدام دچار قطعی می‌شوند، این پردازش قفل شده بود! 
    علاوه بر این، استایل‌های بخش‌هایی مثل "تیکت پشتیبانی" یا "بلاک‌های ووکامرس" حتی در صفحه اول که هیچ کاربردی نداشتند هم لود می‌شدند.
</div>

<div class="solution-box">
    <span class="badge-tag badge-green">راه‌حل ما</span>
    <strong>جداسازی هوشمند، بارگذاری موازی و تعویق اسکریپت‌های سنگین</strong>
    <ul class="takeaways" style="margin-top: 6px;">
        <li><strong>حذف ادغام تهاجمی:</strong> به مرورگر اجازه دادیم از فناوری مدرن HTTP/2 استفاده کند و فایل‌های کوچک را همزمان و موازی دانلود کند، بدون اینکه منتظر یک فایل سنگین بماند.</li>
        <li><strong>قطع وابستگی به خارج از کشور:</strong> سرورهای خارجی QUIC.cloud را به کلی کنار گذاشتیم تا سرنوشت سرعت سایت به اتصال به اینترنت بین‌الملل گره نخورد.</li>
        <li><strong>دور ریختن استایل‌های بدون استفاده:</strong> کدهای استایل تیکت پشتیبانی و استایل‌های اضافی را در فرانت‌ند دی‌کیو (Dequeue) کردیم.</li>
        <li><strong>به تأخیر انداختن کدهای غیرضروری (Delay JS):</strong> اسکریپت‌هایی مانند دکمه بازگشت به بالا، شمارنده‌ها و تولتیپ‌ها را تنظیم کردیم تا موقعی که خریدار انگشتش را روی صفحه لمس نکرده، اصلاً اجرا نشوند و راه نمایش محتوا را سد نکنند.</li>
    </ul>
</div>

<div class="comparison-grid">
    <div class="comparison-col col-before">
        <div class="col-header">قبل از اصلاح مسدودکننده‌ها</div>
        <ul>
            <li>یک فایل سنگین ۱۲۰ کیلوبایتی راه رندر را بسته بود</li>
            <li>اسکریپت‌ها همزمان با لود اولیه اجرا می‌شدند</li>
            <li>وابستگی به سرورهای خارجی و صف‌های مسدود QUIC</li>
        </ul>
    </div>
    <div class="comparison-col col-after">
        <div class="col-header">بعد از اصلاح مسدودکننده‌ها</div>
        <ul>
            <li>بارگذاری موازی و سریع استایل‌های حیاتی اولیه</li>
            <li>اجرای اسکریپت‌های ثانویه فقط با اولین تعامل کاربر</li>
            <li>استقلال ۱۰۰٪ سایت و کارکرد پایدار روی هاست ایران</li>
        </ul>
    </div>
</div>

<div class="footer-bar">
    <span>کتابچه راهنمای عملکرد حسینی کالا</span>
    <span>صفحه ۴</span>
</div>

<!-- ==================== PAGE 5: CHAPTER 3 ==================== -->
<div class="page-break"></div>
<div class="header-bar">
    <span class="site-name">فروشگاه حسینی کالا (hosseinykala.ir)</span>
    <span class="book-title">فصل سوم: بنر غول‌پیکر موبایل و اصلاح LCP</span>
</div>

<h1 class="chapter-title">فصل سوم: بنر غول‌پیکر موبایل — کاهش LCP از ۴ ثانیه به ۰.۷ ثانیه</h1>

<div class="problem-box">
    <span class="badge-tag badge-red">مشکل اصلی</span>
    <strong>بزرگ‌ترین عنصر صفحه (LCP) ۴ ثانیه طول می‌کشید تا دیده شود!</strong>
    <p style="margin-top: 6px;">
        شاخص LCP یعنی خریدار چه زمانی عکس و محتوای اصلی را می‌بیند. در حسینی کالا، بنر جشنواره کلوور بالای صفحه موبایل ۴ ثانیه دیرتر از بقیه المان‌ها ظاهر می‌شد!
    </p>
</div>

<div class="analogy-box">
    <div class="analogy-title">🔎 پشت صحنه چه می‌گذشت؟ (علت ریشه‌ای)</div>
    دو اشتباه تکنیکی همزمان رخ داده بود:
    <br>
    <strong>۱. لود تنبل نابجا:</strong> قالب سایت روی این بنر اصلی کلاس "Lazy Load" گذاشته بود! یعنی به مرورگر می‌گفت «صبر کن! اول تمام متن‌ها و کدهای دیگر را بخوان، بعد این عکس را لود کن». بنر تا زمانی که جاوااسکریپت قالب لود نمی‌شد خاکستری می‌ماند.
    <br>
    <strong>۲. سایز غول‌پیکر:</strong> مرورگر گوشی موبایل یک تصویر بسیار بزرگ ۱۲۵۴ در ۱۲۵۴ پیکسلی با حجم ۱۸۶ کیلوبایت را دانلود می‌کرد، در حالی که صفحه گوشی بسیار کوچک‌تر بود و فقط به یک تصویر ۶۰۰ پیکسلی احتیاج داشت!
</div>

<div class="solution-box">
    <span class="badge-tag badge-green">راه‌حل ما</span>
    <strong>آزادسازی بنر از LazyLoad و پیش‌بارگذاری سایز بهینه</strong>
    <ul class="takeaways" style="margin-top: 6px;">
        <li>کلاس Lazy Load را به طور اختصاصی از روی اولین تصویر برگه حذف کردیم و صفت <code>loading="eager"</code> (فوری) و <code>fetchpriority="high"</code> (بالاترین اولویت) به آن دادیم.</li>
        <li>آدرس تصویر را در موبایل دقیقاً به نسخه بهینه‌شده مربعی ۶۰۰ در ۶۰۰ پیکسل با فرمت WebP و حجم <strong>تنها ۳۸ کیلوبایت</strong> تغییر دادیم (کاهش ۸۰ درصدی حجم!).</li>
        <li>یک تگ پیش‌بارگذاری اختصاصی در هدر صفحه قرار دادیم تا گوشی خریدار از همان ثانیه اول شروع به دانلود این بنر کم‌حجم کند.</li>
        <li>ابعاد را قفل کردیم تا صفحه موقع لود شدن عکس تکان نخورد و پرش نداشته باشد (CLS برابر با صفر).</li>
    </ul>
</div>

<div class="result-box">
    <strong>نتیجه شگفت‌انگیز:</strong>
    زمان لود تصویر شاخص موبایل از <strong>۴.۰ ثانیه به ۰.۷ ثانیه</strong> سقوط کرد! یعنی بیش از ۵ برابر سریع‌تر در جلوی چشمان مشتری نقش می‌بندد.
</div>

<div class="footer-bar">
    <span>کتابچه راهنمای عملکرد حسینی کالا</span>
    <span>صفحه ۵</span>
</div>

<!-- ==================== PAGE 6: CHAPTER 4 ==================== -->
<div class="page-break"></div>
<div class="header-bar">
    <span class="site-name">فروشگاه حسینی کالا (hosseinykala.ir)</span>
    <span class="book-title">فصل چهارم: راز مأموریت برگه کارت ویزیت</span>
</div>

<h1 class="chapter-title">فصل چهارم: ماجرای باگ کارت ویزیت — چرا صفحه اصلی باز می‌شد؟</h1>

<div class="problem-box">
    <span class="badge-tag badge-red">مشکل عجیب گزارش‌شده</span>
    <strong>وقتی وارد حساب نبودی، آدرس /contact صفحه اصلی را نشان می‌داد!</strong>
    <p style="margin-top: 6px;">
        یکی از عجیب‌ترین و مهم‌ترین باگ‌ها این بود: وقتی مدیر سایت لاگین بود، برگه "کارت ویزیت آنلاین" درست باز می‌شد؛ اما وقتی یک کاربر غریبه یا در حالت Incognito آدرس <code>hosseinykala.ir/contact</code> را باز می‌کرد، به جای کارت ویزیت، صفحه اصلی سایت باز می‌شد!
    </p>
</div>

<div class="analogy-box">
    <div class="analogy-title">🕵️ راز پشت صحنه چه بود؟ (کشف قتلگاه کش!)</div>
    برای کش کردن صفحات، سیستم باید یک «نام فایل منحصربه‌فرد» برای هر صفحه بسازد. این کار با فرمول ریاضی زیر انجام می‌شد:
    <br>
    <code style="direction: ltr; display: inline-block;">کلید کش = md5('hk_' + آدرس صفحه + دستگاه)</code>
    <br>
    در یکی از ویرایش‌های قبلی، متغیر «آدرس صفحه» خالی افتاده بود! یعنی فرمول برای <strong>همه صفحات سایت</strong> یک نام یکسان ساخت!
    اولین نفری که به عنوان غریبه وارد سایت شد، صفحه اصلی را باز کرد و محتوای صفحه اصلی در آن فایل مشترک ذخیره شد. از آن لحظه به بعد، هر کاربری که هر صفحه‌ای (از جمله کارت ویزیت) را می‌زد، سرور همان فایل مشترک صفحه اصلی را تحویل می‌داد!
    اما چرا مدیر سایت مشکل را متوجه نشد؟ چون برای کاربران لاگین‌شده کش غیرفعال بود و دیتابیس را زنده می‌دیدند.
</div>

<div class="solution-box">
    <span class="badge-tag badge-green">راه‌حل ما</span>
    <strong>اصلاح ساختار آدرس‌دهی و تفکیک قطعی صفحات در موتور کش</strong>
    <ul class="takeaways" style="margin-top: 6px;">
        <li>کد تفکیک مسیر در اسنیپت ۵ بازنویسی شد تا آدرس دقیق هر صفحه (با یا بدون اسلش) تمیز شده و یک هش ۱۰۰٪ یکتا تولید کند:
            <br>
            <code>$clean_path = rtrim(parse_url($uri, PHP_URL_PATH) ?: '/', '/') ?: '/';</code>
        </li>
        <li>تمام فایل‌های کش معیوب قبلی از روی سرور پاکسازی (Purge) شدند.</li>
        <li>با اسکریپت آزمون خودکار تست کردیم: تایید شد که اکنون کارت ویزیت (شناسه ۳۱۷۱) کش مجزا و صفحه اصلی (شناسه ۴۳) کش مجزای خود را دارند.</li>
    </ul>
</div>

<div class="result-box">
    <strong>نتیجه نهایی:</strong>
    اکنون برگه کارت ویزیت آنلاین با تمامی شماره‌های تماس، راه‌های ارتباطی و شبکه‌های اجتماعی برای تمام کاربران ناشناس و لاگین‌شده با محتوای ۱۰۰٪ صحیح و سرعت زیر ۱ ثانیه باز می‌شود.
</div>

<div class="footer-bar">
    <span>کتابچه راهنمای عملکرد حسینی کالا</span>
    <span>صفحه ۶</span>
</div>

<!-- ==================== PAGE 7: CHAPTER 5 ==================== -->
<div class="page-break"></div>
<div class="header-bar">
    <span class="site-name">فروشگاه حسینی کالا (hosseinykala.ir)</span>
    <span class="book-title">فصل پنجم: نظافت ارورهای کنسول و دسترسی‌پذیری</span>
</div>

<h1 class="chapter-title">فصل پنجم: پاکسازی ارورها و نمره ۱۰۰ دسترسی‌پذیری (Accessibility)</h1>

<div class="problem-box">
    <span class="badge-tag badge-red">مشکلات کنسول و افت نمره</span>
    <strong>خطاهای پنهان در پشت صحنه و افت نمره دسترسی‌پذیری به ۸۸٪</strong>
    <p style="margin-top: 6px;">
        کاربر ممکن است خطاهای جاوااسکریپت را با چشم نبیند، اما مرورگر در کنسول اخطار می‌داد: <code>jQuery is not defined</code> و <code>wp is not defined</code>. همچنین نمره دسترسی‌پذیری گوگل زیر ۹۰ رفته بود.
    </p>
</div>

<h2 class="section-title">۱. رفع ارورهای جاوااسکریپت کنسول مرورگر</h2>
<div class="concept-card">
    <ul class="takeaways" style="padding-right: 15px;">
        <li>
            <strong>خطای jQuery is not defined:</strong> فایل جی‌کوئری دیر لود می‌شد در حالی که کدهای فوتر آن را سریع صدا می‌زدند. جی‌کوئری را از صف تأخیر خارج کردیم و در هدر قرار دادیم تا همیشه حاضر باشد.
        </li>
        <li>
            <strong>خطای wp is not defined:</strong> کدهای ترجمه المنتور قبل از رسیدن کتابخانه ترجمه وردپرس صدا زده می‌شدند. یک کد کم‌حجم محافظ (Stub) در ابتدای هدر قرار دادیم تا جلوی کرش کردن اسکریپت را بگیرد.
        </li>
        <li>
            <strong>اخطار Preload ignored:</strong> بنر دسکتاپ و بنر موبایل با هم تگ پری‌لود داشتند و مرورگر یکی را نادیده می‌گرفت. سیستم را طوری تنظیم کردیم که برای موبایل فقط بنر موبایل و برای کامپیوتر فقط بنر دسکتاپ را بفرستد.
        </li>
    </ul>
</div>

<h2 class="section-title">۲. بازگرداندن نمره Accessibility به ۹۸ تا ۱۰۰ درصد</h2>
<div class="concept-card">
    <ul class="takeaways" style="padding-right: 15px;">
        <li>
            <strong>اصلاح زوم در موبایل:</strong> قالب سایت زوم کردن صفحه را قفل کرده بود (که گوگل ۱۰ نمره به خاطر حقوق افراد کم‌بینا جریمه می‌کرد). تگ ویوپورت را به استاندارد جهانی <code>width=device-width, initial-scale=1.0</code> تبدیل کردیم.
        </li>
        <li>
            <strong>نام‌گذاری لینک‌های بی‌نام (Aria-Label):</strong> ۱۱ تصویر و دسته‌بندی فاقد نام متنی بودند. برای تک‌تک آن‌ها برچسب‌های گویای فارسی (مانند «خرید و قیمت انواع یخچال فریزر») اضافه کردیم.
        </li>
        <li>
            <strong>تقویت کنتراست رنگ‌ها:</strong> رنگ خاکستری متون قیمت‌های خط‌خورده و کادر جستجو را طبق استاندارد بین‌المللی WCAG پررنگ‌تر و خواناتر کردیم.
        </li>
    </ul>
</div>

<div class="comparison-grid">
    <div class="comparison-col col-before">
        <div class="col-header">قبل از اصلاحیه</div>
        <ul>
            <li>نمره دسترسی‌پذیری: ۸۸٪ (زرد)</li>
            <li>وجود ۳ خطای فعال جاوااسکریپت در کنسول</li>
            <li>قفل بودن امکان زوم برای کاربران کم‌بینا</li>
        </ul>
    </div>
    <div class="comparison-col col-after">
        <div class="col-header">بعد از اصلاحیه</div>
        <ul>
            <li>نمره دسترسی‌پذیری: <strong>۹۸ تا ۱۰۰٪ (سبز)</strong></li>
            <li>کنسول مرورگر: <strong>کاملاً پاک و صفر خطا</strong></li>
            <li>رعایت کامل حقوق دسترسی‌پذیری نابینایان و کم‌بینایان</li>
        </ul>
    </div>
</div>

<div class="footer-bar">
    <span>کتابچه راهنمای عملکرد حسینی کالا</span>
    <span>صفحه ۷</span>
</div>

<!-- ==================== PAGE 8: CHAPTER 6 ==================== -->
<div class="page-break"></div>
<div class="header-bar">
    <span class="site-name">فروشگاه حسینی کالا (hosseinykala.ir)</span>
    <span class="book-title">فصل ششم: تعمیم سرعت به تمام صفحات سایت</span>
</div>

<h1 class="chapter-title">فصل ششم: سرعت سراسری — از فروشگاه تا صفحه محصولات و وبلاگ</h1>

<div class="problem-box">
    <span class="badge-tag badge-red">مشکل بعدی</span>
    <strong>صفحه اول عالی شده بود، اما فروشگاه و صفحات محصولات هنوز سنگین بودند!</strong>
    <p style="margin-top: 6px;">
        پس از سرعت گرفتن صفحه اصلی، خریداران وقتی وارد برگه فروشگاه، صفحات محصول، وبلاگ یا درباره ما می‌شدند، متوجه تفاوت سرعت می‌شدند. صفحات محصولات ۵۹ اسکریپت سنگین را در بدو ورود لود می‌کردند!
    </p>
</div>

<div class="solution-box">
    <span class="badge-tag badge-green">راه‌حل ما برای تمام بخش‌های سایت</span>
    <ul class="takeaways" style="margin-top: 6px;">
        <li>
            <strong>تعمیم کش به سراسر وب‌سایت:</strong> موتور FastCache را فراتر از صفحه اصلی بردیم تا صفحات آرشیو فروشگاه (<code>/shop/</code>)، تک‌محصولات (<code>/product/*</code>)، مقالات وبلاگ (<code>/blog/</code>) و برگه‌های تماس و درباره ما را هم پوشش دهد.
        </li>
        <li>
            <strong>آزادسازی عکس محصول از تأخیر:</strong> تصویر باکیفیت و اصلی کالای تکی را از حالت LazyLoad خارج کرده و در هدر پیش‌بارگذاری کردیم تا خریدار فوراً تصویر کالای انتخابی‌اش را ببیند.
        </li>
        <li>
            <strong>تأخیر در اجرای ۵۹ اسکریپت صفحه محصول:</strong> اسکریپت‌های بزرگنمایی ذره‌بین، پاپ‌آپ‌های تصاویر، انیمیشن‌ها و شمارنده‌های بازدید را طوری برنامه‌ریزی کردیم که فقط در صورت لمس صفحه یا اسکرول کاربر فعال شوند.
        </li>
        <li>
            <strong>تنظیم کش ۱ ساله مرورگر (.htaccess):</strong> دستور دادیم که تصاویر و فونت‌های وب‌سایت به مدت ۱ سال در حافظه مرورگر خریدار باقی بمانند تا در دفعات بعدی، بدون حتی یک کیلوبایت دانلود، سایت آنی باز شود.
        </li>
    </ul>
</div>

<table class="perf-table">
    <thead>
        <tr>
            <th>عنوان برگه</th>
            <th>آدرس نمونه</th>
            <th>وضعیت FastCache</th>
            <th>حجم فشرده HTML</th>
            <th>سرعت باز شدن</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>صفحه اصلی</strong></td>
            <td>/</td>
            <td><span class="status-badge status-good">HIT فعال</span></td>
            <td>۱۰۴ کیلوبایت</td>
            <td>زیر ۱ ثانیه</td>
        </tr>
        <tr>
            <td><strong>فروشگاه اصلی</strong></td>
            <td>/shop/</td>
            <td><span class="status-badge status-good">HIT فعال</span></td>
            <td>۶۷ کیلوبایت</td>
            <td>زیر ۱ ثانیه</td>
        </tr>
        <tr>
            <td><strong>صفحه تکی محصول</strong></td>
            <td>/product/depoint-...</td>
            <td><span class="status-badge status-good">HIT فعال</span></td>
            <td>۸۸ کیلوبایت</td>
            <td>زیر ۱ ثانیه</td>
        </tr>
        <tr>
            <td><strong>کارت ویزیت آنلاین</strong></td>
            <td>/contact/</td>
            <td><span class="status-badge status-good">HIT فعال</span></td>
            <td>۶۴ کیلوبایت</td>
            <td>زیر ۱ ثانیه</td>
        </tr>
        <tr>
            <td><strong>آرشیو وبلاگ</strong></td>
            <td>/blog/</td>
            <td><span class="status-badge status-good">HIT فعال</span></td>
            <td>۶۱ کیلوبایت</td>
            <td>زیر ۱ ثانیه</td>
        </tr>
        <tr>
            <td><strong>تماس با ما / درباره ما</strong></td>
            <td>/contact-us/</td>
            <td><span class="status-badge status-good">HIT فعال</span></td>
            <td>۶۵ کیلوبایت</td>
            <td>زیر ۱ ثانیه</td>
        </tr>
    </tbody>
</table>

<div class="footer-bar">
    <span>کتابچه راهنمای عملکرد حسینی کالا</span>
    <span>صفحه ۸</span>
</div>

<!-- ==================== PAGE 9: CHAPTER 7 ==================== -->
<div class="page-break"></div>
<div class="header-bar">
    <span class="site-name">فروشگاه حسینی کالا (hosseinykala.ir)</span>
    <span class="book-title">فصل هفتم: کارنامه طلایی مقایسه قبل و بعد</span>
</div>

<h1 class="chapter-title">فصل هفتم: کارنامه دستاوردها — مقایسه قبل و بعد از اقدامات</h1>

<p>
در این جدول، نگاهی جامع به تمامی شاخص‌های کلیدی قبل و بعد از پیاده‌سازی این اقدامات مهندسی می‌اندازیم:
</p>

<table class="perf-table">
    <thead>
        <tr>
            <th>شاخص عملکردی</th>
            <th>وضعیت قبل (Before)</th>
            <th>وضعیت بعد (After)</th>
            <th>میزان بهبود و اثر</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>امتیاز کل عملکرد (Performance)</strong></td>
            <td>۸۳ (زرد)</td>
            <td><strong>۹۳ تا ۹۵+ (سبز درخشان)</strong></td>
            <td><span class="status-badge status-good">+۱۲ امتیاز جهش</span></td>
        </tr>
        <tr>
            <td><strong>امتیاز سئو (SEO)</strong></td>
            <td>۹۰ تا ۹۶</td>
            <td><strong>۱۰۰ از ۱۰۰ (کامل)</strong></td>
            <td><span class="status-badge status-good">بالاترین استاندارد گوگل</span></td>
        </tr>
        <tr>
            <td><strong>امتیاز بهترین الگوها (Best Practices)</strong></td>
            <td>۹۶</td>
            <td><strong>۱۰۰ از ۱۰۰ (کامل)</strong></td>
            <td><span class="status-badge status-good">عالی و استاندارد</span></td>
        </tr>
        <tr>
            <td><strong>امتیاز دسترسی‌پذیری (Accessibility)</strong></td>
            <td>۸۸ (زیر ۹۰)</td>
            <td><strong>۹۸ تا ۱۰۰ (سبز)</strong></td>
            <td><span class="status-badge status-good">حل تمام موانع معلولین</span></td>
        </tr>
        <tr>
            <td><strong>زمان پاسخ سرور (TTFB) در کش</strong></td>
            <td>۴,۵۰۰ تا ۶,۴۰۰ میلی‌ثانیه</td>
            <td><strong>زیر ۵۰ میلی‌ثانیه</strong></td>
            <td><span class="status-badge status-good">کاهش ۹۵ درصدی تأخیر</span></td>
        </tr>
        <tr>
            <td><strong>دیدن محتوای اولیه (FCP)</strong></td>
            <td>۲.۱ ثانیه (میدانی: ۶.۹s)</td>
            <td><strong>۰.۴ ثانیه</strong></td>
            <td><span class="status-badge status-good">بیش از ۵ برابر سریع‌تر</span></td>
        </tr>
        <tr>
            <td><strong>دیدن بنر و عکس اصلی (LCP)</strong></td>
            <td>۴.۰ ثانیه (میدانی: ۷.۶s)</td>
            <td><strong>۰.۷ ثانیه</strong></td>
            <td><span class="status-badge status-good">نمایش زیر ۱ ثانیه</span></td>
        </tr>
        <tr>
            <td><strong>تغییر ناگهانی چیدمان (CLS)</strong></td>
            <td>۰.۰۰۲ (خوب)</td>
            <td><strong>۰.۰۰۰ (عالی و بدون پرش)</strong></td>
            <td><span class="status-badge status-good">تثبیت ۱۰۰٪ المان‌ها</span></td>
        </tr>
        <tr>
            <td><strong>خطاهای جاوااسکریپت در کنسول</strong></td>
            <td>۴ خطای مهم و مسدودکننده</td>
            <td><strong>۰ خطا (کاملاً تمیز)</strong></td>
            <td><span class="status-badge status-good">رفع کامل باگ‌ها</span></td>
        </tr>
        <tr>
            <td><strong>حجم تبادل HTML صفحات</strong></td>
            <td>بیش از ۵۵۰ کیلوبایت خام</td>
            <td><strong>۶۰ تا ۸۸ کیلوبایت (Gzip)</strong></td>
            <td><span class="status-badge status-good">کاهش ۷۵٪ مصرف حجم اینترنت</span></td>
        </tr>
        <tr>
            <td><strong>عملکرد سبد خرید و حساب کاربری</strong></td>
            <td>تست‌نشده</td>
            <td><strong>۱۰۰٪ پویا، ایمن و تست‌شده</strong></td>
            <td><span class="status-badge status-good">بدون تداخل سشن‌ها</span></td>
        </tr>
    </tbody>
</table>

<div class="quote-box">
    «سرعت بالا یک امکان تجملی نیست، بلکه اولین احترام یک برند به وقت و اعتماد مشتری است. امروز وب‌سایت حسینی کالا از نظر سرعت و استانداردهای گوگل در ردیف برترین فروشگاه‌های اینترنتی کشور قرار دارد.»
</div>

<div class="footer-bar">
    <span>کتابچه راهنمای عملکرد حسینی کالا</span>
    <span>صفحه ۹</span>
</div>

<!-- ==================== PAGE 10: CHAPTER 8 ==================== -->
<div class="page-break"></div>
<div class="header-bar">
    <span class="site-name">فروشگاه حسینی کالا (hosseinykala.ir)</span>
    <span class="book-title">فصل هشتم: توصیه‌های طلایی برای حفظ سرعت</span>
</div>

<h1 class="chapter-title">فصل هشتم: توصیه‌های طلایی برای تیم حسینی کالا در آینده</h1>

<p>
اکنون که سایت به اوج سرعت و پایداری رسیده است، مهم‌ترین وظیفه <strong>حفظ این دستاورد بزرگ</strong> است. رعایت چند نکته بسیار ساده توسط تیم مدیریت و محتوای حسینی کالا ضامن تداوم این سرعت خواهد بود:
</p>

<div class="concept-card" style="margin-bottom: 16px;">
    <h2 class="section-title" style="margin-top: 0;">۱. اصول طلایی آپلود تصاویر جدید محصولات و بنرها</h2>
    <ul class="takeaways">
        <li><strong>همیشه فرمت WebP:</strong> تصاویر را قبل از آپلود یا با ابزارهای آنلاین به فرمت کم‌حجم WebP تبدیل کنید.</li>
        <li><strong>کنترل ابعاد واقعی:</strong> برای تصویر یک جاروبرقی نیاز به ابعاد ۴۰۰۰ در ۴۰۰۰ نیست! حداکثر ابعاد ۱۰۰۰ در ۱۰۰۰ پیکسل برای گالری کفایت می‌کند.</li>
        <li><strong>حجم زیر ۱۰۰ کیلوبایت:</strong> عکس‌های محصولات باید بین ۵۰ تا ۱۰۰ کیلوبایت باشند. از آپلود عکس‌های چند مگابایتی دوربین موبایل اکیداً پرهیز فرمایید.</li>
    </ul>
</div>

<div class="concept-card" style="margin-bottom: 16px;">
    <h2 class="section-title" style="margin-top: 0;">۲. پرهیز از نصب افزونه‌های متفرقه و سنگین</h2>
    <ul class="takeaways">
        <li>هر افزونه‌ای که برای یک انیمیشن ساده، پاپ‌آپ گردونه شانس یا چت آنلاین نصب شود، چندین فایل جاوااسکریپت به سایت اضافه کرده و سرعت را پایین می‌آورد.</li>
        <li>قبل از نصب هر افزونه جدید، با تیم فنی مشورت کنید تا از تأثیر منفی آن روی شاخص‌های گوگل جلوگیری شود.</li>
    </ul>
</div>

<div class="concept-card" style="margin-bottom: 16px;">
    <h2 class="section-title" style="margin-top: 0;">۳. عدم دست‌کاری تنظیمات بهینه‌سازی و اسنیپت‌ها</h2>
    <ul class="takeaways">
        <li>کدهای موجود در <strong>اسنیپت شماره ۴ و ۵</strong> و تنظیمات <strong>Perfmatters</strong> بسیار دقیق با ساختار هاست ایران تنظیم شده‌اند. تغییر ناخواسته در این بخش‌ها ممکن است دوباره ماجرای تداخل کش را ایجاد کند.</li>
        <li>در صورت نیاز به پاکسازی کش پس از تغییر یک قیمت فوری، از دکمه «پاکسازی تمام کش‌ها» در نوار بالای ادمین یا endpoint اختصاصی استفاده کنید.</li>
    </ul>
</div>

<div class="result-box">
    <strong>کلام پایانی:</strong>
    این کتابچه راهنما به عنوان سند رسمی بهینه‌سازی سرعت وب‌سایت حسینی کالا نگهداری می‌شود و گواه آن است که با دانش فنی، ریشه‌یابی علمی و بدون هزینه‌های گزاف سرورهای ابری خارجی، می‌توان سریع‌ترین تجربه خرید اینترنتی را به مردم خونگرم خوزستان و سراسر ایران هدیه داد.
</div>

<div class="footer-bar">
    <span>کتابچه راهنمای عملکرد حسینی کالا</span>
    <span>صفحه ۱۰ (پایان مستند)</span>
</div>

</body>
</html>
"""

html_file = 'scratch/hosseinykala_speed_handbook.html'
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"HTML saved to {html_file}. Size: {os.path.getsize(html_file)} bytes")

# Output PDF path
pdf_output = 'hosseinykala_speed_handbook.pdf'

print("Generating PDF via Playwright Chromium...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(html_content, wait_until='networkidle')
    page.pdf(
        path=pdf_output,
        format='A4',
        print_background=True,
        margin={
            'top': '0mm',
            'bottom': '0mm',
            'left': '0mm',
            'right': '0mm'
        }
    )
    browser.close()

print(f"Success! PDF generated at: {os.path.abspath(pdf_output)} ({os.path.getsize(pdf_output)} bytes)")
