import re, sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/db_backup_pre_optimization.sql.gz', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

submits = re.findall(r'<input[^>]+type=["\']?submit["\']?[^>]*>', text, re.I)
for s in submits:
    print('Submit:', s)
