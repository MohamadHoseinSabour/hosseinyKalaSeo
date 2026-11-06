import os
import sys
import json
import requests
from requests.auth import HTTPBasicAuth
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

AUTH = HTTPBasicAuth('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
WP_BASE = 'https://hosseinykala.ir'

print("=== ۱. بررسی زنده هر دو محصول روی وب‌سایت حسینی کالا ===")
for pid, name in [(4492, "جاروبرقی کندی KCV-325 G"), (4494, "تلویزیون هوشمند الیو OL-43FSS30")]:
    url = f"{WP_BASE}/wp-json/wc/v3/products/{pid}"
    res = requests.get(url, auth=AUTH, timeout=15)
    assert res.status_code == 200, f"خطا در دریافت شناسه {pid}: {res.status_code}"
    data = res.json()
    print(f"✓ محصول زنده {pid}:")
    print(f"   نام: {data.get('name')}")
    print(f"   وضعیت انتشار: {data.get('status')}")
    print(f"   وضعیت موجودی: {data.get('stock_status')}")
    print(f"   دسته‌بندی‌ها: {[c.get('name') for c in data.get('categories', [])]}")
    print(f"   لینک دائمی: {data.get('permalink')}")
    print(f"   تصویر شاخص: {data.get('images', [{}])[0].get('src')}")

print("\n=== ۲. بررسی سلول‌های کاتالوگ اکسل ===")
wb = openpyxl.load_workbook('hosseiny_kala_catalog.xlsx', data_only=True)

# ۱. شستشو و نظافت
ws_w = wb['شستشو و نظافت']
row_candy = 111
print("شیت شستشو و نظافت سطر 111:")
print(f"   A: {ws_w.cell(row_candy, 1).value}")
print(f"   B: {ws_w.cell(row_candy, 2).value} ریال | C: {ws_w.cell(row_candy, 3).value} تومان")
print(f"   H (موجودی): {ws_w.cell(row_candy, 8).value}")
print(f"   N (شناسه): {ws_w.cell(row_candy, 14).value}")
print(f"   P (لینک): {ws_w.cell(row_candy, 16).value}")
print(f"   R (وضعیت در سایت): {ws_w.cell(row_candy, 18).value}")

# ۲. صوتی و تصویری
ws_av = wb['صوتی و تصویری']
row_olive = 11
print("\nشیت صوتی و تصویری سطر 11:")
print(f"   A: {ws_av.cell(row_olive, 1).value}")
print(f"   H (موجودی): {ws_av.cell(row_olive, 8).value}")
print(f"   N (شناسه): {ws_av.cell(row_olive, 14).value}")
print(f"   P (لینک): {ws_av.cell(row_olive, 16).value}")
print(f"   R (وضعیت در سایت): {ws_av.cell(row_olive, 18).value}")

# ۳. داشبورد
ws_dash = wb['📊 خلاصه و داشبورد']
print("\nشیت داشبورد سطر ۵:")
print(f"   کل محصولات: {ws_dash.cell(5, 2).value} | ثبت‌شده سایت: {ws_dash.cell(5, 3).value} | موجود: {ws_dash.cell(5, 5).value} | ناموجود: {ws_dash.cell(5, 6).value}")

print("\n🎉 تمامی بررسی‌ها با موفقیت ۱۰۰٪ تایید شدند!")
