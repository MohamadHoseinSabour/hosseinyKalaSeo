import sys
import re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open("chrome_dump.html", "r", encoding="utf-8") as f:
    html = f.read()

print("HTML length:", len(html))

# Check page title
m_title = re.search(r'<title[^>]*>(.*?)</title>', html)
print("Title:", m_title.group(1) if m_title else "No title")

soup = BeautifulSoup(html, 'html.parser')

h1s = [h.get_text(strip=True) for h in soup.find_all('h1')]
h2s = [h.get_text(strip=True) for h in soup.find_all('h2')]
h3s = [h.get_text(strip=True) for h in soup.find_all('h3')]
print("H1:", h1s)
print("H2 count:", len(h2s), h2s[:5])
print("H3 count:", len(h3s), h3s[:10])

# Find links to posts (/v/...)
links = soup.find_all('a', href=True)
post_links = []
for a in links:
    href = a['href']
    if '/v/' in href:
        post_links.append((href, a.get_text(separator=' | ', strip=True)))

print(f"Found {len(post_links)} post links:")
for href, text in post_links:
    print(f" - [{text}] -> {href}")

