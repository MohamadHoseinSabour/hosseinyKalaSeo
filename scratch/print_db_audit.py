import json

with open('scratch/db_audit_report.json', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total Autoload: {data['total_autoload_kb']} KB across {data['total_autoload_count']} rows")
print(f"Expired transients: {data['expired_transients_count']} ({data['expired_transients_kb']} KB)")
print(f"Total transients: {data['total_transients_count']} ({data['total_transients_kb']} KB)")
print(f"Revisions: {data['revisions_count']} | Auto-drafts: {data['auto_drafts_count']} | Trash: {data['trash_posts_count']}")
print(f"Orphan postmeta: {data['orphan_postmeta_count']}")
print("Action Scheduler status:", data['action_scheduler_status'])

print("\nTop 15 Largest Autoloaded Options:")
for opt in data['top_autoload'][:15]:
    kb = round(float(opt['length']) / 1024, 1)
    print(f"  - {opt['option_name']}: {kb} KB")

print("\nTop 10 Largest Tables:")
for t in data['top_tables'][:10]:
    print(f"  - {t['name']}: {t['size_mb']} MB ({t['rows_count']} rows)")
