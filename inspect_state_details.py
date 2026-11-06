import json

with open('divar_preloaded_state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

for k in ['appMeta', 'currentPost', 'httpError', 'premiumPanel']:
    print(f"=== {k} ===")
    print(json.dumps(state.get(k), ensure_ascii=False, indent=2)[:500])
