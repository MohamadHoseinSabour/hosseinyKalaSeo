import sys
import io
import json
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('scratch/perfect_audit_summary.json', 'r', encoding='utf-8') as f:
    audit_data = json.load(f)

new_products = audit_data['new_products']
print(f"Total new products: {len(new_products)}")

# Also let's inspect the html table to see if there are prices, barcodes, units, or other fields for these 44 items
with open(r'c:\Users\mmhhs\Downloads\rp_cu_5.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

table = soup.find('table')
rows = table.find_all('tr')
headers = [th.get_text(strip=True) for th in rows[0].find_all(['th', 'td'])]
print("HTML Table Headers:", headers)

for p in new_products:
    idx = p['index']
    # The index in perfect_audit_summary corresponds to the row index
    # Let's find the exact row in html
    row = rows[idx] # let's check
    tds = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
    p['html_row'] = tds
    print(f"Idx {idx}: {p['raw_title']} -> Brand: {p['brand']}, Cat: {p['category']}, Qty: {p['qty']}, Full row: {tds}")
