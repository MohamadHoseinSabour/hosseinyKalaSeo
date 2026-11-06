import urllib.request
import base64
import json
import ssl
import sys

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

creds = base64.b64encode(b'agent:Mlwg pHHX NQ64 drrz 7ca2 IVto').decode('utf-8')

# 1. Create or fetch tags
tag_names = ['جاروبرقی بست', 'قیمت جاروبرقی بست', 'جاروبرقی بست bvc pc18b', 'راهنمای خرید جاروبرقی']
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
    except Exception as e:
        # If tag already exists, find its ID
        try:
            req_get = urllib.request.Request(f"{url_tag}?search={urllib.parse.quote(name)}", headers={'Authorization': f'Basic {creds}'})
            existing = json.loads(urllib.request.urlopen(req_get, context=ctx, timeout=8).read().decode('utf-8'))
            if existing:
                tag_ids.append(existing[0]['id'])
        except Exception:
            pass

print("Tags IDs:", tag_ids)

# 2. Article HTML Content
content_html = '''
<h1 style="font-size: 26px; line-height: 1.6; color: #0f172a; margin-bottom: 24px; font-weight: 800;">بررسی تخصصی جاروبرقی بست مدل BVC-PC18B؛ ارزش خرید، قدرت مکش و مقایسه با رقبا</h1>

<p>پیدا کردن یک جاروبرقی باکیفیت و خوش‌قیمت در آشفته‌بازار فعلی لوازم خانگی به چالشی بزرگ برای خانواده‌ها و زوج‌های جوان تبدیل شده است. در میان برندهای مختلف، <strong>جاروبرقی بست مدل BVC-PC18B</strong> توانسته با تکیه بر اعتبار گروه صنعتی انتخاب (تولیدکننده اسنوا و دوو) توجه خریداران هوشمند را جلب کند. اما آیا موتور ۱۴۰۰ واتی این دستگاه توانایی نظافت عمقی فرش‌های پرتراکم ایرانی را دارد؟ در این مطلب تحلیلی و تخصصی از <a href="https://hosseinykala.ir/" style="color: #2563eb; font-weight: bold;">فروشگاه لوازم خانگی حسینی</a> اهواز، تمام زوایای فنی، مزایا، معایب و تجربه کارکرد این مدل را بی‌پرده کالبدشکافی می‌کنیم.</p>

<div style="background: #f1f5f9; border-radius: 8px; padding: 18px 24px; margin: 25px 0;">
<h3 style="margin-top: 0; color: #1e293b; font-size: 18px;">آن‌چه در این بررسی تخصصی می‌خوانید:</h3>
<ul style="color: #334155; line-height: 2;">
<li>برند بست (Bost) ساخت کجاست و چه پیشینه‌ای دارد؟</li>
<li>کالبدشکافی طراحی، جنس بدنه و ارگونومی BVC-PC18B</li>
<li>بررسی توان موتور و قدرت مکش واقعی روی فرش و سرامیک</li>
<li>سیستم فیلتراسیون بهداشتی و ظرفیت مخزن ۶.۵ لیتری</li>
<li>جدول کامل مشخصات فنی و مقایسه با جاروبرقی‌های هم‌رده</li>
<li>نقاط قوت و معایب غیرقابل انکار دستگاه از دید خریداران</li>
<li>گارانتی رسمی و شرایط خرید نقد و اقساطی در اهواز و سراسر ایران</li>
</ul>
</div>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">برند بست (Bost) ساخت کجاست؟</h2>
<p>برند <strong>بست (Bost)</strong> یکی از زیرمجموعه‌های استراتژیک <strong>گروه انتخاب</strong> است؛ همان مجتمع صنعتی نام‌آشنایی که برندهای پیشرو مانند دوو (Daewoo) و اسنوا (Snowa) را تولید و روانه بازار می‌کند. هدف اصلی راه‌اندازی برند بست، ارائه محصولاتی کاربردی، بادوام و کاملاً اقتصادی برای خانواده‌هایی است که تمایل ندارند هزینه‌های سنگین تکنولوژی‌های لوکس را بپردازند اما خواهان ضمانت‌نامه معتبر شرکتی و دسترسی آسان به قطعات هستند.</p>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">طراحی ظاهری و کیفیت ساخت بدنه</h2>
<p>در نگاه اول، فرم تخم‌مرغی و جمع‌وجور جاروبرقی بست جلب توجه می‌کند. بدنه دستگاه از پلیمر تقویت‌شده ABS ساخته شده که مقاومت فوق‌العاده‌ای در برابر ضربه‌های اتفاقی ناشی از برخورد با پایه‌های مبل و گوشه‌های دیوار دارد. دستگیره ارگونومیک، چرخ‌های بزرگ با روکش نرم و سیم جمع‌کن اتوماتیک پرسرعت باعث شده‌اند جابجایی دستگاه روی فرش‌های ضخیم و کفپوش‌های سرامیکی بدون هیچ‌گونه زحمت انجام شود.</p>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">توان موتور و مکش واقعی روی سطوح مختلف</h2>
<p>یکی از پرتکرارترین پرسش‌های کاربران این است: <em>«آیا موتور ۱۴۰۰ وات برای جاروبرقی ضعیف نیست؟»</em> پاسخ منفی است. در استاندارد مهندسی جدید جاروبرقی‌های مدرن، برخلاف گذشته عدد توان مصرفی بر حسب وات نشان‌دهنده مصرف بهینه انرژی است، نه ضعف مکش. موتور تعبیه‌شده روی مدل BVC-PC18B راندمان مکانیکی فوق‌العاده‌ای ایجاد می‌کند و قادر است سنگین‌ترین ریزگردها، پرزها و موهای حیوانات خانگی را از لابلای بافت فرش بیرون بکشد.</p>

<div style="background: #eff6ff; border-right: 4px solid #3b82f6; padding: 18px; margin: 25px 0; border-radius: 4px;">
<p style="margin: 0; color: #1e40af; line-height: 1.8;"><strong>تجربه کارشناسان حسینی کالا:</strong> در تست‌های عملی انجام شده در شوروم فروشگاه، جاروبرقی بست حتی در ولوم‌های میانی مکش کافی برای جمع‌آوری دانه‌های شنی و گردوخاک از روی سرامیک را فراهم کرد بدون این‌که موتور با داغی شدید یا افت راندمان مواجه شود.</p>
</div>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">فیلتراسیون بهداشتی و مخزن ۶.۵ لیتری کیسه‌ای</h2>
<p>جاروبرقی بست مدل BVC-PC18B یک مدل کیسه‌دار است. گنجایش مخزن زباله آن <strong>۶.۵ لیتر</strong> است؛ ظرفیتی فوق‌العاده بزرگ که شما را تا ماه‌ها از خرید مداوم یا تعویض پاکت بی‌نیاز می‌کند. همچنین سیستم فیلتراسیون چندمرحله‌ای تعبیه‌شده در خروجی هوای موتور، مانع از بازگشت ذرات میکرونی آلرژی‌زا به هوای خانه می‌شود که این موضوع برای سالمندان و کودکان دارای آسم بسیار حیاتی است.</p>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">جدول مشخصات فنی جاروبرقی بست BVC-PC18B</h2>
<div style="overflow-x: auto; margin: 25px 0;">
<table style="width: 100%; border-collapse: collapse; text-align: right; font-size: 15px;">
<thead>
<tr style="background: #0f172a; color: #ffffff;">
<th style="padding: 12px; border: 1px solid #cbd5e1;">مشخصه فنی</th>
<th style="padding: 12px; border: 1px solid #cbd5e1;">جزئیات در مدل BVC-PC18B</th>
</tr>
</thead>
<tbody>
<tr style="background: #f8fafc;">
<td style="padding: 10px; border: 1px solid #cbd5e1; font-weight: bold;">برند سازنده</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">بست (Bost) - گروه صنعتی انتخاب</td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #cbd5e1; font-weight: bold;">توان موتور</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۱۴۰۰ وات با راندمان مکش بالا</td>
</tr>
<tr style="background: #f8fafc;">
<td style="padding: 10px; border: 1px solid #cbd5e1; font-weight: bold;">نوع مخزن</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">کیسه‌ای (ظرفیت حجیم ۶.۵ لیتر)</td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #cbd5e1; font-weight: bold;">لوله تلسکوپی</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">فلزی با قابلیت تنظیم ارتفاع متناسب با قد کاربر</td>
</tr>
<tr style="background: #f8fafc;">
<td style="padding: 10px; border: 1px solid #cbd5e1; font-weight: bold;">طول کابل برق و شعاع کارکرد</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">کابل ۵ متری با شعاع حرکتی حدود ۸ متر</td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #cbd5e1; font-weight: bold;">گارانتی و خدمات</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۲۴ ماه ضمانت رسمی انتخاب سرویس حامی</td>
</tr>
</tbody>
</table>
</div>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">مزایا و معایب واقعی دستگاه</h2>
<p>برای تصمیم‌گیری آگاهانه، مهم است که مزایا و محدودیت‌های این جاروبرقی را در کفه ترازو قرار دهید:</p>
<ul style="line-height: 2; color: #334155;">
<li><strong style="color: #059669;">مزایا:</strong> قیمت بسیار رقابتی، مخزن غول‌پیکر ۶.۵ لیتری، دسترسی همیشگی به قطعات و کیسه در بازار، گارانتی ۲ ساله انتخاب سرویس، بدنه مستحکم در برابر ضربه.</li>
<li><strong style="color: #dc2626;">معایب:</strong> نبود کنترل مکش روی دسته (تنظیم ولوم فقط از روی بدنه انجام می‌شود) و طول سیم ۵ متری که برای سالن‌های بسیار وسیع بالای ۱۲۰ متر نیازمند جابجایی پریز است.</li>
</ul>

<div style="background: #f8fafc; border: 2px dashed #cbd5e1; border-radius: 8px; padding: 22px; margin: 30px 0; text-align: center;">
<h3 style="color: #0f172a; margin-top: 0; font-size: 20px;">خرید مستقیم جاروبرقی بست BVC-PC18B با گارانتی اصلی</h3>
<p style="color: #475569; font-size: 15px; margin-bottom: 20px;">جهت مشاهده مشخصات تکمیلی، استعلام قیمت روز و ثبت سفارش آنلاین یا حضوری، می‌توانید از صفحه محصول در سایت حسینی کالا دیدن فرمایید:</p>
<a href="https://hosseinykala.ir/product/bost-bvc-pc18b-vacuum-cleaner/" style="background: #2563eb; color: #ffffff; padding: 12px 28px; border-radius: 6px; text-decoration: none; font-weight: bold; display: inline-block;">مشاهده و خرید جاروبرقی بست مدل BVC-PC18B</a>
<p style="margin-top: 15px; font-size: 14px; color: #64748b;">همچنین برای بررسی سایر برندها می‌توانید به بخش <a href="https://hosseinykala.ir/product-category/washing-cleaning/%D8%AC%D8%A7%D8%B1%D9%88%D8%A8%D8%B1%D9%82%DB%8C/bost-vacuum-cleaners/" style="color: #2563eb; font-weight: 600;">جاروبرقی بست</a> یا دسته‌بندی کلی <a href="https://hosseinykala.ir/product-category/washing-cleaning/%D8%AC%D8%A7%D8%B1%D9%88%D8%A8%D8%B1%D9%82%DB%8C/" style="color: #2563eb; font-weight: 600;">جاروبرقی</a> مراجعه نمایید.</p>
</div>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">خرید اقساطی لوازم خانگی در اهواز</h2>
<p>اگر در حال تکمیل جهیزیه یا خرید اقساطی هستید، این کالا به همراه تمام لوازم خانگی بزرگ و کوچک در <a href="https://hosseinykala.ir/" style="color: #2563eb; font-weight: bold;">فروشگاه لوازم خانگی حسینی</a> اهواز به صورت اقساطی قابل تهیه است. شما می‌توانید از طریق <a href="https://hosseinykala.ir/refah-bank-beta-installment-guide/" style="color: #2563eb;">طرح بتا بانک رفاه</a>، <a href="https://hosseinykala.ir/bajet-tejarat-refah-300m-appliances/" style="color: #2563eb;">اعتبار باجت تجارت</a> یا چک صیادی بدون ضامن سفارش خود را نهایی کنید.</p>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">سؤالات متداول خریداران</h2>
<div style="margin-top: 20px;">
<h4 style="color: #0f172a; margin-bottom: 6px;">آیا جاروبرقی بست پاکت دائمی دارد یا یک‌بار مصرف؟</h4>
<p style="color: #475569; margin-top: 0; line-height: 1.8;">این محصول قابلیت استفاده از هر دو نوع پاکت را دارد؛ پاکت پارچه‌ای دائمی قابل شستشو در بسته‌بندی موجود است و از پاکت‌های استاندارد ضدآلرژی هپا نیز پشتیبانی می‌کند.</p>

<h4 style="color: #0f172a; margin-bottom: 6px;">شرایط گارانتی انتخاب سرویس برای جاروبرقی بست چگونه است؟</h4>
<p style="color: #475569; margin-top: 0; line-height: 1.8;">دستگاه دارای ۲۴ ماه ضمانت‌نامه قطعات و موتور توسط شرکت انتخاب سرویس حامی است که با فعال‌سازی پیامکی از لحظه خرید معتبر خواهد بود.</p>

<h4 style="color: #0f172a; margin-bottom: 6px;">نحوه ارسال به سراسر کشور چگونه است؟</h4>
<p style="color: #475569; margin-top: 0; line-height: 1.8;">سفارش‌ها در شهر اهواز با پیک اختصاصی در کمتر از چند ساعت و برای کلیه شهرستان‌های کشور با بسته‌بندی ایمن و پست پیشتاز یا باربری ارسال می‌شوند.</p>
</div>
'''

