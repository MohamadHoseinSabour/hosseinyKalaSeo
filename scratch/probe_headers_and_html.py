import requests

url = "https://hosseinykala.ir/"
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}, timeout=30)

print("All Headers:")
for k, v in r.headers.items():
    print(f"  {k}: {v}")

html = r.text
print("\nHTML length:", len(html))

# Check for comments at the end of HTML
comments = [line for line in html.splitlines()[-30:] if "<!--" in line or "-->" in line]
print("\nLast 30 lines comments:")
for c in comments:
    print(c)

# Search for caching plugin signatures
signatures = [
    "LiteSpeed", "litespeed", "perfmatters", "WP Rocket", "W3 Total Cache",
    "WP Super Cache", "Fastest Cache", "Autoptimize", "Hummingbird", "Cache-Control"
]
print("\nSignatures found in HTML:")
for s in signatures:
    count = html.count(s)
    if count > 0:
        print(f"  '{s}': {count} occurrences")
