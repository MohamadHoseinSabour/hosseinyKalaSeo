import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('divar_raw_widgets.json', 'r', encoding='utf-8') as f:
    widgets = json.load(f)

ads = []
for i, w in enumerate(widgets):
    data = w.get('data', {})
    title = data.get('title', '')
    action = data.get('action', {}).get('payload', {})
    token = action.get('token', '')
    price = data.get('middle_description_text', '')
    location = data.get('bottom_description_text', '')
    badge = data.get('red_text', '')
    image_url = data.get('image_url', '')
    
    ads.append({
        "index": i + 1,
        "title": title,
        "price": price,
        "location": location.strip(),
        "badge": badge,
        "token": token,
        "url": f"https://divar.ir/v/{token}" if token else ""
    })

print(f"Parsed {len(ads)} ads successfully.\n")
for ad in ads:
    print(f"{ad['index']:02d}. {ad['title']} | {ad['price']} | {ad['token']}")

with open('data/divar_current_ads.json', 'w', encoding='utf-8') as out:
    json.dump(ads, out, ensure_ascii=False, indent=2)
print("\nSaved to data/divar_current_ads.json")
