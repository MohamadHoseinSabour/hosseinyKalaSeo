import json

with open('scratch/live_diagnostics.json', 'r', encoding='utf-8') as f:
    diag = json.load(f)

print("Active Plugins:")
for p in diag.get('active_plugins', []):
    print(f"  - {p}")

print("\nElementor Options:")
for k in ['elementor_css_print_method', 'elementor_load_fa4_shim', 'elementor_font_display', 'elementor_optimized_image_loading', 'elementor_optimized_font_loading']:
    print(f"  {k}: {diag.get(k)}")

print("\nPerfmatters Options:")
pm = diag.get('perfmatters', {})
if isinstance(pm, dict):
    for section, vals in pm.items():
        print(f"  [{section}]: {vals}")
else:
    print("  Perfmatters options is not dict:", pm)

print("\nLiteSpeed Optimization Options:")
ls = diag.get('lscache_conf', {})
if isinstance(ls, dict):
    for k, v in ls.items():
        if any(w in k for w in ['optm', 'css', 'js', 'media', 'font', 'cache']):
            print(f"  {k}: {v}")
