import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('divar_api_calls.json', 'r', encoding='utf-8') as f:
    calls = json.load(f)

all_posts = []
seen_tokens = set()

for c in calls:
    if 'brand-landing/xTlfvkBc' in c['url']:
        data = c['data']
        widgets = data.get('post_row_widget_list', [])
        for w in widgets:
            # check widget structure
            w_data = w.get('widget_type') or w.get('data', {})
            # let's inspect the keys of w
            all_posts.append(w)

print(f"Total raw widgets: {len(all_posts)}")
with open('divar_raw_widgets.json', 'w', encoding='utf-8') as f:
    json.dump(all_posts, f, ensure_ascii=False, indent=2)

# Inspect the first widget
if all_posts:
    print("Widget 0 keys:", list(all_posts[0].keys()))
    print("Widget 0 preview:", json.dumps(all_posts[0], ensure_ascii=False, indent=2)[:800])
