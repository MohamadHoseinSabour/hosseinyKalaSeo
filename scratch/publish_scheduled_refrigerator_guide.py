import urllib.request
import urllib.parse
import base64
import json
import ssl
import sys

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

creds = base64.b64encode(b'agent:Mlwg pHHX NQ64 drrz 7ca2 IVto').decode('utf-8')

# 1. Tags
tag_names = ['راهنمای خرید یخچال فریزر', 'یخچال دوقلو', 'یخچال کمبی', 'یخچال ایستکول', 'یخچال الکترواستیل', 'یخچال کلور']
tag_ids = []

for name in tag_names:
    url_tag = 'https://hosseinykala.ir/wp-json/wp/v2/tags'
    req_t = urllib.request.Request(
        url_tag,
        data=json.dumps({'name': name}).encode('utf-8'),
        headers={'Authorization': f'Basic {creds}', 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        method='POST'
    )
    try:
        res = json.loads(urllib.request.urlopen(req_t, context=ctx, timeout=8).read().decode('utf-8'))
        tag_ids.append(res['id'])
    except Exception:
        try:
            req_get = urllib.request.Request(f"{url_tag}?search={urllib.parse.quote(name)}", headers={'Authorization': f'Basic {creds}'})
            existing = json.loads(urllib.request.urlopen(req_get, context=ctx, timeout=8).read().decode('utf-8'))
            if existing:
                tag_ids.append(existing[0]['id'])
        except Exception:
            pass

print("Refrig Tags IDs:", tag_ids)

# 2. Content HTML
content_html = '''
<h1 style="font-size: 26px; line-height: 1.6; color: #0f172a; margin-bottom: 24px; font-weight: 800;">راهنمای جامع خرید یخچال فریزر در سال ۱۴۰۵؛ مقایسه تخصصی دوقلو، کمبی، ساید و هتلی</h1>

<p>خرید یخچال فریزر شاید مهم‌ترین و پرهزینه‌ترین بخش در چیدمان هر آشپزخانه باشد؛ دستگاهی که باید حداقل ۱۰ تا ۱۵ سال بدون وقفه و به طور شبانه‌روزی کار کند. این حساسیت در مناطق گرمسیری مانند خوزستان و اهواز، با تابستان‌های بالای ۵۰ درجه و نوسانات فصلی برق، اهمیتی دوچندان پیدا می‌کند. یک انتخاب اشتباه در نوع موتور، ظرفیت یا سیستم خنک‌کننده می‌تواند آرامش خانواده را بر هم زده و هزینه‌های سنگین تعمیرات را تحمیل کند. در این راهنمای خرید جامع از <a href="https://hosseinykala.ir/" style="color: #2563eb; font-weight: bold;">فروشگاه لوازم خانگی حسینی</a> اهواز، تمام مدل‌های بازار ایران، تفاوت ساختاری دوقلو، کمبی و ساید، ابعاد استاندارد و شرایط اقلیمی را بررسی می‌کنیم.</p>

<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px 24px; margin: 25px 0;">
<h3 style="margin-top: 0; color: #1e293b; font-size: 18px;">آن‌چه در این راهنمای تخصصی مطالعه می‌کنید:</h3>
<ul style="color: #334155; line-height: 2;">
<li>مقایسه انواع فرم‌فاکتورها: دوقلو، کمبی (بالا/پایین)، ساید بای ساید و مینی هتلی</li>
<li>تحلیل تخصصی برندهای برتر: کلور (Clever)، دیپوینت (Depoint)، الکترواستیل و ایستکول</li>
<li>نکات حیاتی برای مناطق گرمسیری: کلاس اقلیمی تروپیکال (T) و موتور اینورتر دیجیتال</li>
<li>جدول مقایسه ابعاد، ظرفیت مفید به فوت و تناسب با متراژ آشپزخانه</li>
<li>فرمول طلایی محاسبه گنجایش یخچال بر اساس تعداد اعضای خانواده</li>
<li>شرایط خرید نقد و اقساطی یخچال با طرح‌های بانکی و کسر از حقوق در اهواز</li>
<li>پاسخ به سوالات متداول قبل از پرداخت وجه</li>
</ul>
</div>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">۱. مقایسه انواع یخچال فریزر؛ کدام مدل پاسخگوی نیاز شماست؟</h2>
<p>پیش از نگاه به مارک و برند، باید فرم هندسی مناسب خانه خود را مشخص کنید:</p>

<h3 style="color: #0f172a; font-size: 19px;">یخچال فریزر دوقلو (انتخاب اول خانواده‌های پرجمعیت):</h3>
<p>در این مدل، یخچال و فریزر دو کابین کاملاً مستقل هستند که کنار یکدیگر قرار می‌گیرند. بزرگ‌ترین مزیت مدل دوقلو، ظرفیت فوق‌العاده بالا (بین ۳۴ تا ۴۴ فوت) و امکان جابجایی آسان است؛ زیرا در اسباب‌کشی‌ها می‌توانید دو کابین را جداگانه حمل کنید. برای مشاهده جدیدترین مدل‌های این دسته می‌توانید بخش <a href="https://hosseinykala.ir/twin-refrigerator-buying-guide/" style="color: #2563eb; font-weight: 600;">راهنمای خرید یخچال فریزر دوقلو</a> را مشاهده کنید.</p>

<h3 style="color: #0f172a; font-size: 19px;">یخچال کمبی (بالا پایین):</h3>
<p>مدل‌های کمبی در دو نوع «فریزر بالا» یا «فریزر پایین» طراحی می‌شوند. امروزه مدل‌های فریزر پایین محبوب‌ترند زیرا بخش یخچال که روزانه بارها باز می‌شود، در تراز دید چشم قرار دارد. کمبی‌ها برای آشپزخانه‌های با عرض کم یا خانواده‌های ۲ تا ۴ نفره انتخابی کاملاً بهینه و اقتصادی هستند.</p>

<h3 style="color: #0f172a; font-size: 19px;">یخچال‌های کوچک و مینی هتلی (۳ تا ۹ فوت):</h3>
<p>برای دفاتر کار، اتاق‌های خواب، مطب‌ها و سوییت‌های دانشجویی، خرید یک مدل بزرگ توجیهی ندارد. برندهایی مانند ایستکول و کلور با تولید مدل‌های کوچک و شوکیس‌های شیشه‌ای، بازدهی عالی بدون اشغال فضا به ارمغان آورده‌اند.</p>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">۲. بررسی برندهای پیشرو بازار یخچال در ایران</h2>

<div style="display: grid; grid-template-columns: 1fr; gap: 20px; margin: 25px 0;">
<div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 18px;">
<h3 style="color: #0f172a; margin-top: 0; font-size: 18px;">کلور (Clever)؛ پیشتاز در موتورهای اینورتر کم‌صدا</h3>
<p style="color: #475569; line-height: 1.8; margin-bottom: 0;">یخچال‌های کلور با کمپرسورهای اینورتر هوشمند BLDC و تکنولوژی رادیاتور مخفی، یکی از بی‌صداترین محصولات بازار هستند. مدل‌های گلوری پلاس (Glory Plus)، روسو پلاس و کمبی‌های هوم‌بار این برند در رده مصرف انرژی بسیار کم کار می‌کنند. مشاهده مدل‌ها در صفحه <a href="https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/clover-refrigerators/" style="color: #2563eb; font-weight: 600;">یخچال فریزر کلور</a>.</p>
</div>

<div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 18px;">
<h3 style="color: #0f172a; margin-top: 0; font-size: 18px;">الکترواستیل (Electrosteel)؛ قدمت و اصالت در برودت</h3>
<p style="color: #475569; line-height: 1.8; margin-bottom: 0;">الکترواستیل با دهه‌ها سابقه درخشان در صنعت سرمایش، از موتورهای اروپایی با قدرت برودت فوق‌العاده بهره می‌برد. مدل‌های سری فیوچر (Future)، استار و دوقلوهای پرطرفدار این برند دارای بدنه آنتی‌باکتریال و سیستم سرمایش بدون برفک سریع هستند. بررسی بیشتر در دسته <a href="https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/electrosteel-refrigerators/" style="color: #2563eb; font-weight: 600;">یخچال فریزر الکترواستیل</a>.</p>
</div>

<div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 18px;">
<h3 style="color: #0f172a; margin-top: 0; font-size: 18px;">ایستکول (Eastcool)؛ سلطان یخچال‌های اداری و هتلی</h3>
<p style="color: #475569; line-height: 1.8; margin-bottom: 0;">اگر به دنبال یخچال مینی، ۵ فوت، ۹ فوت هتلی یا آبسردکن باکیفیت هستید، ایستکول بدون رقیب است. مصرف برق ناچیز، گاز مبرد سازگار با محیط زیست و ابعاد فشرده از نقاط قوت اصلی این برند است. بررسی در <a href="https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/eastcool-refrigerators/" style="color: #2563eb; font-weight: 600;">یخچال فریزر ایستکول</a>.</p>
</div>
</div>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">۳. فاکتورهای حیاتی برای خرید یخچال در شرایط آب‌وهوایی جنوب (خوزستان و اهواز)</h2>
<p>به یاد داشته باشید استانداردهای برودت در شهرهای معتدل با شهرهای گرمسیری متفاوت است. هنگام خرید در اهواز، به سه فاکتور اساسی توجه کنید:</p>
<ul style="color: #334155; line-height: 2;">
<li><strong>کلاس اقلیمی گرمسیری (Tropical / رده T):</strong> مطمئن شوید کمپرسور دستگاه در دمای بالای ۴۳ درجه تست شده و رده آب‌وهوایی آن T است تا در اوج گرمای تیر و مرداد، داخل کابین سرد بماند.</li>
<li><strong>کمپرسور اینورتر دیجیتال (Digital Inverter):</strong> موتورهای اینورتر بر خلاف مدل‌های قدیمی به صورت خاموش/روشن ناگهانی کار نمی‌کنند، بلکه دور موتور خود را متناسب با دمای محیط تنظیم می‌کنند. این امر مصرف برق را تا ۴۰ درصد کاهش داده و استهلاک قطعات را به حداقل می‌رساند.</li>
<li><strong>گردش هوای چندگانه (Multi Air Flow):</strong> وجود دریچه‌های متعدد سرما در تک‌تک طبقات، تضمین می‌کند که رطوبت سبزیجات حفظ شده و فاسد نشوند.</li>
</ul>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">جدول مقایسه‌ای ابعاد و ظرفیت یخچال‌های پرفروش</h2>
<div style="overflow-x: auto; margin: 25px 0;">
<table style="width: 100%; border-collapse: collapse; text-align: right; font-size: 15px;">
<thead>
<tr style="background: #0f172a; color: #ffffff;">
<th style="padding: 12px; border: 1px solid #cbd5e1;">نوع محصول</th>
<th style="padding: 12px; border: 1px solid #cbd5e1;">گنجایش متوسط</th>
<th style="padding: 12px; border: 1px solid #cbd5e1;">پهنای استاندارد (عرض)</th>
<th style="padding: 12px; border: 1px solid #cbd5e1;">مناسب برای خانواده</th>
</tr>
</thead>
<tbody>
<tr style="background: #f8fafc;">
<td style="padding: 10px; border: 1px solid #cbd5e1; font-weight: bold;">دوقلو عرض ۷۰ (کلور و دیپوینت)</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۴۰ تا ۴۴ فوت</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۱۴۰ سانتی‌متر (دو قلو کنار هم)</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۴ نفر به بالا (مصرف بالا)</td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #cbd5e1; font-weight: bold;">دوقلو عرض ۶۰ (الکترواستیل و کلور)</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۳۴ تا ۳۶ فوت</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۱۲۰ سانتی‌متر</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۳ تا ۵ نفره</td>
</tr>
<tr style="background: #f8fafc;">
<td style="padding: 10px; border: 1px solid #cbd5e1; font-weight: bold;">کمبی بالا پایین بزرگ (۲۷ تا ۳۰ فوت)</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۲۷ الی ۳۰ فوت</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۸۰ تا ۸۶ سانتی‌متر</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۲ تا ۴ نفره (آشپزخانه متوسط)</td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #cbd5e1; font-weight: bold;">مینی و هتلی (ایستکول و کلور)</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۵ تا ۱۰ فوت</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۵۰ تا ۵۵ سانتی‌متر</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">دفاتر اداری، مجردی و مطب</td>
</tr>
</tbody>
</table>
</div>

<div style="background: #f0fdf4; border: 2px solid #86efac; border-radius: 8px; padding: 22px; margin: 30px 0; direction: rtl;">
<h3 style="color: #14532d; margin-top: 0; font-size: 20px;">خرید اقساطی انواع یخچال و فریزر در فروشگاه حسینی کالا اهواز</h3>
<p style="color: #166534; font-size: 15px; line-height: 1.8;">شما همشهریان و خریداران گرامی در سراسر کشور می‌توانید برای خرید انواع یخچال با ضمانت رسمی و خدمات پس از فروش مطمئن، از طرح‌های اعتباری ویژه حسینی کالا استفاده نمایید:</p>
<ul style="color: #14532d; line-height: 2;">
<li><strong>طرح بتا بانک رفاه:</strong> ویژه بازنشستگان و مستمری‌بگیران تأمین اجتماعی بدون ضامن با کسر از حقوق. راهنما در <a href="https://hosseinykala.ir/refah-bank-beta-installment-guide/" style="color: #15803d; font-weight: bold;">طرح بتا بانک رفاه</a>.</li>
<li><strong>وام ۲۰۰ میلیونی بانک ملت:</strong> امکان دریافت فوری پیش‌فاکتور رسمی. بررسی جزئیات در <a href="https://hosseinykala.ir/mellat-bank-200m-appliances-loan-guide/" style="color: #15803d; font-weight: bold;">وام ۲۰۰ میلیونی بانک ملت</a>.</li>
<li><strong>طرح باجت بانک تجارت (کالانو):</strong> اعتبار دیجیتال تا ۳۰۰ میلیون تومان با بازپرداخت ۲۴ ماهه.</li>
<li><strong>خرید با چک صیادی:</strong> اقساط آسان با کارمزد منصفانه برای تمامی شاغلین و کسبه محترم.</li>
</ul>
<p style="margin-bottom: 0;"><a href="https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/" style="background: #15803d; color: #ffffff; padding: 10px 24px; border-radius: 6px; text-decoration: none; font-weight: bold; display: inline-block;">مشاهده کاتالوگ و قیمت تمام یخچال‌های موجود</a></p>
</div>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">پاسخ به سوالات پرتکرار خریداران (FAQ)</h2>
<div style="margin-top: 20px;">
<h4 style="color: #0f172a; margin-bottom: 6px;">یخچال دوقلو بهتر است یا ساید بای ساید؟</h4>
<p style="color: #475569; margin-top: 0; line-height: 1.8;">اگر اولویت شما فضای داخلی جادار، فریزر با کشوهای متعدد و حمل‌ونقل راحت در اثاث‌کشی است، بدون شک دوقلو انتخاب بهتری است. ساید بای ساید ظاهری مدرن‌تر دارد اما فضای فریزر آن به دلیل عمودی بودن محدودتر است.</p>

<h4 style="color: #0f172a; margin-bottom: 6px;">آیا موتورهای اینورتر در نوسانات برق آسیب‌پذیرترند؟</h4>
<p style="color: #475569; margin-top: 0; line-height: 1.8;">خیر، بردهای اینورتر مدرن دارای محافظ‌های داخلی دامنه ولتاژ هستند؛ با این حال استفاده از یک محافظ برق استاندارد شرکتی در ورودی برق یخچال در مناطقی مانند خوزستان همواره توصیه می‌شود.</p>

<h4 style="color: #0f172a; margin-bottom: 6px;">چگونه پیش‌فاکتور خرید یخچال برای وام بانکی بگیریم؟</h4>
<p style="color: #475569; margin-top: 0; line-height: 1.8;">با مراجعه حضوری به شعب فروشگاه لوازم خانگی حسینی در اهواز یا ارتباط با کارشناسان فروش از طریق پشتیبانی سایت، پیش‌فاکتور رسمی دارای شناسه صنف در کمترین زمان برای ارائه به بانک صادر می‌شود.</p>
</div>
'''

# 3. Payload
post_payload = {
    'title': 'راهنمای جامع خرید یخچال فریزر در سال ۱۴۰۵؛ مقایسه دوقلو، کمبی، ساید و هتلی',
    'slug': 'comprehensive-refrigerator-freezer-buying-guide',
    'status': 'future',
    'date': '2026-10-25T19:30:00',
    'categories': [54],
    'tags': tag_ids,
    'featured_media': 2465,
    'content': content_html,
    'excerpt': 'راهنمای کامل خرید انواع یخچال فریزر ایرانی؛ مقایسه ابعاد، گنجایش، موتور اینورتر و قیمت مدل‌های دوقلو، کمبی و هتلی کلور، الکترواستیل و دیپوینت در حسینی کالا اهواز.'
}

url_create = 'https://hosseinykala.ir/wp-json/wp/v2/posts'
req_create = urllib.request.Request(
    url_create,
    data=json.dumps(post_payload).encode('utf-8'),
    headers={'Authorization': f'Basic {creds}', 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    method='POST'
)

try:
    resp = urllib.request.urlopen(req_create, context=ctx, timeout=12)
    created_post = json.loads(resp.read().decode('utf-8'))
    new_id = created_post['id']
    print(f"Successfully created SCHEDULED post! ID: {new_id} | Status: {created_post['status']} | Date: {created_post['date']}")
    
    # 4. Set Rank Math Meta
    url_rm = 'https://hosseinykala.ir/wp-json/rankmath/v1/updateMeta'
    rm_payload = {
        'objectID': new_id,
        'objectType': 'post',
        'meta': {
            'rank_math_title': 'راهنمای خرید یخچال فریزر ۱۴۰۵؛ مقایسه دوقلو، کمبی و ساید | حسینی کالا',
            'rank_math_description': 'کدام یخچال برای خانه شما مناسب‌تر است؟ مقایسه ابعاد، موتور اینورتر و قیمت یخچال دوقلو، کمبی و هتلی کلور، دیپوینت و الکترواستیل در حسینی کالا اهواز.',
            'rank_math_focus_keyword': 'راهنمای خرید یخچال فریزر, خرید یخچال در اهواز'
        }
    }
    req_rm = urllib.request.Request(
        url_rm,
        data=json.dumps(rm_payload).encode('utf-8'),
        headers={'Authorization': f'Basic {creds}', 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        method='POST'
    )
    urllib.request.urlopen(req_rm, context=ctx, timeout=8)
    print("Rank Math Meta tags configured for the scheduled refrigerator post!")
except Exception as e:
    print("Error creating scheduled post:", e)
