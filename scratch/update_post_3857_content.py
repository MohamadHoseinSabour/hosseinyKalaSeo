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

# 1. Fetch current post 3857
url = 'https://hosseinykala.ir/wp-json/wp/v2/posts/3857'
req = urllib.request.Request(url, headers={'Authorization': f'Basic {creds}', 'User-Agent': 'Mozilla/5.0'})
post = json.loads(urllib.request.urlopen(req, context=ctx, timeout=8).read().decode('utf-8'))
current_content = post['content']['raw'] if 'raw' in post['content'] else post['content']['rendered']

# Check if H1 or FAQ schema already exists
if '<script type="application/ld+json">' in current_content and 'FAQPage' in current_content:
    print("FAQ Schema already present in content!")
else:
    # 2. Prepare H1 banner
    h1_banner = '''<h1 style="font-size: 26px; line-height: 1.6; color: #0f172a; margin-bottom: 24px; font-weight: 800;">راهنمای دریافت وام ۲۰۰ میلیونی خرید لوازم خانگی بانک ملت؛ فرابانک و حامی کارت</h1>
'''
    
    # 3. Prepare Internal Links & Product Recommendation Box
    rec_box = '''
<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-right: 4px solid #2563eb; border-radius: 8px; padding: 20px; margin: 30px 0; direction: rtl;">
<h3 style="color: #1e293b; margin-top: 0; font-size: 19px;">کالاهای پیشنهادی برای خرید با پیش‌فاکتور وام ۲۰۰ میلیونی بانک ملت</h3>
<p style="color: #475569; font-size: 15px; line-height: 1.8;">پس از تایید اعتبار و صدور پیش‌فاکتور رسمی در <a href="https://hosseinykala.ir/" style="color: #2563eb; text-decoration: underline; font-weight: bold;">فروشگاه لوازم خانگی حسینی</a> اهواز، می‌توانید از بین برترین برندهای بازار با گارانتی اصلی انتخاب نمایید:</p>
<ul style="color: #334155; line-height: 2; font-size: 15px; padding-right: 20px;">
<li><strong>یخچال و فریزر:</strong> مشاهده و انتخاب انواع مدل‌های دوقلو، ساید و کمبی در صفحه <a href="https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/" style="color: #2563eb; font-weight: 600;">خرید یخچال فریزر</a> با بهترین قیمت.</li>
<li><strong>ماشین لباسشویی:</strong> انواع مدل‌های ۸ و ۹ کیلویی اینورتر را در دسته <a href="https://hosseinykala.ir/product-category/washing-cleaning/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d9%84%d8%a8%d8%a7%d8%b3%d8%b4%d9%88%db%8c%db%8c/" style="color: #2563eb; font-weight: 600;">ماشین لباسشویی</a> بررسی کنید.</li>
<li><strong>تلویزیون هوشمند:</strong> سایزهای ۵۰ تا ۷۵ اینچ 4K برندهای معتبر در صفحه <a href="https://hosseinykala.ir/product-category/audio-video/television/" style="color: #2563eb; font-weight: 600;">تلویزیون هوشمند</a>.</li>
<li><strong>ماشین ظرفشویی:</strong> مدل‌های ۱۵ و ۱۶ نفره مبله در بخش <a href="https://hosseinykala.ir/product-category/washing-cleaning/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d8%b8%d8%b1%d9%81%d8%b4%d9%88%db%8c%db%8c/" style="color: #2563eb; font-weight: 600;">ماشین ظرفشویی</a> با گارانتی رسمی.</li>
</ul>
</div>
'''

    # 4. Prepare JSON-LD FAQ Schema
    faq_schema = '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "شرایط دریافت وام ۲۰۰ میلیونی خرید لوازم خانگی بانک ملت چیست؟",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "متقاضیان باید دارای رتبه اعتباری مناسب در سامانه اعتبارسنجی بانکی باشند و از طریق سامانه فرابانک ملت یا مراجعه به شعب و ارائه پیش‌فاکتور رسمی از فروشگاه‌های معتبر اقدام نمایند."
      }
    },
    {
      "@type": "Question",
      "name": "آیا برای دریافت وام بانک ملت نیاز به پیش‌فاکتور رسمی است؟",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "بله؛ ارائه پیش‌فاکتور رسمی دارای شناسه معتبر صنفی از فروشگاه‌های طرف قرارداد مانند فروشگاه لوازم خانگی حسینی الزامی است تا مبلغ وام در قالب کارت اعتباری یا حامی کارت شارژ شود."
      }
    },
    {
      "@type": "Question",
      "name": "مدت بازپرداخت و سود وام خرید کالای بانک ملت چقدر است؟",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "مدت بازپرداخت این تسهیلات تا سقف ۶۰ ماه (۵ سال) با نرخ مصوب شورای پول و اعتبار بوده و اقساط آن به صورت ماهانه کسر یا واریز می‌گردد."
      }
    },
    {
      "@type": "Question",
      "name": "چگونه می‌توان با حامی کارت ملت از حسینی کالا خرید کرد؟",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "پس از دریافت اعتبار حامی کارت از بانک ملت، خریداران محترم می‌توانند به صورت حضوری در شعب اهواز یا از طریق درگاه‌های پشتیبانی حسینی کالا، سفارش خود را نهایی کنند."
      }
    }
  ]
}
</script>
'''

    new_content = h1_banner + current_content + rec_box + faq_schema

    update_payload = {
        'content': new_content
    }

    req_update = urllib.request.Request(
        url,
        data=json.dumps(update_payload).encode('utf-8'),
        headers={
            'Authorization': f'Basic {creds}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        },
        method='POST'
    )

    try:
        resp_update = urllib.request.urlopen(req_update, context=ctx, timeout=10)
        print("Successfully updated post 3857 content with H1, Category Links, and FAQ Schema!")
    except Exception as e:
        print(f"Error updating post 3857 content: {e}")
