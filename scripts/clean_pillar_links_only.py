import requests
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/posts/3851', auth=AUTH, headers=HEADERS)
data = r.json()
content = data.get('content', {}).get('raw') or data.get('content', {}).get('rendered', '')

print(f"Original content length: {len(content)}")

# 1. Replace the 5 card button links with clean non-link informative badges
card_replacements = [
    (
        r'<a href="https://hosseinykala.ir/refah-bank-beta-installment-guide/" style="display: block;background: #0284c7;color: #ffffff;text-decoration: none;padding: 8px 12px;border-radius: 8px;font-weight: bold;font-size: 13px">[^<]+</a>',
        '<div style="display: block;background: #0284c7;color: #ffffff;padding: 8px 12px;border-radius: 8px;font-weight: bold;font-size: 13px">ثبت در سامانه beta.refah-bank.ir</div>'
    ),
    (
        r'<a href="https://hosseinykala.ir/bajet-tejarat-refah-300m-appliances/" style="display: block;background: #4f46e5;color: #ffffff;text-decoration: none;padding: 8px 12px;border-radius: 8px;font-weight: bold;font-size: 13px">[^<]+</a>',
        '<div style="display: block;background: #4f46e5;color: #ffffff;padding: 8px 12px;border-radius: 8px;font-weight: bold;font-size: 13px">اقدام از طریق اپلیکیشن باجت</div>'
    ),
    (
        r'<a href="https://hosseinykala.ir/mellat-bank-200m-appliances-loan-guide/" style="display: block;background: #e11d48;color: #ffffff;text-decoration: none;padding: 8px 12px;border-radius: 8px;font-weight: bold;font-size: 13px">[^<]+</a>',
        '<div style="display: block;background: #e11d48;color: #ffffff;padding: 8px 12px;border-radius: 8px;font-weight: bold;font-size: 13px">استعلام در سامانه فرابانک ملت</div>'
    ),
    (
        r'<a href="https://hosseinykala.ir/sayadi-cheque-installment-buying-guide/" style="display: block;background: #059669;color: #ffffff;text-decoration: none;padding: 8px 12px;border-radius: 8px;font-weight: bold;font-size: 13px">[^<]+</a>',
        '<div style="display: block;background: #059669;color: #ffffff;padding: 8px 12px;border-radius: 8px;font-weight: bold;font-size: 13px">خرید مستقیم در حسینی کالا اهواز</div>'
    ),
    (
        r'<a href="https://hosseinykala.ir/mehr-iran-kalacard-bnpl-appliances-guide/" style="display: block;background: #d97706;color: #ffffff;text-decoration: none;padding: 8px 12px;border-radius: 8px;font-weight: bold;font-size: 13px">[^<]+</a>',
        '<div style="display: block;background: #d97706;color: #ffffff;padding: 8px 12px;border-radius: 8px;font-weight: bold;font-size: 13px">کارمزد قرض‌الحسنه ۴ درصد</div>'
    )
]

for pattern, replacement in card_replacements:
    content = re.sub(pattern, replacement, content)

# 2. Textual article links in paragraphs
# Beta link in step 5:
content = re.sub(
    r'\s*برای اطلاعات تکمیلی به <a href="https://hosseinykala.ir/refah-bank-beta-installment-guide/"[^>]*><strong>[^<]+</strong></a> مراجعه فرمایید\.',
    ' به همراه گارانتی معتبر شرکتی.',
    content
)
content = re.sub(
    r'<a href="https://hosseinykala.ir/refah-bank-beta-installment-guide/"[^>]*><strong>[^<]+</strong></a>',
    'طرح بتای بانک رفاه',
    content
)

# Bajet link in paragraph:
content = re.sub(
    r'\s*جزئیات بیشتر را در <a href="https://hosseinykala.ir/bajet-tejarat-refah-300m-appliances/"[^>]*><strong>[^<]+</strong></a> بخوانید\.',
    '',
    content
)
content = re.sub(
    r'<a href="https://hosseinykala.ir/bajet-tejarat-refah-300m-appliances/"[^>]*><strong>[^<]+</strong></a>',
    'طرح باجت و کالانو',
    content
)

