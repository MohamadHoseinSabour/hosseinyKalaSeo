import os
import sys
import json
import time
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

TAG_MAP = {}

def load_all_tags():
    print("Loading all tags from WordPress...", flush=True)
    page = 1
    while page <= 2:
        url = f"https://hosseinykala.ir/wp-json/wp/v2/tags?per_page=100&page={page}"
        try:
            r = requests.get(url, headers=HEADERS, auth=AUTH, timeout=20)
            if r.status_code == 200:
                tags = r.json()
                for t in tags:
                    TAG_MAP[t['name'].strip()] = t['id']
                if len(tags) < 100:
                    break
                page += 1
            else:
                break
        except Exception as e:
            print(f"Error fetching tags page {page}: {e}", flush=True)
            break
    print(f"Loaded {len(TAG_MAP)} existing tags.", flush=True)

def get_or_create_tag(name):
    clean = name.strip()
    if clean in TAG_MAP:
        return TAG_MAP[clean]
    
    print(f"Creating new tag: {clean}", flush=True)
    try:
        r = requests.post(
            "https://hosseinykala.ir/wp-json/wp/v2/tags",
            headers=HEADERS,
            auth=AUTH,
            json={'name': clean},
            timeout=20
        )
        if r.status_code in [200, 201]:
            tid = r.json()['id']
            TAG_MAP[clean] = tid
            return tid
        else:
            print(f"Failed to create tag {clean}: {r.status_code}", flush=True)
    except Exception as e:
        print(f"Exception creating tag {clean}: {e}", flush=True)
    return None

