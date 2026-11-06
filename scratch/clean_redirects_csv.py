import csv
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/hosseinykala_404_redirects_rankmath.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    rows = list(reader)

print(f"Total rows: {len(rows)}")
for r in rows[:15]:
    print(r)