# 3. Post Payload
post_payload = {
    'title': 'بررسی تخصصی جاروبرقی بست مدل BVC-PC18B؛ کیفیت، قدرت مکش و راهنمای خرید',
    'slug': 'bost-bvc-pc18b-vacuum-cleaner-review',
    'status': 'future',
    'date': '2026-10-22T19:30:00',
    'categories': [54],
    'tags': tag_ids,
    'featured_media': 2886,
    'content': content_html,
    'excerpt': 'بررسی جامع و تخصصی جاروبرقی بست مدل BVC-PC18B موتور ۱۴۰۰ وات با مخزن ۶.۵ لیتری و ضمانت ۲۴ ماهه انتخاب سرویس. نقد مکش، مزایا و معایب در حسینی کالا اهواز.'
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
    
    # 4. Set Rank Math Meta for the new post
    url_rm = 'https://hosseinykala.ir/wp-json/rankmath/v1/updateMeta'
    rm_payload = {
        'objectID': new_id,
        'objectType': 'post',
        'meta': {
            'rank_math_title': 'بررسی جاروبرقی بست مدل BVC-PC18B موتور ۱۴۰۰ وات؛ ارزش خرید دارد؟ | حسینی کالا',
            'rank_math_description': 'نقد و بررسی تخصصی جاروبرقی بست مدل BVC-PC18B؛ آیا موتور ۱۴۰۰ وات مکش کافی دارد؟ مقایسه با رقبا، مزایا و معایب و خرید اقساطی در فروشگاه حسینی کالا اهواز.',
            'rank_math_focus_keyword': 'جاروبرقی بست, جاروبرقی بست bvc pc18b'
        }
    }
    req_rm = urllib.request.Request(
        url_rm,
        data=json.dumps(rm_payload).encode('utf-8'),
        headers={'Authorization': f'Basic {creds}', 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        method='POST'
    )
    urllib.request.urlopen(req_rm, context=ctx, timeout=8)
    print("Rank Math Meta tags configured for the scheduled post!")
except Exception as e:
    print("Error creating scheduled post:", e)
