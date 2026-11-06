import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\mmhhs\Downloads\rp_cu_5.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

rows = soup.find_all('tr')
# In rp_cu_5.html, let's see how rows pair:
# e.g., row index, description, qty
table_data = []
for tr in rows:
    tds = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
    if tds:
        table_data.append(tds[0])

# Let's inspect the items and their quantities:
# Headers: شرح, تعداد
# Then pairs of: row number, product title, qty
# Let's parse the structured records from table_data:
records = []
i = 0
while i < len(table_data):
    val = table_data[i]
    if val.isdigit() and i + 2 < len(table_data):
        row_num = val
        title = table_data[i+1]
        qty_str = table_data[i+2]
        if qty_str.isdigit():
            records.append({'row_num': row_num, 'title': title, 'qty': int(qty_str)})
            i += 3
            continue
    i += 1

print(f"Total structured records parsed: {len(records)}")

tv_records = []
for r in records:
    t = r['title']
    if any(k in t.lower() for k in ['led', 'ال ای دی', 'toshiba', 'توشیبا', 'x.visjon', 'xvision', 'ایکس', 'هایسنس', 'hisense', 'دوو', 'aversen', 'هاورسون', 'هاورسن', 'اینچ', 'اینج', 'tv']):
        tv_records.append(r)

print(f"\nAll TV items in rp_cu_5.html ({len(tv_records)} items):")
for r in tv_records:
    print(f"  ردیف فاکتور {r['row_num']}: «{r['title']}» | تعداد: {r['qty']}")
