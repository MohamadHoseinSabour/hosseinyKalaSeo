import requests

r = requests.get('https://hosseinykala.ir/', headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
lines = r.text.splitlines()
print(f"Total lines in HTML: {len(lines)}")

# Let's inspect around lines 6800-6870
for idx in range(max(0, 6800), min(len(lines), 6870)):
    print(f"{idx+1}: {lines[idx]}")
