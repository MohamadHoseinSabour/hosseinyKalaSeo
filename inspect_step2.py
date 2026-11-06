import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

soup = BeautifulSoup(open('wizard_step2.html', encoding='utf-8'), 'html.parser')

step_row = soup.find('div', class_=lambda c: c and 'step-indicator' in c)
print('Step indicator:', step_row.get_text(strip=True) if step_row else 'None')

print('\n=== ALL INPUTS ON STEP 2 ===')
for inp in soup.find_all('input'):
    t = inp.get('type')
    n = inp.get('name')
    ph = inp.get('placeholder')
    print(f'Input: type={t}, name={n}, ph={ph}')

print('\n=== TEXTAREAS ===')
for t in soup.find_all('textarea'):
    n = t.get('name')
    ph = t.get('placeholder')
    print(f'Textarea: name={n}, ph={ph}')

print('\n=== BUTTONS / CLICKABLE ITEMS ===')
for b in soup.find_all(['button', 'div']):
    txt = b.get_text(strip=True)
    if any(k in txt for k in ['فروشگاه', 'خانه کلور', 'حسینی', 'دسته', 'انتخاب', 'بعدی', 'تایید']):
        if len(txt) < 80:
            print(f'Tag: {b.name}, Text: {txt}')

print('\n=== LABELS & HEADINGS ===')
for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'label', 'p', 'span']):
    txt = tag.get_text(strip=True)
    if any(k in txt for k in ['دسته', 'فروشگاه', 'کسب', 'قیمت', 'توضیحات', 'وضعیت', 'برند', 'مدل', 'نوع']):
        if len(txt) < 80:
            print(' -', txt)
