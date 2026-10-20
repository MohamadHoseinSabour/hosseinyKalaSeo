import requests
from requests.auth import HTTPBasicAuth
import json

auth = HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

# New title, slug, content
new_title = "ماشین ظرفشویی ۱۶ نفره کلور مدل لمسی استیل ۳ سبد"
new_slug = "clover-16-person-touch-inox-dishwasher"
new_categories = [97, 159]  # 97: ماشین ظرفشویی, 159: ماشین ظرفشویی کلور

new_excerpt = """<ul>
<li><strong>گنجایش فوق‌العاده ۱۶ نفره:</strong> طراحی جادار ۳ سبد آسانسوردار مجزا مناسب مهمانی‌ها و خانواده‌های پرجمعیت با سبد اختصاصی قاشق و چنگال.</li>
<li><strong>پنل لمسی دیجیتال پیشرفته:</strong> مجهز به نمایشگر مدرن LED مخفی و کلیدهای تمام لمسی با کاربری بسیار آسان.</li>
<li><strong>موتور کم‌مصرف و بی‌صدا:</strong> عملکرد فوق‌العاده سایلنت ۴۴ دسی‌بل با رده انرژی بهینه و مصرف آب تنها ۹.۵ لیتر در هر سیکل.</li>
<li><strong>برنامه‌های شستشوی متنوع:</strong> دارای ۸ برنامه اصلی شامل شستشوی سریع، اقتصادی (Eco)، ظروف کریستال و توربو پرقدرت به همراه سیستم خشک‌کن توربو.</li>
<li><strong>بدنه تمام استیل ضدلک و ضدزنگ:</strong> مقاوم در برابر خط‌وخش و رطوبت با ضمانت رسمی در فروشگاه لوازم خانگی حسینی اهواز.</li>
</ul>"""