SVG_INFOGRAPHIC = """
<div style="margin: 30px 0; text-align: center; direction: rtl; overflow-x: auto;">
<svg viewBox="0 0 960 480" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-radius: 16px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3); font-family: Tahoma, Vazirmatn, sans-serif;">
  <defs>
    <linearGradient id="cardGrad1" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#0284c7" stop-opacity="0.2"/><stop offset="100%" stop-color="#0284c7" stop-opacity="0.05"/></linearGradient>
    <linearGradient id="cardGrad2" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#4f46e5" stop-opacity="0.2"/><stop offset="100%" stop-color="#4f46e5" stop-opacity="0.05"/></linearGradient>
    <linearGradient id="cardGrad3" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#e11d48" stop-opacity="0.2"/><stop offset="100%" stop-color="#e11d48" stop-opacity="0.05"/></linearGradient>
    <linearGradient id="cardGrad4" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#059669" stop-opacity="0.25"/><stop offset="100%" stop-color="#059669" stop-opacity="0.08"/></linearGradient>
    <linearGradient id="cardGrad5" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#d97706" stop-opacity="0.2"/><stop offset="100%" stop-color="#d97706" stop-opacity="0.05"/></linearGradient>
  </defs>

  <!-- Title & Subtitle -->
  <text x="480" y="42" fill="#38bdf8" font-size="20" font-weight="bold" text-anchor="middle">نقشه جامع روش‌های خرید اقساطی لوازم خانگی | حسینی کالا</text>
  <text x="480" y="68" fill="#94a3b8" font-size="13" text-anchor="middle">مقایسه سقف تسهیلات، دوره بازپرداخت، نرخ کارمزد و شرایط ضمانت</text>

  <!-- Card 1: Refah Beta -->
  <g transform="translate(775, 95)">
    <rect x="0" y="0" width="165" height="345" rx="12" fill="url(#cardGrad1)" stroke="#0284c7" stroke-width="1.5"/>
    <rect x="0" y="0" width="165" height="42" rx="12" fill="#0284c7"/>
    <text x="82" y="26" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">طرح بتا بانک رفاه</text>
    <text x="82" y="68" fill="#38bdf8" font-size="11" text-anchor="middle">مخصوص بازنشستگان</text>
    <text x="82" y="92" fill="#f8fafc" font-size="15" font-weight="bold" text-anchor="middle">بر اساس حقوق</text>
    
    <line x1="20" y1="110" x2="145" y2="110" stroke="#334155" stroke-width="1"/>
    
    <text x="145" y="135" fill="#94a3b8" font-size="11" text-anchor="end">دوره بازپرداخت:</text>
    <text x="145" y="155" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="end">تا ۳۶ ماه</text>
    
    <text x="145" y="185" fill="#94a3b8" font-size="11" text-anchor="end">نحوه کسر اقساط:</text>
    <text x="145" y="205" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="end">خودکار از حقوق</text>
    
    <text x="145" y="235" fill="#94a3b8" font-size="11" text-anchor="end">ضامن و چک:</text>
    <text x="145" y="255" fill="#22c55e" font-size="12" font-weight="bold" text-anchor="end">بدون چک و ضامن</text>
    
    <text x="145" y="285" fill="#94a3b8" font-size="11" text-anchor="end">پیش‌پرداخت:</text>
    <text x="145" y="305" fill="#f8fafc" font-size="12" text-anchor="end">بدون پیش یا حداقل</text>
    
    <rect x="15" y="318" width="135" height="18" rx="4" fill="#0369a1" fill-opacity="0.4"/>
    <text x="82" y="331" fill="#7dd3fc" font-size="10" text-anchor="middle">سامانه beta.refah-bank.ir</text>
  </g>

  <!-- Card 2: Bajet Tejarat -->
  <g transform="translate(585, 95)">
    <rect x="0" y="0" width="165" height="345" rx="12" fill="url(#cardGrad2)" stroke="#4f46e5" stroke-width="1.5"/>
    <rect x="0" y="0" width="165" height="42" rx="12" fill="#4f46e5"/>
    <text x="82" y="26" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">طرح باجت (کالانو)</text>
    <text x="82" y="68" fill="#818cf8" font-size="11" text-anchor="middle">بانک تجارت / رفاه</text>
    <text x="82" y="92" fill="#f8fafc" font-size="15" font-weight="bold" text-anchor="middle">تا ۳۰۰ میلیون</text>
    
    <line x1="20" y1="110" x2="145" y2="110" stroke="#334155" stroke-width="1"/>
    
    <text x="145" y="135" fill="#94a3b8" font-size="11" text-anchor="end">دوره بازپرداخت:</text>
    <text x="145" y="155" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="end">۱۲ تا ۳۶ ماه</text>
    
    <text x="145" y="185" fill="#94a3b8" font-size="11" text-anchor="end">شیوه اعتبارسنجی:</text>
    <text x="145" y="205" fill="#818cf8" font-size="12" font-weight="bold" text-anchor="end">آنلاین (رتبه A و B)</text>
    
    <text x="145" y="235" fill="#94a3b8" font-size="11" text-anchor="end">ضامن:</text>
    <text x="145" y="255" fill="#22c55e" font-size="12" font-weight="bold" text-anchor="end">بدون ضامن در رتبه A</text>
    
    <text x="145" y="285" fill="#94a3b8" font-size="11" text-anchor="end">شکل تسهیلات:</text>
    <text x="145" y="305" fill="#f8fafc" font-size="12" text-anchor="end">اعتبار خرید دیجیتال</text>
    
    <rect x="15" y="318" width="135" height="18" rx="4" fill="#3730a3" fill-opacity="0.4"/>
    <text x="82" y="331" fill="#c7d2fe" font-size="10" text-anchor="middle">اپلیکیشن باجت تجارت</text>
  </g>

  <!-- Card 3: Mellat Bank -->
  <g transform="translate(395, 95)">
    <rect x="0" y="0" width="165" height="345" rx="12" fill="url(#cardGrad3)" stroke="#e11d48" stroke-width="1.5"/>
    <rect x="0" y="0" width="165" height="42" rx="12" fill="#e11d48"/>
    <text x="82" y="26" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">وام بانک ملت</text>
    <text x="82" y="68" fill="#fb7185" font-size="11" text-anchor="middle">حامی کارت / فرابانک</text>
    <text x="82" y="92" fill="#f8fafc" font-size="15" font-weight="bold" text-anchor="middle">تا ۲۰۰ میلیون</text>
    
    <line x1="20" y1="110" x2="145" y2="110" stroke="#334155" stroke-width="1"/>
    
    <text x="145" y="135" fill="#94a3b8" font-size="11" text-anchor="end">دوره بازپرداخت:</text>
    <text x="145" y="155" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="end">تا ۶۰ ماه (۵ سال)</text>
    
    <text x="145" y="185" fill="#94a3b8" font-size="11" text-anchor="end">نرخ سود سالیانه:</text>
    <text x="145" y="205" fill="#fb7185" font-size="12" font-weight="bold" text-anchor="end">۱۸٪ تا ۲۳٪ مصوب</text>
    
    <text x="145" y="235" fill="#94a3b8" font-size="11" text-anchor="end">نوع ضمانت:</text>
    <text x="145" y="255" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="end">ضامن معتبر / رتبه</text>
    
    <text x="145" y="285" fill="#94a3b8" font-size="11" text-anchor="end">مستندات لازم:</text>
    <text x="145" y="305" fill="#f8fafc" font-size="12" text-anchor="end">پیش‌فاکتور رسمی</text>
    
    <rect x="15" y="318" width="135" height="18" rx="4" fill="#9f1239" fill-opacity="0.4"/>
    <text x="82" y="331" fill="#fecdd3" font-size="10" text-anchor="middle">سامانه فرابانک ملت</text>
  </g>

  <!-- Card 4: Sayadi Cheque (Hosseiny Kala Star) -->
  <g transform="translate(205, 95)">
    <rect x="0" y="0" width="165" height="345" rx="12" fill="url(#cardGrad4)" stroke="#059669" stroke-width="2"/>
    <rect x="0" y="0" width="165" height="42" rx="12" fill="#059669"/>
    <text x="82" y="26" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">چک صیادی (حسینی)</text>
    <text x="82" y="68" fill="#34d399" font-size="11" text-anchor="middle">تحویل فوری در اهواز</text>
    <text x="82" y="92" fill="#f8fafc" font-size="15" font-weight="bold" text-anchor="middle">بدون معطلی بانکی</text>
    
    <line x1="20" y1="110" x2="145" y2="110" stroke="#047857" stroke-width="1"/>
    
    <text x="145" y="135" fill="#94a3b8" font-size="11" text-anchor="end">پیش‌پرداخت نقد:</text>
    <text x="145" y="155" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="end">۵۰٪ کل مبلغ فاکتور</text>
    
    <text x="145" y="185" fill="#94a3b8" font-size="11" text-anchor="end">دوره بازپرداخت:</text>
    <text x="145" y="205" fill="#34d399" font-size="12" font-weight="bold" text-anchor="end">تا ۱۲ ماه اقساط</text>
    
    <text x="145" y="235" fill="#94a3b8" font-size="11" text-anchor="end">کارمزد ماهانه:</text>
    <text x="145" y="255" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="end">۳ درصد ماهیانه</text>
    
    <text x="145" y="285" fill="#94a3b8" font-size="11" text-anchor="end">سرعت تحویل کالا:</text>
    <text x="145" y="305" fill="#34d399" font-size="12" font-weight="bold" text-anchor="end">آنی و همان روز</text>
    
    <rect x="15" y="318" width="135" height="18" rx="4" fill="#065f46" fill-opacity="0.5"/>
    <text x="82" y="331" fill="#a7f3d0" font-size="10" text-anchor="middle">استعلام وضعیت سفید صیاد</text>
  </g>

  <!-- Card 5: Mehr Iran & BNPL -->
  <g transform="translate(15, 95)">
    <rect x="0" y="0" width="165" height="345" rx="12" fill="url(#cardGrad5)" stroke="#d97706" stroke-width="1.5"/>
    <rect x="0" y="0" width="165" height="42" rx="12" fill="#d97706"/>
    <text x="82" y="26" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">کالا کارت مهر ایران</text>
    <text x="82" y="68" fill="#fbbf24" font-size="11" text-anchor="middle">وام قرض‌الحسنه</text>
    <text x="82" y="92" fill="#f8fafc" font-size="15" font-weight="bold" text-anchor="middle">تا ۳۰۰ میلیون</text>
    
    <line x1="20" y1="110" x2="145" y2="110" stroke="#334155" stroke-width="1"/>
    
    <text x="145" y="135" fill="#94a3b8" font-size="11" text-anchor="end">نرخ کارمزد سالیانه:</text>
    <text x="145" y="155" fill="#34d399" font-size="12" font-weight="bold" text-anchor="end">۴ درصد قرض‌الحسنه</text>
    
    <text x="145" y="185" fill="#94a3b8" font-size="11" text-anchor="end">دوره بازپرداخت:</text>
    <text x="145" y="205" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="end">۶ تا ۲۴ ماه</text>
    
    <text x="145" y="235" fill="#94a3b8" font-size="11" text-anchor="end">ضامن:</text>
    <text x="145" y="255" fill="#fbbf24" font-size="12" font-weight="bold" text-anchor="end">ضامن معتبر رسمی</text>
    
    <text x="145" y="285" fill="#94a3b8" font-size="11" text-anchor="end">مسدودی سپرده:</text>
    <text x="145" y="305" fill="#22c55e" font-size="12" font-weight="bold" text-anchor="end">بدون مسدودی حساب</text>
    
    <rect x="15" y="318" width="135" height="18" rx="4" fill="#78350f" fill-opacity="0.4"/>
    <text x="82" y="331" fill="#fde68a" font-size="10" text-anchor="middle">سامانه آنلاین مهریران</text>
  </g>
</svg>
</div>
"""

