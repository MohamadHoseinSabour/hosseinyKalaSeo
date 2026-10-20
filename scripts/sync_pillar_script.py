import re

with open('scripts/update_pillar_super_detailed.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace card button links
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

# Remove article links from text
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

# Product links
content = re.sub(
    r'<a href="https://hosseinykala.ir/product/[^"]+"[^>]*>(.*?)</a>',
    r'\1',
    content
)

with open('scripts/update_pillar_super_detailed.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated scripts/update_pillar_super_detailed.py")
