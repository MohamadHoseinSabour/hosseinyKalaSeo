import os, shutil, glob, sys
sys.stdout.reconfigure(encoding='utf-8')

# Folders to delete
folders_to_delete = [
    'divar image',
    'product_images_2026-10-05',
    'new_product_images',
    'extracted_products',
    'new_products'
]

# Backup files to delete (keeping hosseiny_kala_catalog.xlsx and hosseiny_kala_catalog.backup_fix_20261012_233911.xlsx as the single safe backup)
excel_backups_to_delete = [
    'hosseiny_kala_catalog.backup.xlsx',
    'hosseiny_kala_catalog.backup_20261012_130656.xlsx',
    'hosseiny_kala_catalog.backup_20261012_232425.xlsx',
    'hosseiny_kala_catalog.backup_20261012_232513.xlsx',
    'hosseiny_kala_catalog.backup_20261012_232554.xlsx',
    'hosseiny_kala_catalog.backup_colors_20261012_142555.xlsx',
    'hosseiny_kala_catalog_latest.xlsx'
]

deleted_bytes = 0
deleted_files = 0

for folder in folders_to_delete:
    if os.path.exists(folder):
        f_size = 0
        f_count = 0
        for root, dirs, files in os.walk(folder):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    f_size += os.path.getsize(fp)
                    f_count += 1
                except:
                    pass
        print(f"Deleting folder: {folder} ({f_count} files, {f_size / (1024*1024):.2f} MB)...")
        shutil.rmtree(folder, ignore_errors=True)
        deleted_bytes += f_size
        deleted_files += f_count

for ef in excel_backups_to_delete:
    if os.path.exists(ef):
        try:
            sz = os.path.getsize(ef)
            os.remove(ef)
            deleted_bytes += sz
            deleted_files += 1
            print(f"Deleted excess backup: {ef} ({sz / (1024*1024):.2f} MB)")
        except Exception as e:
            print(f"Could not delete {ef}: {e}")

# Clean temporary images/artifacts in scratch, keep only useful python scripts
if os.path.exists('scratch'):
    scratch_cleaned = 0
    scratch_size = 0
    for root, dirs, files in os.walk('scratch', topdown=False):
        for f in files:
            if not f.endswith('.py') and not f.endswith('.json'):
                fp = os.path.join(root, f)
                try:
                    sz = os.path.getsize(fp)
                    os.remove(fp)
                    scratch_size += sz
                    scratch_cleaned += 1
                except:
                    pass
        # delete empty subdirectories in scratch
        for d in dirs:
            dp = os.path.join(root, d)
            try:
                if not os.listdir(dp):
                    os.rmdir(dp)
            except:
                pass
    print(f"Cleaned scratch temporary cache: {scratch_cleaned} files, {scratch_size / (1024*1024):.2f} MB")
    deleted_bytes += scratch_size
    deleted_files += scratch_cleaned

print(f"\n✅ Total cleaned: {deleted_files} files, {deleted_bytes / (1024*1024):.2f} MB freed!")