MEGA_ARTICLE_HTML = f"""
<p>نوسانات قیمتی و شتاب تورم در سال‌های اخیر، نوسازی وسایل خانه یا تهیه جهیزیه عروس را به یکی از جدی‌ترین چالش‌های خانواده‌های ایرانی تبدیل کرده است. در این شرایط، ماه‌ها پس‌انداز کردن برای خرید نقدی یک کالا معمولاً نتیجه‌ای جز عقب ماندن از افزایش قیمت‌ها ندارد. خرید اقساطی لوازم خانگی راهکاری منطقی و حساب‌شده است که امکان دسترسی بی‌درنگ به تجهیزات اساسی و باکیفیت را با هزینه‌ای شناور فراهم می‌کند. در این راهنمای مرجع از <a href="https://hosseinykala.ir/" target="_blank" rel="noopener"><strong>فروشگاه لوازم خانگی حسینی</strong></a>، تمام روش‌های عملی، فعال و قانونی خرید اقساطی شامل <strong>طرح بتای بانک رفاه</strong>، <strong>طرح باجت</strong>، <strong>تسهیلات ۲۰۰ میلیونی بانک ملت</strong>، <strong>خرید اقساطی با چک صیادی</strong> و طرح‌های قرض‌الحسنه را از نگاه یک خریدار با جزئیات کامل و شفاف بررسی می‌کنیم.</p>

{SVG_INFOGRAPHIC}

<h2>چرا خرید اقساطی در اقتصاد امروز تصمیمی کاملاً اقتصادی است؟</h2>
<p>برخی خریداران همچنان تردید دارند که آیا پرداخت کارمزد اقساطی کار درستی است یا خیر. پاسخ این پرسش در مقایسه نرخ کارمزد با تورم سالیانه لوازم خانگی نهفته است. وقتی تورم عمومی بازار لوازم برقی به مراتب بالاتر از نرخ سود تسهیلات بانکی یا کارمزدهای متعارف است، شما کالا را با ارزش جاری ریال تحویل گرفته و در ماه‌های آینده با ریال کم‌ارزش‌تر اقساط آن را می‌پردازید.</p>
<p>مزیت دیگر خرید قسطی، توانایی انتخاب دستگاه‌های بادوام و مجهز به موتورهای اینورتر است. برای نمونه، به جای اجبار در انتخاب یک یخچال کوچک، می‌توانید با مدیریت اقساط سراغ یک <a href="https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/" target="_blank" rel="noopener"><strong>یخچال فریزر دوقلو</strong></a> مدرن بروید که تا ۱۰ سال آینده هزینه‌های تعمیراتی را روی دست شما نگذارد.</p>

<h2>۱. طرح بتای بانک رفاه کارگران؛ ویژه بازنشستگان و مستمری‌بگیران تأمین اجتماعی</h2>
<p><strong>سامانه بتا (Beta)</strong> بانک رفاه کارگران یکی از امن‌ترین و راحت‌ترین بسترهای اعتباری برای جامعه محترم بازنشستگان و مستمری‌بگیران سازمان تأمین اجتماعی است. در این سازوکار، نیازی به ارائه چک، سفته، ضامن کارمند یا مراجعه فرساینده به شعب بانک وجود ندارد.</p>

<div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-right: 5px solid #16a34a; border-radius: 10px; padding: 18px 20px; margin: 25px 0; direction: rtl;">
  <h4 style="color: #166534; margin-top: 0; font-size: 16px;">ویژگی‌های برجسته طرح بتا در یک نگاه:</h4>
  <ul style="margin-bottom: 0; color: #14532d; line-height: 1.9;">
    <li><strong>کسر خودکار اقساط:</strong> مبلغ هر قسط مستقیماً در روز واریز حقوق از حساب بازنشسته کسر می‌گردد.</li>
    <li><strong>بازپرداخت منعطف:</strong> اقساط متناسب با انتخاب مشتری بین ۶ تا ۳۶ ماه تقسیم‌بندی می‌شود.</li>
    <li><strong>بدون پیش‌پرداخت (یا حداقل پیش‌پرداخت):</strong> بسته به سقف اعتبار و توان مالی حقوق‌بگیر، خرید کالا بدون پرداخت نقد اولیه امکان‌پذیر است.</li>
    <li><strong>محاسبه سقف اعتبار بر اساس حقوق:</strong> تا سقف ۶۰ درصد از مانده حقوق آزاد بازنشسته می‌تواند به عنوان تعهد قسط ماهانه در نظر گرفته شود.</li>
  </ul>
</div>

<h3>مراحل گام‌به‌گام خرید کالا از طریق سامانه بتا:</h3>
<ol>
  <li>مراجعه به وبگاه رسمی سامانه به نشانی <code>beta.refah-bank.ir</code>.</li>
  <li>ورود با کد ملی و شماره تلفن همراه معتبری که دقیقاً به نام شخص بازنشسته ثبت شده باشد.</li>
  <li>تأیید اطلاعات هویتی و اعتبارسنجی آنلاین از طریق اطلاعات کارت حقوقی و رمز پویا.</li>
  <li>مشاهده سقف مجاز قسط ماهانه و انتخاب فروشگاه‌های طرف قرارداد.</li>
  <li>صدور مجوز کسر از حقوق در سامانه و نهایی کردن فاکتور خرید لوازم خانگی.</li>
</ol>

<h2>۲. طرح باجت (کالانو بانک تجارت) و کارت رفاهی تا سقف ۳۰۰ میلیون تومان</h2>
<p>اگر بازنشسته تأمین اجتماعی نیستید و به دنبال اعتباری با مبالغ درشت برای خرید جهیزیه یا تجهیز صفر تا صد آشپزخانه می‌گردید، <strong>طرح باجت</strong> و کارت‌های اعتباری رفاهی دو گزینه ایده‌آل پیش روی شما هستند.</p>

<h3>طرح کالانو در اپلیکیشن باجت بانک تجارت:</h3>
<p>اپلیکیشن «باجت» سامانه دیجیتال خدمات خرد بانک تجارت است. در قالب طرح <strong>کالانو</strong>، مشتریان می‌توانند تا سقف <strong>۳۰۰ میلیون تومان</strong> اعتبار خرید لوازم خانگی دریافت کنند. شاخص‌ترین مزیت باجت، امکان پیشبرد تمام مراحل بدون نیاز به کاغذبازی است. متقاضیانی که رتبه اعتباری نظام بانکی آن‌ها A یا B باشد، حتی بدون ضامن حضوری می‌توانند اعتبار خود را به صورت بن خرید لوازم خانگی دریافت کرده و اقساط آن را در بازه ۱۲ تا ۳۶ ماه بپردازند.</p>

<h3>تسهیلات کارت رفاهی و کارگشا بانک رفاه:</h3>
<p>علاوه بر بتا، بانک رفاه تسهیلات کارت رفاهی تا سقف ۳۰۰ میلیون تومان را برای حمایت از خرید کالاهای بادوام تولید ایران در اختیار متقاضیان قرار می‌دهد. این طرح دارای نرخ‌های کارمزد مصوب رقابتی بوده و بازپرداخت آن متناسب با توان درآمدی بین ۲۴ تا ۳۶ ماه تنظیم می‌شود.</p>

<h2>۳. تسهیلات ۲۰۰ میلیونی خرید کالا بانک ملت؛ حامی کارت و فرابانک</h2>
<p>بانک ملت از طریق سامانه‌های نوین خود به‌ویژه <strong>فرابانک</strong> و طرح شناخته‌شده <strong>حامی کارت ملت</strong>، مسیر مشخصی برای اعطای وام خرید کالای بادوام داخلی طراحی کرده است.</p>
<ul>
  <li><strong>سقف تسهیلات:</strong> تا سقف ۲۰۰ میلیون تومان بر اساس رتبه اعتبارسنجی و پیش‌فاکتور رسمی.</li>
  <li><strong>مدت زمان بازپرداخت:</strong> حداکثر تا ۶۰ ماه (۵ سال)، که امکان شکستن اقساط به مبالغ ماهانه سبک را فراهم می‌سازد.</li>
  <li><strong>روش اقدام:</strong> بارگذاری مدارک شغلی، احراز هویت در اپلیکیشن یا وب‌سایت فرابانک ملت و در صورت نیاز ارائه معرفی‌نامه ضامن رسمی معتبر.</li>
  <li><strong>ارائه پیش‌فاکتور معتبر:</strong> دریافت فاکتور رسمی مشخصات کالا از فروشگاه‌های معتبر لوازم خانگی.</li>
</ul>

<h2>۴. خرید اقساطی با چک صیادی در فروشگاه لوازم خانگی حسینی</h2>
<p>بسیاری از مشتریان به دلیل زمان‌گیر بودن روندهای اداری بانک‌ها، نداشتن ضامن کارمند یا ضرورت تحویل فوری کالا، تمایلی به انتظار در نوبت وام‌های بانکی ندارند. ما در <a href="https://hosseinykala.ir/" target="_blank" rel="noopener"><strong>فروشگاه لوازم خانگی حسینی</strong></a> با استقرار شعب حضوری در شهر <strong>اهواز</strong>، امکان خرید اقساطی را با شفاف‌ترین سازوکار ممکن بر پایه چک‌های بنفش صیادی فراهم ساخته‌ایم.</p>

<div style="background: #eff6ff; border: 1px solid #bfdbfe; border-right: 5px solid #2563eb; border-radius: 10px; padding: 20px; margin: 25px 0; direction: rtl;">
  <h3 style="color: #1e40af; margin-top: 0;">شرایط رسمی خرید با چک صیادی در حسینی کالا:</h3>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; margin-top: 15px;">
    <div style="background: #ffffff; padding: 14px; border-radius: 8px; border: 1px solid #dbeafe;">
      <strong style="color: #1d4ed8; display: block; margin-bottom: 5px;">۱. پیش‌پرداخت نقدی:</strong>
      <span style="color: #334155; font-size: 14px;">دقیقاً ۵۰٪ از کل مبلغ فاکتور کالا در زمان سفارش به صورت نقدی پرداخت می‌شود.</span>
    </div>
    <div style="background: #ffffff; padding: 14px; border-radius: 8px; border: 1px solid #dbeafe;">
      <strong style="color: #1d4ed8; display: block; margin-bottom: 5px;">۲. بازپرداخت اقساطی:</strong>
      <span style="color: #334155; font-size: 14px;">۵۰٪ باقیمانده در اقساط ماهانه متناسب با بودجه خریدار (تا ۱۲ ماه) قسط‌بندی می‌گردد.</span>
    </div>
    <div style="background: #ffffff; padding: 14px; border-radius: 8px; border: 1px solid #dbeafe;">
      <strong style="color: #1d4ed8; display: block; margin-bottom: 5px;">۳. نرخ سود ماهانه:</strong>
      <span style="color: #334155; font-size: 14px;">کارمزد اقساط ماهیانه تنها ۳ درصد به مانده بدهی تعلق می‌گیرد.</span>
    </div>
    <div style="background: #ffffff; padding: 14px; border-radius: 8px; border: 1px solid #dbeafe;">
      <strong style="color: #1d4ed8; display: block; margin-bottom: 5px;">۴. تحویل کالا:</strong>
      <span style="color: #334155; font-size: 14px;">تحویل کالا فوری و در همان روز نهایی شدن چک‌ها در اهواز و استان خوزستان انجام می‌گیرد.</span>
    </div>
  </div>
</div>

<h3>یک مثال ملموس از محاسبه خرید با چک صیادی:</h3>
<p>فرض کنید قصد خرید یک <a href="https://hosseinykala.ir/product/pakshoma-21kg-twin-tub-washer/" target="_blank" rel="noopener"><strong>ماشین لباسشویی پاکشوما</strong></a> به ارزش ۳۰ میلیون تومان را دارید:</p>
<ul>
  <li><strong>پیش‌پرداخت اولیه (۵۰٪):</strong> ۱۵ میلیون تومان نقد پرداخت می‌شود.</li>
  <li><strong>مانده تسهیلات:</strong> ۱۵ میلیون تومان باقی می‌ماند.</li>
  <li>اگر بازپرداخت در قالب ۵ فقره چک ماهانه تنظیم شود، با احتساب کارمزد ۳ درصد ماهانه، هر چک با شفافیت کامل رقمی دقیق خواهد داشت و پس از ثبت چک‌ها در سامانه صیاد، دستگاه همان روز تحویل شما می‌گردد.</li>
</ul>

<h3>الزامات پذیرش چک صیادی:</h3>
<ol>
  <li>چک باید حتماً از دسته‌چک‌های جدید بنفش‌رنگ متصل به سامانه صیاد باشد.</li>
  <li>صاحب حساب نباید سابقه چک برگشتی رفع‌سوءاثرنشده در سیستم بانک مرکزی داشته باشد (وضعیت استعلام سفید).</li>
  <li>چک‌ها در سامانه صیاد (اپلیکیشن‌های بانکی یا پیچک) به نام فروشگاه ثبت و شناسه انتقال تایید شود.</li>
</ol>

<h2>۵. سایر طرح‌های فعال: کالا کارت مهر ایران و روش‌های پرداخت اعتباری (BNPL)</h2>

<h3>کالا کارت بانک قرض‌الحسنه مهر ایران:</h3>
<p>یکی از ارزان‌ترین روش‌های بانکی، طرح <strong>کالا کارت مهر ایران</strong> است. این تسهیلات بدون نیاز به مسدودسازی حساب، تا سقف ۱۵۰ الی ۳۰۰ میلیون تومان با کارمزد بسیار پایین <strong>۴ درصد قرض‌الحسنه</strong> اعطا می‌شود. بازپرداخت آن بین ۶ تا ۲۴ ماه است و گزینه‌ای فوق‌العاده برای کارمندان و خریدارانی است که یک ضامن رسمی معتبر در اختیار دارند.</p>

<h3>روش‌های لندتک و BNPL (الان بخر، بعداً پرداخت کن):</h3>
<p>برای کالاهای کوچک‌تر برقی نظیر جاروبرقی، سرخ‌کن بدون روغن، اسپرسوساز خانگی یا دستگاه‌های تصفیه آب، پلتفرم‌های دیجیتال نظیر <strong>اسنپ‌پی (SnappPay)</strong> خرید در ۴ قسط بدون سود و ضامن را میسر کرده‌اند. همچنین سامانه‌هایی چون <strong>دیجی‌پی</strong> و <strong>لندو</strong> امکان دریافت وام با سفته الکترونیکی بدون ضامن فیزیکی را مهیا ساخته‌اند.</p>

<h2>جدول مقایسه جامع تمام روش‌های خرید اقساطی لوازم خانگی</h2>
<div style="overflow-x: auto; margin: 25px 0;">
<table style="width: 100%; border-collapse: collapse; text-align: right; min-width: 650px; font-size: 14px;">
  <thead>
    <tr style="background-color: #1e293b; color: #ffffff;">
      <th style="padding: 12px 14px; border: 1px solid #334155;">روش و بستر</th>
      <th style="padding: 12px 14px; border: 1px solid #334155;">سقف اعتبار</th>
      <th style="padding: 12px 14px; border: 1px solid #334155;">کارمزد / سود</th>
      <th style="padding: 12px 14px; border: 1px solid #334155;">مدت بازپرداخت</th>
      <th style="padding: 12px 14px; border: 1px solid #334155;">ضمانت مورد نیاز</th>
      <th style="padding: 12px 14px; border: 1px solid #334155;">مهم‌ترین ویژگی</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background-color: #f8fafc;">
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: bold; color: #0284c7;">طرح بتا بانک رفاه</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">بر اساس توان حقوق</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">مصوب مرابحه</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">تا ۳۶ ماه</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0; color: #16a34a; font-weight: bold;">کسر خودکار از حقوق</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">بدون چک و ضامن کاغذی</td>
    </tr>
    <tr>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: bold; color: #4f46e5;">طرح باجت (کالانو تجارت)</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">تا ۳۰۰ میلیون تومان</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">نرخ مصوب بانکی</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">۱۲ تا ۳۶ ماه</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">اعتبارسنجی آنلاین / ضامن</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">ثبت‌نام ۱۰۰٪ موبایلی در اپ</td>
    </tr>
    <tr style="background-color: #f8fafc;">
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: bold; color: #e11d48;">وام خرید کالا بانک ملت</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">تا ۲۰۰ میلیون تومان</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">۱۸٪ تا ۲۳٪ سالیانه</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">تا ۶۰ ماه (۵ سال)</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">ضامن رسمی و پیش‌فاکتور</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">طولانی‌ترین بازه بازپرداخت</td>
    </tr>
    <tr style="background-color: #ecfdf5;">
      <td style="padding: 10px 14px; border: 1px solid #a7f3d0; font-weight: bold; color: #059669;">چک صیادی حسینی کالا</td>
      <td style="padding: 10px 14px; border: 1px solid #a7f3d0;">۵۰٪ مانده فاکتور</td>
      <td style="padding: 10px 14px; border: 1px solid #a7f3d0;">۳٪ ماهانه</td>
      <td style="padding: 10px 14px; border: 1px solid #a7f3d0;">تا ۱۲ ماه</td>
      <td style="padding: 10px 14px; border: 1px solid #a7f3d0;">چک بنفش صیادی وضعیت سفید</td>
      <td style="padding: 10px 14px; border: 1px solid #a7f3d0; font-weight: bold; color: #047857;">تحویل آنی کالا بدون نوبت بانک</td>
    </tr>
    <tr>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: bold; color: #d97706;">کالا کارت مهر ایران</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">تا ۳۰۰ میلیون تومان</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0; color: #16a34a; font-weight: bold;">۴٪ سالانه (قرض‌الحسنه)</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">۶ تا ۲۴ ماه</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">یک ضامن معتبر کارمند</td>
      <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">پایین‌ترین کارمزد در شبکه بانکی</td>
    </tr>
  </tbody>
</table>
</div>

<h2>کدام کالاها را می‌توان به صورت اقساطی از حسینی کالا خرید؟</h2>
<p>تمامی اقلام ضروری جهیزیه و منزل در فروشگاه حسینی با پوشش کامل ضمانت‌نامه رسمی و شرکتی مشمول طرح‌های اقساطی هستند:</p>
<ul>
  <li><a href="https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/" target="_blank" rel="noopener"><strong>انواع یخچال فریزر دوقلو و کمبی:</strong></a> مدل‌های پرچمدار مانند <a href="https://hosseinykala.ir/product/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1-%da%af%d9%84%d9%88%d8%b1%db%8c-%d9%be%d9%84%d8%a7%d8%b3-%d8%af%d9%88%d9%82%d9%84%d9%88-%da%a9%d9%84%d9%88%d8%b154-%d9%81%d9%88%d8%aa/" target="_blank" rel="noopener"><strong>یخچال فریزر دوقلو ۵۴ فوت کلور گلوری پلاس</strong></a> و <a href="https://hosseinykala.ir/product/depoint-max-du-twin-refrigerator-34ft/" target="_blank" rel="noopener"><strong>یخچال دوقلو ۳۴ فوت دیپوینت مدل MAX DU</strong></a> با موتورهای اینورتر و رده مصرف فوق‌کم‌مصرف.</li>
  <li><a href="https://hosseinykala.ir/product-category/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d9%84%d8%a8%d8%a7%d8%b3%d8%b4%d9%88%db%8c%db%8c/" target="_blank" rel="noopener"><strong>ماشین‌های لباسشویی اتوماتیک:</strong></a> مدل‌های ۸ و ۹ کیلویی کلور و پاکشوما مجهز به شستشوی بخار و موتور دایرکت درایو.</li>
  <li><a href="https://hosseinykala.ir/product-category/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d8%b8%d8%b1%d9%81%d8%b4%d9%88%db%8c%db%8c/" target="_blank" rel="noopener"><strong>ماشین ظرفشویی ۱۵ نفره:</strong></a> دستگاه‌های مبله ۳ سبد کم‌صدا نظیر ظرفشویی کلور CDW-H15V با رده انرژی +++A.</li>
  <li><a href="https://hosseinykala.ir/product-category/%da%a9%d9%88%d9%84%d8%b1-%d8%a2%d8%a8%db%8c/" target="_blank" rel="noopener"><strong>کولرهای آبی سلولزی و پرتابل:</strong></a> مدل‌های ریتون ۷۰۰۰ و ۱۶۰۰۰ متناسب با گرمای خوزستان.</li>
  <li><a href="https://hosseinykala.ir/product-category/%d8%aa%d8%b5%d9%81%db%8c%d9%87-%da%a9%d9%86%d9%86%d8%af%d9%87-%d8%a2%d8%a8/" target="_blank" rel="noopener"><strong>دستگاه‌های تصفیه آب خانگی:</strong></a> سیستم‌های ۶ تا ۸ مرحله‌ای اسمز معکوس <a href="https://hosseinykala.ir/product/soft-water-ir-06-purifier/" target="_blank" rel="noopener"><strong>سافت واتر IR-06</strong></a> برای شیرین‌سازی و تصفیه سختی آب.</li>
  <li><a href="https://hosseinykala.ir/product-category/%d8%ac%d8%a7%d8%b1%d9%88%d8%a8%d8%b1%d9%82%db%8c/" target="_blank" rel="noopener"><strong>جاروبرقی‌های کیسه‌ای و سطلی:</strong></a> از برندهای پاناسونیک، هیتاچی و بست.</li>
</ul>

<h2>راهنمای تصمیم‌گیری: کدام شیوه خرید اقساطی برای شما بهتر است؟</h2>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px; margin: 25px 0; direction: rtl;">
  <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px;">
    <h4 style="color: #0284c7; margin-top: 0;">اگر بازنشسته یا مستمری‌بگیر تأمین اجتماعی هستید:</h4>
    <p style="margin-bottom: 0; color: #475569; font-size: 14px;"><strong>طرح بتا بانک رفاه</strong> بی‌رقیب است. بدون نیاز به چک، سفته و ضامن، اقساط خود را مستقیماً از حقوق پرداخت کنید.</p>
  </div>
  <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px;">
    <h4 style="color: #059669; margin-top: 0;">اگر کالا را فوراً می‌خواهید و دسته‌چک صیادی دارید:</h4>
    <p style="margin-bottom: 0; color: #475569; font-size: 14px;"><strong>طرح چک صیادی حسینی کالا</strong> با ۵۰٪ پیش‌پرداخت، کالا را بدون فوت وقت و همان روز تحویل شما می‌دهد.</p>
  </div>
  <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px;">
    <h4 style="color: #4f46e5; margin-top: 0;">اگر به دنبال جهیزیه کامل با سقف بالا هستید:</h4>
    <p style="margin-bottom: 0; color: #475569; font-size: 14px;"><strong>طرح باجت تجارت (کالانو)</strong> یا کارت‌های رفاهی تا سقف ۳۰۰ میلیون تومان بودجه لازم را تأمین می‌کنند.</p>
  </div>
</div>

<h2>سوالات متداول درباره خرید اقساطی لوازم خانگی</h2>
<div style="background-color: #f9fafb; border-right: 4px solid #0284c7; padding: 18px; margin: 25px 0; direction: rtl;">
  <h3 style="margin-top: 0; color: #1e293b; font-size: 16px;">آیا گارانتی شرکتی کالاهای اقساطی با کالاهای نقدی تفاوتی دارد؟</h3>
  <p style="color: #4b5563;">خیر؛ تمام محصولات عرضه شده در فروشگاه حسینی کالا با گارانتی اصلی شرکتی، شناسه کالا و ضمانت اصالت معتبر تحویل داده می‌شوند و نحوه تسویه حساب (نقدی یا اقساطی) هیچ تفاوتی در حقوق خدمات پس از فروش و گارانتی ایجاد نمی‌کند.</p>

  <h3 style="color: #1e293b; font-size: 16px;">آیا برای خرید با چک صیادی حضور در فروشگاه اهواز الزامی است؟</h3>
  <p style="color: #4b5563;">همشهریان ساکن اهواز می‌توانند به شعبه حضوری ما در خیابان کاوه مراجعه فرمایند. برای سایر شهرهای استان خوزستان و کشور نیز امکان هماهنگی تلفنی، استعلام صیاد و ارسال پستی یا باربری چک‌ها و سپس تحویل کالا وجود دارد.</p>

  <h3 style="color: #1e293b; font-size: 16px;">در طرح بتای رفاه اگر حقوق فرد تکافوی کل مبلغ را ندهد چه می‌شود؟</h3>
  <p style="color: #4b5563;">در چنین وضعیتی، خریدار می‌تواند مابه‌التفاوت سقف اعتبار حقوق خود را به صورت پیش‌پرداخت واریز کند و الباقی مبلغ را در قالب اقساط کسر از حقوق ثبت نماید.</p>

  <h3 style="color: #1e293b; font-size: 16px;">آیا استعلام چک صیادی در همان لحظه انجام می‌شود؟</h3>
  <p style="color: #4b5563;">بله؛ استعلام وضعیت صیادی به صورت برخط در کمتر از ۵ دقیقه انجام شده و در صورت سفید بودن وضعیت اعتباری، چک‌ها ثبت و فاکتور نهایی می‌شود.</p>
</div>

<h2>مشاوره و خرید حضوری از فروشگاه لوازم خانگی حسینی در اهواز</h2>
<p>خرید لوازم خانگی نیازمند بررسی دقیق فنی و اطمینان از اصالت کالاست. کارشناسان ما در <a href="https://hosseinykala.ir/" target="_blank" rel="noopener"><strong>فروشگاه لوازم خانگی حسینی</strong></a> با بیش از سه دهه سابقه در بازار لوازم خانگی <strong>اهواز</strong> آماده‌اند تا شما را در انتخاب بهترین مدل‌ها متناسب با توان مالی و بودجه‌تان راهنمایی کنند.</p>
<p>جهت دریافت مشاوره رایگان تلفنی، استعلام موجودی روز یا اطلاع از جزئیات هر یک از طرح‌های اقساطی، می‌توانید با پشتیبانی فروشگاه در تماس باشید یا به صورت حضوری به شعب ما در خیابان کاوه اهواز تشریف بیاورید.</p>
"""

