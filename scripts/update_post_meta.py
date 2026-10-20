import requests

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

post_id = 3851
payload = {
    'meta': {
        'rank_math_title': 'خرید اقساطی لوازم خانگی؛ معرفی طرح بتا، باجت، بانک ملت و چک صیادی | حسینی کالا',
        'rank_math_description': 'راهنمای جامع خرید اقساطی لوازم خانگی در سال ۱۴۰۵. بررسی شرایط طرح بتای بانک رفاه برای بازنشستگان، طرح باجت تا ۳۰۰ میلیون، وام بانک ملت و خرید با چک صیادی در اهواز.',
        'rank_math_focus_keyword': 'خرید اقساطی لوازم خانگی'
    }
}

r = requests.post(f'https://hosseinykala.ir/wp-json/wp/v2/posts/{post_id}', auth=AUTH, headers=HEADERS, json=payload, timeout=20)
print(f"Meta update HTTP {r.status_code}")
if r.status_code == 200:
    print("Meta updated successfully!")
else:
    print(r.text[:200])
