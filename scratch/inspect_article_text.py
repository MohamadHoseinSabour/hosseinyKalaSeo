import urllib.request
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request('https://hosseinykala.ir/contact', headers={'User-Agent': 'Mozilla/5.0 (iPhone)'})
with urllib.request.urlopen(req) as r:
    html = r.read().decode('utf-8', errors='ignore')

# Extract main content inside #main-content or article
main_content = re.search(r'(<article[^>]*>.*?</article>)', html, re.DOTALL)
if main_content:
    article_text = re.sub(r'<[^>]+>', ' ', main_content.group(1))
    clean_lines = [line.strip() for line in article_text.split('\n') if line.strip()]
    print("Article content text (first 30 lines):")
    for l in clean_lines[:30]:
        print(" ", l)
else:
    print("No <article> found!")