# Mellat link in paragraph:
content = re.sub(
    r'\s*برای جزئیات مدارک و نحوه صدور پیش‌فاکتور به <a href="https://hosseinykala.ir/mellat-bank-200m-appliances-loan-guide/"[^>]*><strong>[^<]+</strong></a> مراجعه فرمایید\.',
    ' پیش‌فاکتور رسمی مورد تایید بانک توسط کارشناسان حسینی کالا صادر می‌گردد.',
    content
)
content = re.sub(
    r'<a href="https://hosseinykala.ir/mellat-bank-200m-appliances-loan-guide/"[^>]*><strong>[^<]+</strong></a>',
    'تسهیلات خرید کالا بانک ملت',
    content
)

# Sayadi cheque link in paragraph:
content = re.sub(
    r'\s*راهنمای کامل را در <a href="https://hosseinykala.ir/sayadi-cheque-installment-buying-guide/"[^>]*><strong>[^<]+</strong></a> بخوانید\.',
    '',
    content
)
content = re.sub(
    r'<a href="https://hosseinykala.ir/sayadi-cheque-installment-buying-guide/"[^>]*><strong>[^<]+</strong></a>',
    'خرید اقساطی با چک صیادی',
    content
)

# Mehr Iran / BNPL link in paragraph:
content = re.sub(
    r'\s*برای مطالعه مقایسه جامع این دو روش به <a href="https://hosseinykala.ir/mehr-iran-kalacard-bnpl-appliances-guide/"[^>]*><strong>[^<]+</strong></a> مراجعه فرمایید\.',
    '',
    content
)
content = re.sub(
    r'<a href="https://hosseinykala.ir/mehr-iran-kalacard-bnpl-appliances-guide/"[^>]*><strong>[^<]+</strong></a>',
    'تسهیلات کالا کارت و سامانه‌های پرداخت اعتباری',
    content
)

# 3. Product links: Unlink products so only strong text remains
# Clover fridge 54ft:
content = re.sub(
    r'<a href="https://hosseinykala.ir/product/%db%8c%d8%ae%da%86%d8%a7%d9%84-[^"]+"[^>]*><strong>(یخچال فریزر دوقلو ۵۴ فوت کلور گلوری پلاس)</strong></a>',
    r'<strong>\1</strong>',
    content
)
# Depoint Max DU:
content = re.sub(
    r'<a href="https://hosseinykala.ir/product/depoint-max-du-twin-refrigerator-34ft/"[^>]*><strong>(یخچال دوقلو ۳۴ فوت دیپوینت MAX DU)</strong></a>',
    r'<strong>\1</strong>',
    content
)
# Clover dishwasher:
content = re.sub(
    r'<a href="https://hosseinykala.ir/product/clover-cdw-h15v-dishwasher-15p/"[^>]*><strong>(ظرفشویی کلور CDW-H15V)</strong></a>',
    r'<strong>\1</strong>',
    content
)
# Soft water purifier:
content = re.sub(
    r'<a href="https://hosseinykala.ir/product/soft-water-ir-06-purifier/"[^>]*><strong>(سافت واتر IR-06)</strong></a>',
    r'<strong>\1</strong>',
    content
)

# Also any general fallback for any remaining product links:
content = re.sub(
    r'<a href="https://hosseinykala.ir/product/[^"]+"[^>]*>(.*?)</a>',
    r'\1',
    content
)

# Check remaining links
remaining = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', content, re.DOTALL)
print(f"\nRemaining links in updated Post 3851: {len(remaining)}")
for href, anchor in remaining:
    clean_anchor = re.sub(r'<[^>]+>', '', anchor).strip()
    print(f"  [{href}]  ===>  '{clean_anchor}'")

# Push update to WordPress
update_url = 'https://hosseinykala.ir/wp-json/wp/v2/posts/3851'
payload = {'content': content}
up_res = requests.post(update_url, auth=AUTH, headers=HEADERS, json=payload, timeout=30)
if up_res.status_code == 200:
    print("\n✅ [SUCCESS] Post 3851 updated successfully on WordPress!")
else:
    print(f"\n❌ [FAIL] Post 3851: HTTP {up_res.status_code} - {up_res.text[:200]}")