new_content = """<p>اگر به دنبال انتخابی هوشمندانه، بادوام و باکیفیت در میان لوازم خانگی مدرن هستید، <strong>ماشین ظرفشویی ۱۶ نفره کلور مدل لمسی استیل ۳ سبد</strong> از برند نام‌آشنا و معتبر <strong>کلور (Clover)</strong> پاسخی شایسته و مطمئن به نیازهای شستشوی ظروف شماست. این ظرفشویی با بهره‌گیری از آخرین تکنولوژی‌های روز دنیا، مصرف بهینه انرژی و آب، و طراحی چشم‌نواز بدنه استیل، خیال شما را پس از مهمانی‌های بزرگ آسوده می‌کند. شما می‌توانید این کالا را با ضمانت اصالت و سلامت فیزیکی از <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> تهیه فرموده یا جهت بررسی و خرید حضوری به شعب ما در <strong>اهواز</strong> مراجعه نمایید.</p>

<h2>کیفیت ساخت بالا، موتور سایلنت و طراحی مدرن کلور</h2>
<p>طراحی ارگونومیک و مهندسی‌شده ماشین ظرفشویی ۱۶ نفره کلور، بالاترین سطح راحتی، ایمنی و بهره‌وری را فراهم می‌آورد. استفاده از متریال مرغوب تمام استیل ضدلک در ساختار بدنه و محفظه داخلی، مقاومت دستگاه را در برابر رسوب و زنگ‌زدگی به حداکثر رسانده است. عایق‌بندی صوتی پیشرفته، صدای کارکرد دستگاه را به ۴۴ دسی‌بل کاهش داده تا در آرامش کامل و بدون ایجاد لرزش به نظافت دقیق ظروف بپردازد.</p>

<h2>جدول مشخصات فنی ماشین ظرفشویی ۱۶ نفره کلور مدل لمسی استیل</h2>
<table class="table table-striped table-bordered" style="width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 20px;">
<tbody>
<tr>
<th style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa; width: 35%;">برند سازنده</th>
<td style="padding: 10px; border: 1px solid #ddd;">کلور (Clover)</td>
</tr>
<tr>
<th style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;">مدل دستگاه</th>
<td style="padding: 10px; border: 1px solid #ddd;">۱۶ نفره لمسی ۳ سبد (Touch Inox 16-Person)</td>
</tr>
<tr>
<th style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;">دسته‌بندی</th>
<td style="padding: 10px; border: 1px solid #ddd;"><a href="https://hosseinykala.ir/product-category/washing-cleaning/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d8%b8%d8%b1%d9%81%d8%b4%d9%88%db%8c%db%8c/clover-dishwashers/">ماشین ظرفشویی کلور</a></td>
</tr>
<tr>
<th style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;">ظرفیت شستشو</th>
<td style="padding: 10px; border: 1px solid #ddd;">۱۶ نفره جادار (مناسب خانواده‌های پرجمعیت)</td>
</tr>
<tr>
<th style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;">تعداد سبد</th>
<td style="padding: 10px; border: 1px solid #ddd;">۳ سبد آسانسوردار با قابلیت تنظیم ارتفاع و سبد اختصاصی کارد و چنگال</td>
</tr>
<tr>
<th style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;">جنس و رنگ بدنه</th>
<td style="padding: 10px; border: 1px solid #ddd;">استیل ضدلک و ضدزنگ مقاوم (Inox)</td>
</tr>
<tr>
<th style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;">نوع پنل کنترل</th>
<td style="padding: 10px; border: 1px solid #ddd;">پنل دیجیتال تمام لمسی مخفی (Full Touch) با نمایشگر مدرن</td>
</tr>
<tr>
<th style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;">تعداد برنامه‌های شستشو</th>
<td style="padding: 10px; border: 1px solid #ddd;">۸ برنامه شستشوی هوشمند + برنامه‌های کمکی و تاخیر زمانی</td>
</tr>
<tr>
<th style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;">میزان مصرف آب در سیکل</th>
<td style="padding: 10px; border: 1px solid #ddd;">حدود ۹.۵ لیتر (فوق کم‌مصرف)</td>
</tr>
<tr>
<th style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;">سطح صدا</th>
<td style="padding: 10px; border: 1px solid #ddd;">سوپرسایلنت ۴۴ دسی‌بل</td>
</tr>
<tr>
<th style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;">اصالت و گارانتی</th>
<td style="padding: 10px; border: 1px solid #ddd;">ضمانت اصالت و سلامت فیزیکی حسینی کالا</td>
</tr>
</tbody>
</table>

<h2>مزایا و امکانات کلیدی ماشین ظرفشویی ۱۶ نفره کلور</h2>
<ul>
<li><strong>سبدهای آسانسوردار انعطاف‌پذیر:</strong> امکان چیدمان آسان انواع قابلمه‌ها، دیس‌ها و ظروف بزرگ با تغییر ارتفاع سبد میانی.</li>
<li><strong>ضدعفونی بهداشتی ظروف:</strong> استفاده از آب داغ در مراحل شستشو جهت پاک‌سازی کامل چربی‌ها و باکتری‌ها.</li>
<li><strong>خشک‌کن توربو قدرتمند:</strong> خارج کردن کامل رطوبت و جلوگیری از ایجاد لکه‌های آب روی ظروف بلور و پیرکس.</li>
<li><strong>سیستم ایمنی ضد نشت آب (AquaStop):</strong> قطع فوری جریان آب در صورت بروز هرگونه نشتی جهت حفظ ایمنی منزل.</li>
</ul>

<h2>خرید و قیمت ماشین ظرفشویی ۱۶ نفره کلور از حسینی کالا اهواز</h2>
<p><strong>ماشین ظرفشویی ۱۶ نفره کلور مدل لمسی استیل ۳ سبد</strong> ترکیبی بی‌نظیر از تکنولوژی پیشرفته، دوام قطعات و ارزش خرید بالا است. اگر قصد مقایسه و خرید ظرفشویی‌های باکیفیت بازار را دارید، کارشناسان ما در <a href="https://hosseinykala.ir/">فروشگاه لوازم خانگی حسینی</a> آماده ارائه مشاوره تخصصی و ثبت سفارش شما با بهترین قیمت و ارسال سریع هستند.</p>"""

payload = {
    'title': new_title,
    'slug': new_slug,
    'categories': new_categories,
    'excerpt': new_excerpt,
    'content': new_content
}

resp = requests.post(
    'https://hosseinykala.ir/wp-json/wp/v2/product/3546',
    auth=auth,
    headers=headers,
    data=json.dumps(payload),
    timeout=30
)

print("Update Status Code:", resp.status_code)
if resp.status_code in [200, 201]:
    res = resp.json()
    print("Success! Updated product:")
    print("ID:", res.get('id'))
    print("Title:", res.get('title', {}).get('raw') or res.get('title', {}).get('rendered'))
    print("Slug:", res.get('slug'))
    print("Categories:", res.get('categories') or res.get('product_cat'))
    print("Link:", res.get('link'))
else:
    print("Error:", resp.text)
