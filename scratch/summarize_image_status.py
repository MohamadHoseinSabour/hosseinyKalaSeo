import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base = 'new_product_images'

total_folders = 0
total_downloaded = 0
total_pending = 0

print("=" * 70)
print("گزارش جامع وضعیت پوشه‌ها و تصاویر محصولات جدید (حسینی کالا)")
print("=" * 70)

for cat in sorted(os.listdir(base)):
    cat_dir = os.path.join(base, cat)
    if not os.path.isdir(cat_dir):
        continue
    prods = sorted(os.listdir(cat_dir))
    print(f"\n📂 دسته‌بندی: 【 {cat} 】 ({len(prods)} محصول)")
    print("-" * 70)
    for p in prods:
        p_dir = os.path.join(cat_dir, p)
        if not os.path.isdir(p_dir):
            continue
        total_folders += 1
        files = os.listdir(p_dir)
        img_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        has_guide = 'راهنمای_تصویر_نیاز_به_بررسی.txt' in files
        
        if img_files:
            total_downloaded += 1
            img_info = []
            for img in img_files:
                sz = os.path.getsize(os.path.join(p_dir, img)) // 1024
                img_info.append(f"{img} ({sz} KB)")
            print(f"  ✓ [تصویر آماده] {p}")
            print(f"      فایل‌ها: {', '.join(img_info)}")
        else:
            total_pending += 1
            print(f"  ⏳ [پوشه آماده جهت بارگذاری کاربر] {p}")
            if has_guide:
                print(f"      فایل راهنما: راهنمای_تصویر_نیاز_به_بررسی.txt مستقر شد")

print("\n" + "=" * 70)
print(f"آمار کل:")
print(f"  • کل پوشه‌های ایجادشده: {total_folders}")
print(f"  • موارد دارای تصویر معتبر و دانلودشده: {total_downloaded}")
print(f"  • موارد نیازمند بررسی / بارگذاری توسط کاربر: {total_pending}")
print("=" * 70)
