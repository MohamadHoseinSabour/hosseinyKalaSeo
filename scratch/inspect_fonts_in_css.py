import re
import requests

with open('scratch/live_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all font URLs in HTML
font_matches = re.findall(r'https?://[^\s\'"()]+\.(?:woff2?|ttf|eot)', html)
print(f"Fonts found in HTML: {len(font_matches)}")
for fm in set(font_matches):
    print("  HTML font:", fm)

# Find CSS link in HTML
css_links = re.findall(r'href=["\'](https://hosseinykala\.ir/wp-content/[^"\']+\.css[^"\']*)["\']', html)
print(f"\nCSS links found: {len(css_links)}")
for cl in css_links:
    print("  CSS link:", cl)
    try:
        r = requests.get(cl, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        css_text = r.text
        css_fonts = re.findall(r'url\((["\']?[^)]+\.(?:woff2?|ttf|eot)[^)]*)\)', css_text)
        print(f"    Fonts in CSS ({len(css_fonts)} total, {len(set(css_fonts))} unique):")
        for cf in sorted(list(set(css_fonts))):
            print(f"      {cf}")
    except Exception as e:
        print(f"    Error fetching CSS: {e}")
