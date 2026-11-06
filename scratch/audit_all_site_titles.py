import os
import sys
import json
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\mmhhs\OneDrive\Documents\GitHub\hosseinyKalaSeo"
prods = json.load(open(os.path.join(PROJECT_DIR, 'data', 'products.json'), encoding='utf-8'))

print(f"Auditing all {len(prods)} site products...")

site_anomalies = []
for p in prods:
    pid = p['id']
    name = p['name']
    slug = p['slug']
    
    # 1. Check for typos
    issues = []
    if '  ' in name:
        issues.append("فاصله دوتایی (Double Space)")
    if '&amp;' in name:
        issues.append("کاراکتر &amp; خام")
    if 'ي' in name:
        issues.append("ی عربی به جای ی فارسی")
    if 'ك' in name:
        issues.append("ک عربی به جای ک فارسی")
    if 'هاورسون' in name or 'aversen' in name.lower():
        issues.append("نام هاورسون به جای هاورسن")
    if 'دیپونت' in name:
        issues.append("دیپونت به جای دیپوینت")
    if 'وستینگهوس' in name:
        issues.append("وستینگهوس به جای وستینگهاوس")
    if 'فلیپس' in name:
        issues.append("فلیپس به جای فیلیپس")
    if 'اینج' in name:
        issues.append("اینج به جای اینچ")
    if 'کلور54' in name:
        issues.append("کلور54 چسبیده")
    if '44 فوت' in name and '54 فوت' in name:
        issues.append("تناقض ظرفیت ۴۴ فوت و ۵۴ فوت")

    if issues:
        site_anomalies.append({
            'id': pid,
            'name': name,
            'slug': slug,
            'issues': issues
        })

print(f"Site products with title formatting anomalies: {len(site_anomalies)}")
for a in site_anomalies:
    print(f"PID {a['id']}: \"{a['name']}\" -> {', '.join(a['issues'])}")
