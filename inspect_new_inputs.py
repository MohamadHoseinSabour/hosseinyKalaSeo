import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

soup = BeautifulSoup(open('current_new.html', encoding='utf-8'), 'html.parser')

print("=== ALL INPUTS ===")
for inp in soup.find_all('input'):
    print(f"Tag: {inp.name}, type={inp.get('type')}, name={inp.get('name')}, id={inp.get('id')}, class={inp.get('class')}, placeholder={inp.get('placeholder')}")

print("\n=== ALL BUTTONS ===")
for b in soup.find_all(['button', 'div', 'a']):
    txt = b.get_text(strip=True)
    if any(k in txt for k in ['عنوان', 'عکس', 'بعدی', 'متوجه', 'فروشگاه', 'پاک کردن', 'انتخاب']):
        if len(txt) < 50:
            print(f"Tag: {b.name}, class={b.get('class')}, id={b.get('id')} -> Text: '{txt}'")
