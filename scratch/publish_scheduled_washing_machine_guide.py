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
tag_names = ['راهنمای خرید ماشین لباسشویی', 'لباسشویی کلور', 'لباسشویی دوو', 'ماشین لباسشویی اینورتر', 'خرید لباسشویی در اهواز']
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

print("Washing Machine Tags IDs:", tag_ids)

# 2. Content HTML
content_html = '''
<h1 style="font-size: 26px; line-height: 1.6; color: #0f172a; margin-bottom: 24px; font-weight: 800;">راهنمای جامع خرید ماشین لباسشویی متناسب با سختی آب و اقلیم خوزستان و اهواز</h1>

<p>خرید ماشین لباسشویی در استان خوزستان و شهر اهواز، قواعد متفاوتی نسبت به سایر نقاط کشور دارد. بالا بودن املاح کلسیم و منیزیم (TDS بالا) در آب لوله‌کشی شهری، نشست مداوم ریزگردها روی لباس‌ها که نیاز به شستشوی مکرر ایجاد می‌کند و نوسانات ولتاژ برق در فصل گرما، سه عاملی هستند که اگر در انتخاب دستگاه لحاظ نشوند، طول عمر گران‌ترین لباسشویی‌ها را به کمتر از ۳ سال کاهش می‌دهند. در این مقاله تخصصی از کارشناسان فنی <a href="https://hosseinykala.ir/" style="color: #2563eb; font-weight: bold;">فروشگاه لوازم خانگی حسینی</a> اهواز، یاد می‌گیرید که چه فناوری‌هایی مانع از سوختن المنت و رسوب‌زدگی دیگ لباسشویی می‌شوند و کدام برندها برای این اقلیم ایده‌آل هستند.</p>

<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px 24px; margin: 25px 0;">
<h3 style="margin-top: 0; color: #1e293b; font-size: 18px;">سرفصل‌های این راهنمای تخصصی:</h3>
<ul style="color: #334155; line-height: 2;">
<li>چرا سختی آب اهواز قاتل خاموش ماشین لباسشویی است؟</li>
<li>فناوری‌های حیاتی: المنت‌های سرامیکی، موتور دایرکت درایو و سیستم‌های ضد کف</li>
<li>انتخاب ظرفیت هوشمندانه: مقایسه کاربردی مدل‌های ۷، ۸ و ۹ کیلویی</li>
<li>بررسی برندهای برتر بازار ایران: کلور (Clever)، دوو (Daewoo)، پاکشوما و بست</li>
<li>جدول مقایسه سرعت چرخش (RPM)، نوع موتور و رده مصرف انرژی</li>
<li>روش‌های طلایی نگهداری و رسوب‌زدایی پیشگیرانه در آب‌وهوای جنوب</li>
<li>طرح‌های ویژه خرید اقساطی لباسشویی در اهواز بدون ضامن</li>
</ul>
</div>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">۱. سختی آب خوزستان چه بلایی سر لباسشویی می‌آورد؟</h2>
<p>آب سنگین باعث تشکیل لایه‌های ضخیم کربنات کلسیم روی <strong>المنت حرارتی (Heater)</strong> و جداره خارجی دیگ شستشو می‌شود. این لایه رسوبی مانند عایق حرارتی عمل کرده و مانع از انتقال گرما به آب می‌شود؛ در نتیجه المنت برای گرم کردن آب باید دو تا سه برابر زمان معمول کار کند که به سوختن المنت، افزایش تصاعدی قبض برق و عدم حل شدن کامل پودر شوینده در الیاف پارچه ختم می‌شود.</p>

<div style="background: #fef2f2; border-right: 4px solid #ef4444; padding: 18px; margin: 25px 0; border-radius: 4px;">
<p style="margin: 0; color: #991b1b; line-height: 1.8;"><strong>راهکار طلایی حسینی کالا:</strong> هنگام خرید در اهواز، حتماً مدلی را انتخاب کنید که مجهز به <em>المنت با پوشش سرامیکی ضد رسوب (Ceramic Heater)</em> باشد یا همزمان با نصب، یک فیلتر پلی‌فسفات مغناطیسی در مسیر شیر ورودی آب دستگاه تعبیه کنید.</p>
</div>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">۲. تفاوت موتور تسمه‌ای و بدون تسمه (Direct Drive BLDC)</h2>
<p>لباسشویی‌های نسل جدید به موتورهای بدون تسمه دایرکت درایو (Direct Drive) مجهز هستند. در این مدل‌ها، دیگ شستشو مستقیماً روی شفت موتور سوار است؛ این یعنی:</p>
<ul style="color: #334155; line-height: 2;">
<li>حذف تسمه و پولی و در نتیجه خداحافظی با لرزش‌های شدید و صدای ناهنجار در دور خشک‌کن ۱۴۰۰ دور.</li>
<li>کاهش استهلاک قطعات مکانیکی و افزایش طول عمر مفید موتور تا بالای ۱۰ سال.</li>
<li>مصرف انرژی بهینه در رده‌های بالاتر از +++A.</li>
</ul>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">۳. ظرفیت مناسب؛ ۸ کیلویی بخریم یا ۹ کیلویی؟</h2>
<p>خانواده‌های خوزستانی به دلیل شستشوی منظم ملحفه‌ها، پرده‌ها و پتوهای مسافرتی یک‌نفره، بیشترین گرایش را به مدل‌های پرظرفیت دارند. اگر خانواده ۲ تا ۳ نفره هستید مدل‌های ۸ کیلویی کاملاً پاسخگو است، اما اگر تعداد نفرات ۴ نفر یا بیشتر است یا قصد دارید روتختی‌های سنگین را در خانه بشویید، مدل‌های ۹ کیلویی انتخاب مطمئن‌تری خواهند بود. برای تحلیل آماری این موضوع می‌توانید مقاله <a href="https://hosseinykala.ir/washing-machine-8kg-vs-9kg-guide/" style="color: #2563eb; font-weight: 600;">مقایسه لباسشویی ۸ و ۹ کیلویی</a> را مطالعه کنید.</p>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">۴. بررسی برندهای پرچمدار در بازار ایران</h2>

<div style="display: grid; grid-template-columns: 1fr; gap: 20px; margin: 25px 0;">
<div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 18px;">
<h3 style="color: #0f172a; margin-top: 0; font-size: 18px;">ماشین لباسشویی کلور (Clever) سری BMW</h3>
<p style="color: #475569; line-height: 1.8; margin-bottom: 0;">کلور با استفاده از موتورهای فوق کم‌صدا BLDC اینورتر، پنل‌های تمام‌لمسی مدرن و تکنولوژی حباب‌ساز، البسه را در دمای پایین آب با بالاترین تمیزی می‌شوید که این ویژگی برای آب دارای رسوب اهواز بسیار اثربخش است. مشاهده مدل‌ها در دسته <a href="https://hosseinykala.ir/product-category/washing-cleaning/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d9%84%d8%a8%d8%a7%d8%b3%d8%b4%d9%88%db%8c%db%8c/clover-washing-machines/" style="color: #2563eb; font-weight: 600;">لباسشویی کلور</a>.</p>
</div>

<div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 18px;">
<h3 style="color: #0f172a; margin-top: 0; font-size: 18px;">ماشین لباسشویی دوو (Daewoo)</h3>
<p style="color: #475569; line-height: 1.8; margin-bottom: 0;">دوو به عنوان برندی معتبر با گارانتی ۲۴ ماهه انتخاب سرویس، سیستم شستشوی همراه با بخار (Steam Care) و دیگ زمردی ضد آسیب به الیاف را در مدل‌های کاریزما و لایف ارائه داده است.</p>
</div>
</div>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">جدول مقایسه مشخصات لباسشویی‌های مدرن</h2>
<div style="overflow-x: auto; margin: 25px 0;">
<table style="width: 100%; border-collapse: collapse; text-align: right; font-size: 15px;">
<thead>
<tr style="background: #0f172a; color: #ffffff;">
<th style="padding: 12px; border: 1px solid #cbd5e1;">مدل / برند</th>
<th style="padding: 12px; border: 1px solid #cbd5e1;">ظرفیت دیگ</th>
<th style="padding: 12px; border: 1px solid #cbd5e1;">نوع موتور</th>
<th style="padding: 12px; border: 1px solid #cbd5e1;">حداکثر سرعت خشک‌کن</th>
<th style="padding: 12px; border: 1px solid #cbd5e1;">سیستم شستشو با بخار</th>
</tr>
</thead>
<tbody>
<tr style="background: #f8fafc;">
<td style="padding: 10px; border: 1px solid #cbd5e1; font-weight: bold;">کلور سری BMW T2</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۹ کیلوگرم</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">دایرکت درایو BLDC اینورتر</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۱۴۰۰ دور در دقیقه</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">دارد (Steam Wash)</td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #cbd5e1; font-weight: bold;">کلور سری BMW T3</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۸ کیلوگرم</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">اینورتر هوشمند کم‌لرزش</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۱۲۰۰ تا ۱۴۰۰ دور</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">دارد</td>
</tr>
<tr style="background: #f8fafc;">
<td style="padding: 10px; border: 1px solid #cbd5e1; font-weight: bold;">دوو مدل LM-9170</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۹ کیلوگرم</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">دایرکت درایو ۱۴۰۰ دور</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">۱۴۰۰ دور در دقیقه</td>
<td style="padding: 10px; border: 1px solid #cbd5e1;">دارد (نانوسیلور)</td>
</tr>
</tbody>
</table>
</div>

<div style="background: #f0fdf4; border: 2px solid #86efac; border-radius: 8px; padding: 22px; margin: 30px 0; direction: rtl;">
<h3 style="color: #14532d; margin-top: 0; font-size: 20px;">خرید اقساطی ماشین لباسشویی در اهواز (بدون پیش‌پرداخت و بدون ضامن)</h3>
<p style="color: #166534; font-size: 15px; line-height: 1.8;">در <a href="https://hosseinykala.ir/" style="color: #15803d; font-weight: bold;">فروشگاه لوازم خانگی حسینی</a> اهواز، شرایط تسهیلاتی متعددی برای خرید ماشین لباسشویی فراهم شده است:</p>
<ul style="color: #14532d; line-height: 2;">
<li><strong>طرح بتا بانک رفاه:</strong> ویژه بازنشستگان و مستمری‌بگیران تأمین اجتماعی با کسر از حقوق. راهنمای ثبت در <a href="https://hosseinykala.ir/refah-bank-beta-installment-guide/" style="color: #15803d; font-weight: bold;">طرح بتا بانک رفاه</a>.</li>
<li><strong>وام ۲۰۰ میلیونی خرید کالای بانک ملت:</strong> صدور پیش‌فاکتور فوری در شعب اهواز. راهنمای کامل در <a href="https://hosseinykala.ir/mellat-bank-200m-appliances-loan-guide/" style="color: #15803d; font-weight: bold;">وام بانک ملت</a>.</li>
<li><strong>اعتبار ۳۰۰ میلیونی باجت تجارت:</strong> خرید با اپلیکیشن باجت با بازپرداخت ۲۴ ماهه. راهنما در <a href="https://hosseinykala.ir/bajet-tejarat-refah-300m-appliances/" style="color: #15803d; font-weight: bold;">طرح باجت تجارت</a>.</li>
<li><strong>خرید با چک صیادی:</strong> اقساط متناسب با توان مالی شما.</li>
</ul>
<p style="margin-bottom: 0;"><a href="https://hosseinykala.ir/product-category/washing-cleaning/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d9%84%d8%a8%d8%a7%d8%b3%d8%b4%d9%88%db%8c%db%8c/" style="background: #15803d; color: #ffffff; padding: 10px 24px; border-radius: 6px; text-decoration: none; font-weight: bold; display: inline-block;">مشاهده قیمت و مدل‌های ماشین لباسشویی در سایت</a></p>
</div>

<h2 style="color: #1e293b; font-size: 22px; margin-top: 32px;">پاسخ به سوالات متداول</h2>
<div style="margin-top: 20px;">
<h4 style="color: #0f172a; margin-bottom: 6px;">هر چند وقت یک‌بار باید لباسشویی در اهواز رسوب‌زدایی شود؟</h4>
<p style="color: #475569; margin-top: 0; line-height: 1.8;">با توجه به سختی بالای آب، توصیه می‌شود هر دو ماه یک‌بار یک دوره جرم‌گیری کامل با پودر یا قرص مخصوص رسوب‌زدایی در برنامه شستشوی با دمای ۶۰ درجه بدون لباس اجرا شود.</p>

<h4 style="color: #0f172a; margin-bottom: 6px;">آیا استفاده از مایع لباسشویی بهتر از پودر است؟</h4>
<p style="color: #475569; margin-top: 0; line-height: 1.8;">بله؛ مایع لباسشویی در آب سرد و آب دارای املاح به مراتب سریع‌تر و کامل‌تر حل می‌شود و هیچ‌گونه لکه سفیدی روی لباس‌های تیره یا رسوبی در جاپودری بر جای نمی‌گذارد.</p>
</div>
'''

