import json

with open('data/id_mappings.json', 'r', encoding='utf-8') as f:
    id_map = json.load(f)

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

prod_by_id = {p['id']: p for p in products}

items_to_check = [
    # Dishwasher
    3546,
    # Fridges under motafareghe
    "فریزر صندوقی الکتروسان",
    "یخچال و فریزر دوقلو 36 فوت",
    "یخچال و فریزر 27 فوت کلو",
    # Laundry under motafareghe
    3709,
    # Cooking under motafareghe
    "کتری و قوری روگازی هرمی",
    "سرخ‌کن بدون روغن ۸ لیتری گرنویک",
    "آون توستر ۶۰ لیتری کانوکشن",
    "سرویس پخت و پز 10 پارچه مدل دستی لوکس",
    "سبزی خردکن KENRA",
    "سرویس قابلمه استیل 10 پارچه",
    # Beverage under motafareghe
    "سماور برقی پیرکس ۳.۲ لیتری گرنویک",
    "اسپرسوساز ۲۰ بار گرنویک",
    "چای‌ساز تمام استیل کورکماز",
    "کتری برقی ۱.۸ لیتری وگاتی",
    "کتری برقی رترو ۱.۷ لیتری زامروتی",
    "سماور برقی ۳ لیتری دیجیتال پیرکس زامروتی",
    "مخلوط‌کن رترو ۱.۵ لیتری ۶۰۰ وات زامروتی",
    "کتری برقی استیل ۲۰۰۰ وات اریکسون"
]

for query in items_to_check:
    if isinstance(query, int):
        p = prod_by_id.get(query)
        if p:
            print(f"ID {p['id']}: Name='{p.get('name')}', Slug='{p.get('slug')}', Cats={p.get('categories')}")
    else:
        found = False
        for p in products:
            if query in p.get('name', ''):
                print(f"ID {p['id']}: Name='{p.get('name')}', Slug='{p.get('slug')}', Cats={p.get('categories')}")
                found = True
        if not found:
            print(f"NOT FOUND on site: '{query}'")