def publish_mega_pillar():
    print("=== Processing Mega Pillar Article ===", flush=True)
    load_all_tags()
    
    slug = 'home-appliances-installment-buying-guide'
    tag_names = [
        'خرید اقساطی لوازم خانگی',
        'طرح بتا بانک رفاه',
        'طرح باجت',
        'وام خرید کالا بانک ملت',
        'خرید اقساطی با چک صیادی',
        'فروشگاه لوازم خانگی حسینی',
        'خرید اقساطی در اهواز',
        'خرید قسطی جهیزیه',
        'کالا کارت مهر ایران'
    ]

    tag_ids = []
    for name in tag_names:
        tid = get_or_create_tag(name)
        if tid:
            tag_ids.append(tid)

    payload = {
        'title': 'راهنمای جامع خرید اقساطی لوازم خانگی در سال ۱۴۰۵؛ بررسی طرح بتا، باجت، بانک ملت و چک صیادی',
        'slug': slug,
        'status': 'future',
        'date': '2026-09-20T19:30:00',
        'categories': [54],
        'tags': tag_ids,
        'featured_media': 3845,
        'excerpt': 'راهنمای کامل خرید اقساطی لوازم خانگی. بررسی شرایط طرح بتای بانک رفاه برای بازنشستگان، طرح باجت تا ۳۰۰ میلیون، وام بانک ملت و خرید با چک صیادی در اهواز با تحویل فوری.',
        'content': MEGA_ARTICLE_HTML
    }

    url = "https://hosseinykala.ir/wp-json/wp/v2/posts"
    print("Posting article to WordPress...", flush=True)
    r = requests.post(url, headers=HEADERS, auth=AUTH, json=payload, timeout=40)

    if r.status_code in [200, 201]:
        data = r.json()
        print(f"[SUCCESS] Mega Pillar Article Scheduled!", flush=True)
        print(f"ID: {data.get('id')} | Status: {data.get('status')} | Date: {data.get('date')} | Link: {data.get('link')}", flush=True)
        return data.get('id')
    else:
        print(f"[FAILED] HTTP {r.status_code}: {r.text[:300]}", flush=True)
        return None

if __name__ == '__main__':
    publish_mega_pillar()
