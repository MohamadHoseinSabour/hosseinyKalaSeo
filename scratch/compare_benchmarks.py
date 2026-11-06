import json

with open('scratch/audit_results/baseline_benchmark.json', encoding='utf-8') as f:
    b = json.load(f)
with open('scratch/audit_results/after_benchmark.json', encoding='utf-8') as f:
    a = json.load(f)

print(f"{'Page':<12} | {'Before TTFB':<12} | {'After TTFB':<12} | {'Before Total':<13} | {'After Total':<12} | {'Improvement':<12}")
print("-" * 85)
for name in b:
    if name in a and 'avg_ttfb_ms' in a[name]:
        b_ttfb = b[name]['avg_ttfb_ms']
        a_ttfb = a[name]['avg_ttfb_ms']
        b_tot = b[name]['avg_total_ms']
        a_tot = a[name]['avg_total_ms']
        pct = (1 - (a_tot / b_tot)) * 100
        print(f"{name:<12} | {b_ttfb:<10.0f}ms | {a_ttfb:<10.0f}ms | {b_tot:<11.0f}ms | {a_tot:<10.0f}ms | {pct:>10.1f}%")
