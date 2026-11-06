import json

with open('divar_preloaded_state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

cp = state.get('currentPost', {})
print("currentPost keys:", list(cp.keys()))
post = cp.get('post', {})
print("post keys:", list(post.keys()))
for k, v in post.items():
    if k in ['data', 'token', 'title', 'widgets', 'sections', 'header']:
        print(f"=== {k} ===")
        print(str(v)[:500])
