import json

with open('data/all_link_replacements.json', encoding='utf-8') as f:
    replacements = json.load(f)

# Sort descending by length
sorted_replacements = sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True)

target_files = [
    'scripts/publish_installment_clusters.py',
    'scripts/publish_installment_pillar.py',
    'scripts/publish_sub5.py',
    'scripts/publish_articles.py'
]

for file_path in target_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        orig_content = content
        count = 0
        for old_url, new_url in sorted_replacements:
            if old_url in content:
                c = content.count(old_url)
                content = content.replace(old_url, new_url)
                count += c
        
        if content != orig_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[UPDATED] {file_path}: {count} replacements made.")
        else:
            print(f"[NO CHANGE] {file_path}")
    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")
