import sys
import time
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

content_sub5 = """<p>تحولات فناوری‌های مالی و پیدایش شیوه‌های نوین اعتباری نظیر لندتک‌ها و سامانه‌های BNPL (الان بخر، بعداً پرداخت کن)، ساختار سنتی خریدهای اقساطی را دگرگون کرده است. از سوی دیگر، تسهیلات بانکی با نرخ‌های کارمزد قرض‌الحسنه همچنان برای خریدهای درشت پرطرفدارترین گزینه‌اند. در این میان دو قطب اصلی شامل <strong>کالا کارت بانک مهر ایران</strong> و <strong>پلتفرم‌های BNPL (مانند اسنپ‌پی و دیجی‌پی)</strong> پیش روی خریداران است. در این تحلیل از <a href="https://hosseinykala.ir/" target="_blank" rel="noopener"><strong>فروشگاه لوازم خانگی حسینی</strong></a>، این دو مدل را در ترازوی مقایسه می‌گذاریم تا بدانید کدام گزینه با هدف خرید شما سازگارتر است.</p>

<p>برای بررسی نقشه کلان تمام روش‌های اقساطی، به <a href="https://hosseinykala.ir/home-appliances-installment-buying-guide/" target="_blank" rel="noopener"><strong>راهنمای جامع خرید اقساطی لوازم خانگی</strong></a> مراجعه فرمایید.</p>

<h2>کالا کارت بانک مهر ایران؛ پادشاه کارمزدهای ارزان</h2>
<p>بانک قرض‌الحسنه مهر ایران با طرح «کالا کارت»، یک کارت اعتباری تا سقف ۱۵۰ الی ۳۰۰ میلیون تومان با نرخ کارمزد باورنکردنی <strong>تنها ۴ درصد سالانه</strong> در اختیار خریداران قرار می‌دهد. این طرح فاقد سودهای سنگین بانکی است و مبالغ در اقساط ۶، ۹، ۱۲، ۱۸ یا ۲۴ ماهه بازپرداخت می‌شوند.</p>

<div style="background: #fffbeb; border-right: 5px solid #d97706; border-radius: 8px; padding: 18px; margin: 20px 0; direction: rtl;">
  <h4 style="color: #92400e; margin-top: 0;">نکات برجسته کالا کارت مهر ایران:</h4>
  <ul style="margin-bottom: 0; color: #78350f; line-height: 1.85;">
    <li><strong>نرخ کارمزد ۴ درصد:</strong> ارزان‌ترین شکل استقراض رسمی در سیستم پولی ایران.</li>
    <li><strong>بدون مسدودی سپرده:</strong> نیازی به بلوکه شدن پول در حساب بانکی ندارید.</li>
    <li><strong>شروع اقساط:</strong> اولین قسط یک ماه پس از واریز یا دریافت کالا آغاز می‌شود.</li>
    <li><strong>ضمانت:</strong> نیازمند ارائه یک ضامن معتبر کارمند با فیش حقوقی به شعبه است.</li>
  </ul>
</div>

<h2>روش‌های BNPL (اسنپ‌پی و دیجی‌پی)؛ سرعت بالا برای خریدهای سبک</h2>
<p>در نقطه مقابل، پلتفرم‌های لندتک با حذف کامل ضامن و سفته فیزیکی، امکان خریدهای خرد و سریع را فراهم ساخته‌اند:</p>

<h3>۱. اسنپ‌پی (SnappPay):</h3>
<p>طرح پرداخت ۴ ماهه اسنپ‌پی بدون دریافت یک ریال سود یا کارمزد کار می‌کند. هزینه کالا به ۴ بخش مساوی تقسیم شده و بخش اول در همان لحظه و ۳ بخش دیگر در پایان هر ماه پرداخت می‌شود. این سیستم برای وسایل خانگی با قیمت‌های خرد نظیر <a href="https://hosseinykala.ir/product-category/%d8%ac%d8%a7%d8%b1%d9%88%d8%a8%d8%b1%d9%82%db%8c/" target="_blank" rel="noopener"><strong>جاروبرقی</strong></a>، اتو بخار، سرخ‌کن بدون روغن یا غذاساز بی‌نظیر است.</p>

<h3>۲. دیجی‌پی و لندو:</h3>
<p>این پلتفرم‌ها برای مبالغ تا سقف ۲۰ الی ۵۰ میلیون تومان، با بهره‌گیری از سفته الکترونیک و اعتبارسنجی آنلاین بانکی، اعتبار خرید کالا را بدون نیاز به حضور در شعب سنتی فراهم می‌آورند.</p>

<h2>جدول مقایسه رودررو: کالا کارت در برابر سامانه‌های BNPL</h2>
<div style="overflow-x: auto; margin: 20px 0;">
<table style="width: 100%; border-collapse: collapse; text-align: right; min-width: 600px; font-size: 14px;">
  <thead>
    <tr style="background-color: #1e293b; color: #ffffff;">
      <th style="padding: 10px 12px; border: 1px solid #334155;">شاخص مقایسه</th>
      <th style="padding: 10px 12px; border: 1px solid #334155;">کالا کارت مهر ایران</th>
      <th style="padding: 10px 12px; border: 1px solid #334155;">اسنپ‌پی (BNPL)</th>
      <th style="padding: 10px 12px; border: 1px solid #334155;">دیجی‌پی / لندو</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background-color: #f8fafc;">
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0; font-weight: bold;">سقف اعتبار</td>
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0; color: #16a34a; font-weight: bold;">تا ۳۰۰ میلیون تومان</td>
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0;">تا ۱۰ الی ۱۵ میلیون تومان</td>
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0;">تا ۵۰ میلیون تومان</td>
    </tr>
    <tr>
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0; font-weight: bold;">کارمزد و سود</td>
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0;">۴٪ سالیانه (قرض‌الحسنه)</td>
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0; color: #16a34a; font-weight: bold;">۰٪ (بدون کارمزد)</td>
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0;">مصوب + کارمزد خدمات پلتفرم</td>
    </tr>
    <tr style="background-color: #f8fafc;">
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0; font-weight: bold;">مدت بازپرداخت</td>
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0;">تا ۲۴ ماه</td>
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0;">۴ ماهه</td>
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0;">۱۲ تا ۲۴ ماه</td>
    </tr>
    <tr>
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0; font-weight: bold;">نوع ضمانت</td>
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0;">ضامن رسمی معتبر</td>
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0; color: #16a34a; font-weight: bold;">بدون ضامن و سفته</td>
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0;">سفته الکترونیک</td>
    </tr>
    <tr style="background-color: #f8fafc;">
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0; font-weight: bold;">سرعت صدور</td>
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0;">۷ الی ۱۰ روز کاری</td>
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0; color: #16a34a; font-weight: bold;">آنی و در لحظه</td>
      <td style="padding: 10px 12px; border: 1px solid #e2e8f0;">۲ الی ۳ روز کاری</td>
    </tr>
  </tbody>
</table>
</div>

<h2>نتیجه‌گیری نهایی: کدام شیوه برای خرید شما بهتر است؟</h2>
<ul>
  <li><strong>برای جهیزیه کامل و لوازم سنگین:</strong> اگر قصد خرید یخچال فریزر دوقلو، لباسشویی اتوماتیک یا کولر سلولزی را دارید، قطعا <strong>کالا کارت مهر ایران</strong> به دلیل سقف بالا و سود ناچیز ۴ درصدی انتخابی بی‌همتاست.</li>
  <li><strong>برای خرده‌ریز آشپزخانه و ارتقای وسایل کوچک:</strong> برای تهیه سرخ‌کن، اسپرسوساز، اتو یا غذاساز، <strong>اسنپ‌پی</strong> بدون درگیر کردن ضامن، خرید شما را در ۴ قسط بدون سود ممکن می‌سازد.</li>
</ul>

<h2>مشاوره انتخاب در فروشگاه لوازم خانگی حسینی</h2>
<p>کارشناسان ما در شعب <a href="https://hosseinykala.ir/" target="_blank" rel="noopener"><strong>فروشگاه لوازم خانگی حسینی</strong></a> در بازار <strong>اهواز</strong> آماده‌اند تا بر اساس بودجه، نوع کالا و مدارک ضمانتی که در اختیار دارید، دقیق‌ترین و به‌صرفه‌ترین مسیر خرید اقساطی را به شما پیشنهاد دهند.</p>"""

