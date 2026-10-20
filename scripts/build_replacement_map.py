import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/categories.json', encoding='utf-8') as f:
    cats = json.load(f)

cat_map = {}
for c in cats:
    cid = str(c['id'])
    cat_map[f"?product_cat={cid}"] = c['url']
    cat_map[f"https://hosseinykala.ir/?product_cat={cid}"] = c['url']

# Also add common typos found in existing articles:
# e.g., ?product_cat=94 was used for air cooler (which is actually ID 95)
air_cooler_url = "https://hosseinykala.ir/product-category/%da%a9%d9%88%d9%84%d8%b1-%d8%a2%d8%a8%db%8c/"
cat_map["?product_cat=94"] = air_cooler_url
cat_map["https://hosseinykala.ir/?product_cat=94"] = air_cooler_url

# In post 3217, ?product_cat=123 was used for "سرخ کن" (fryer is 121, 123 is blender)
# Let's inspect how it was used: if used as سرخ کن:
fryer_url = "https://hosseinykala.ir/product-category/%d8%b3%d8%b1%d8%ae-%da%a9%d9%86/"
# In post 3217 text is "دسته‌بندی سرخ کن" -> fryer_url
# But blender is 123
blender_url = "https://hosseinykala.ir/product-category/%d9%85%d8%ae%d9%84%d9%88%d8%b7-%da%a9%d9%86/"

print(f"Generated {len(cat_map)} category query mappings.")
for k, v in list(cat_map.items())[:15]:
    print(f"  {k}  ==>  {v}")

with open('data/category_url_replacements.json', 'w', encoding='utf-8') as f:
    json.dump(cat_map, f, ensure_ascii=False, indent=2)
