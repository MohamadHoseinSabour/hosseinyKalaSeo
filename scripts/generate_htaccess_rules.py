import json
import urllib.parse
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('data/404_redirect_mappings.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

lines = []
lines.append('# ============================================================')
lines.append('# 301 REDIRECT RULES FOR 46 GSC 404 URLs - HOSSEINY KALA')
lines.append('# Add these rules to your .htaccess file above WordPress rules')
lines.append('# ============================================================\n')
lines.append('<IfModule mod_rewrite.c>')
lines.append('RewriteEngine On\n')

# 1. Query parameters (?product_cat=ID)
lines.append('# --- 1. Fix ?product_cat=ID WooCommerce 404 Errors ---')
cat_query_items = [it for it in items if '?product_cat=' in it['source_url']]
for it in cat_query_items:
    cid = it['source_url'].split('?product_cat=')[1].strip()
    target_path = it['target_url'].replace('https://hosseinykala.ir', '')
    target_unquoted = urllib.parse.unquote(target_path)
    lines.append(f'RewriteCond %{{QUERY_STRING}} (?:^|&)product_cat={cid}(?:&|$)')
    lines.append(f'RewriteRule ^$ {target_unquoted}? [R=301,L]\n')

# 2. Malformed quote URLs
lines.append('# --- 2. Fix Malformed / Relative Escape Bug URLs ---')
lines.append('RewriteRule ^"?https:?/?/?hosseinykala\\.ir/?/?shop/?/?$ /shop/ [R=301,L]')
lines.append('RewriteRule ^"?https:?/?/?hosseinykala\\.ir/?/?$ / [R=301,L]')
lines.append('RewriteRule ^"?https:?/?/?hosseinykala\\.ir/?/?علاقه-مندی-ها/?/?$ / [R=301,L]')

product_malformed = [it for it in items if 'product//' in it['source_url']]
for it in product_malformed:
    src_part = it['source_url'].split('product//')[1].replace('///"', '').replace('///', '').strip()
    src_unquote = urllib.parse.unquote(src_part)
    target_path = it['target_url'].replace('https://hosseinykala.ir', '')
    lines.append(f'RewriteRule ^"?https:?/?/?hosseinykala\\.ir/?/?product/?/?{src_unquote}/?/?$ {target_path} [R=301,L]')

lines.append('\n# --- 3. Fix Deleted Category (اصلاح موی صورت) ---')
lines.append('RewriteRule ^product-category/اصلاح-موی-صورت/?.*$ /product-category/اصلاح-و-زیبایی/اصلاح-موی-سر/? [R=301,L]')

lines.append('\n# --- 4. Fix Crawler Wildcard Artifacts ---')
lines.append('RewriteRule ^wp-content/uploads/\\*$ / [R=301,L]')
lines.append('RewriteRule ^wp-content/\\*$ / [R=301,L]')
lines.append('RewriteRule ^wp-\\*\.php$ / [R=301,L]')
lines.append('RewriteRule ^\\*$ / [R=301,L]')

lines.append('</IfModule>\n')

with open('data/hosseinykala_404_htaccess_rules.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print('Generated .htaccess rules successfully!')