payload = {
    'title': 'مقایسه کالا کارت قرض‌الحسنه مهر ایران و روش‌های خرید اقساطی BNPL اسنپ‌پی و دیجی‌پی',
    'slug': 'mehr-iran-kalacard-bnpl-appliances-guide',
    'status': 'future',
    'date': '2026-10-01T19:30:00',
    'categories': [54],
    'featured_media': 3850,
    'excerpt': 'مقایسه موشکافانه کالا کارت ۴ درصدی بانک قرض‌الحسنه مهر ایران و پلتفرم‌های لندتک BNPL نظیر اسنپ‌پی و دیجی‌پی برای خرید لوازم خانگی برقی و تجهیزات آشپزخانه.',
    'content': content_sub5
}

for attempt in range(3):
    try:
        print(f"Attempt {attempt+1} posting Sub-Article 5...", flush=True)
        r = requests.post("https://hosseinykala.ir/wp-json/wp/v2/posts", headers=HEADERS, auth=AUTH, json=payload, timeout=30)
        if r.status_code in [200, 201]:
            data = r.json()
            pid = data.get('id')
            print(f"[SUCCESS] Sub-article 5 scheduled! ID: {pid} | Date: {data.get('date')} | Link: {data.get('link')}", flush=True)

            meta_payload = {
                'meta': {
                    'rank_math_title': 'کالا کارت مهر ایران در برابر اسنپ‌پی و دیجی‌پی؛ مقایسه روش‌ها | حسینی کالا',
                    'rank_math_description': 'مقایسه جامع کالا کارت ۴ درصدی بانک مهر ایران با شیوه‌های BNPL اسنپ‌پی و دیجی‌پی برای خرید اقساطی لوازم خانگی؛ کارمزد، سقف اعتبار و سرعت دریافت.',
                    'rank_math_focus_keyword': 'کالا کارت مهر ایران'
                }
            }
            r_meta = requests.post(f"https://hosseinykala.ir/wp-json/wp/v2/posts/{pid}", headers=HEADERS, auth=AUTH, json=meta_payload, timeout=20)
            print(f"Meta update: {r_meta.status_code}", flush=True)
            break
        else:
            print(f"HTTP {r.status_code}: {r.text[:200]}", flush=True)
    except Exception as e:
        print(f"Exception: {e}", flush=True)
        time.sleep(3)