# 3. Payload
post_payload = {
    'title': 'راهنمای خرید ماشین لباسشویی متناسب با آب‌وهوا و سختی آب خوزستان و اهواز',
    'slug': 'washing-machine-buying-guide-khuzestan',
    'status': 'future',
    'date': '2026-10-27T19:30:00',
    'categories': [54],
    'tags': tag_ids,
    'featured_media': 2506,
    'content': content_html,
    'excerpt': 'راهنمای جامع انتخاب ماشین لباسشویی مناسب اقلیم گرمسیری و سختی آب اهواز؛ بررسی موتور دایرکت درایو، هیتر سرامیکی، ظرفیت ۸ و ۹ کیلویی و خرید اقساطی در حسینی کالا.'
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
            'rank_math_title': 'راهنمای خرید ماشین لباسشویی متناسب با سختی آب اهواز | حسینی کالا',
            'rank_math_description': 'کدام لباسشویی در برابر سختی آب خوزستان دوام بیشتری دارد؟ بررسی موتور دایرکت درایو، هیتر سرامیکی، ظرفیت ۸ و ۹ کیلویی و خرید اقساطی در حسینی کالا اهواز.',
            'rank_math_focus_keyword': 'راهنمای خرید ماشین لباسشویی, لباسشویی برای آب خوزستان'
        }
    }
    req_rm = urllib.request.Request(
        url_rm,
        data=json.dumps(rm_payload).encode('utf-8'),
        headers={'Authorization': f'Basic {creds}', 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        method='POST'
    )
    urllib.request.urlopen(req_rm, context=ctx, timeout=8)
    print("Rank Math Meta tags configured for the scheduled washing machine post!")
except Exception as e:
    print("Error creating scheduled post:", e)
