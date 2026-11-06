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

posts_to_enhance = [
    {
        'id': 3855,
        'slug': 'bajet-tejarat-refah-300m-appliances',
        'h1': '<h1 style="font-size: 26px; line-height: 1.6; color: #0f172a; margin-bottom: 24px; font-weight: 800;">خرید اقساطی لوازم خانگی با طرح باجت بانک تجارت و کارت رفاهی تا ۳۰۰ میلیون تومان</h1>\n',
        'rec_title': 'لوازم خانگی قابل سفارش با اعتبار باجت تجارت و کارت اعتباری رفاه',
        'rec_text': 'مشتریان گرامی پس از تخصیص اعتبار طرح کالانو باجت تجارت یا کارت رفاهی، می‌توانند اقلام ضروری منزل را از نمایندگی رسمی حسینی کالا تهیه نمایند:'
    },
    {
        'id': 3853,
        'slug': 'refah-bank-beta-installment-guide',
        'h1': '<h1 style="font-size: 26px; line-height: 1.6; color: #0f172a; margin-bottom: 24px; font-weight: 800;">راهنمای کامل طرح بتا بانک رفاه برای خرید اقساطی بازنشستگان تأمین اجتماعی</h1>\n',
        'rec_title': 'لوازم خانگی منتخب طرح بتا بانک رفاه ویژه بازنشستگان تامین اجتماعی',
        'rec_text': 'بازنشستگان و مستمری‌بگیران گرامی می‌توانند بدون نیاز به ضامن و تنها با کسر از حقوق، انواع لوازم خانگی اصلی را از فروشگاه حسینی کالا انتخاب فرمایند:'
    }
]

for p in posts_to_enhance:
    url = f"https://hosseinykala.ir/wp-json/wp/v2/posts/{p['id']}"
    req = urllib.request.Request(url, headers={'Authorization': f'Basic {creds}', 'User-Agent': 'Mozilla/5.0'})
    try:
        post_data = json.loads(urllib.request.urlopen(req, context=ctx, timeout=8).read().decode('utf-8'))
        content = post_data['content']['rendered']
        
        if p['h1'].strip() in content:
            print(f"Post {p['id']} already has H1!")
            continue
            
        rec_box = f'''
<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-right: 4px solid #059669; border-radius: 8px; padding: 20px; margin: 30px 0; direction: rtl;">
<h3 style="color: #1e293b; margin-top: 0; font-size: 19px;">{p['rec_title']}</h3>
<p style="color: #475569; font-size: 15px; line-height: 1.8;">{p['rec_text']}</p>
<ul style="color: #334155; line-height: 2; font-size: 15px; padding-right: 20px;">
<li><strong>یخچال و فریزر:</strong> انواع مدل‌های دوقلو و ساید بای ساید با گارانتی معتبر در صفحه <a href="https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/" style="color: #059669; font-weight: 600;">خرید یخچال فریزر</a>.</li>
<li><strong>ماشین لباسشویی:</strong> مدل‌های اتوماتیک اینورتر با کمترین مصرف انرژی در بخش <a href="https://hosseinykala.ir/product-category/washing-cleaning/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d9%84%d8%a8%d8%a7%d8%b3%d8%b4%d9%88%db%8c%db%8c/" style="color: #059669; font-weight: 600;">ماشین لباسشویی</a>.</li>
<li><strong>تلویزیون و سیستم‌های صوتی:</strong> سایزهای متنوع تلویزیون‌های هوشمند 4K در دسته <a href="https://hosseinykala.ir/product-category/audio-video/television/" style="color: #059669; font-weight: 600;">تلویزیون</a>.</li>
<li><strong>کولر و تهویه مطبوع:</strong> سیستم‌های سرمایشی پرتابل و سلولزی در دسته <a href="https://hosseinykala.ir/product-category/heating-cooling/%da%a9%d9%88%d9%84%d8%b1-%d8%a2%d8%a8%db%8c/" style="color: #059669; font-weight: 600;">کولر آبی</a>.</li>
</ul>
<p style="margin-bottom: 0; font-size: 14px; color: #64748b;">جهت استعلام موجودی روز یا صدور فاکتور اقساطی می‌توانید با کارشناسان <a href="https://hosseinykala.ir/" style="color: #059669; font-weight: bold;">فروشگاه لوازم خانگی حسینی</a> اهواز در ارتباط باشید.</p>
</div>
'''
        new_content = p['h1'] + content + rec_box
        
        req_update = urllib.request.Request(
            url,
            data=json.dumps({'content': new_content}).encode('utf-8'),
            headers={'Authorization': f'Basic {creds}', 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
            method='POST'
        )
        urllib.request.urlopen(req_update, context=ctx, timeout=8)
        print(f"Successfully updated post {p['id']} ({p['slug']}) with H1 and Category Links!")
    except Exception as e:
        print(f"Error updating post {p['id']}: {e}")
