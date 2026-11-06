import json

with open('divar_preloaded_state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

for k, v in state.items():
    s = str(v)
    if 'xTlfvkBc' in s or 'حسینی' in s:
        print(f"Key '{k}' contains match!")
        if isinstance(v, dict):
            print(f"  Keys of {k}: {list(v.keys())}")
            # print some preview
            for subk, subv in v.items():
                if 'xTlfvkBc' in str(subv) or 'حسینی' in str(subv):
                    print(f"    Subkey '{subk}' has match")
