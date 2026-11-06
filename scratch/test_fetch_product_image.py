import sys
import os
import requests
import json
from bs4 import BeautifulSoup
from PIL import Image
import io

sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

# Test finding image for Kahler iron 812
query = "اتو بخار کاخلر مدل KH-812"
print(f"Searching for: {query}...")

# We can search Torob or Digikala or Google images
# Let's test Torob search API
torob_url = f"https://api.torob.com/v4/base-product/search/?sort=popularity&page=0&size=5&query={requests.utils.quote(query)}"
try:
    r = requests.get(torob_url, headers=HEADERS, timeout=10)
    print("Torob status:", r.status_code)
    if r.status_code == 200:
        data = r.json()
        results = data.get('results', [])
        print(f"Found {len(results)} results in Torob.")
        for res in results[:3]:
            print(f"  Title: {res.get('name1')} | Image: {res.get('image_url')}")
except Exception as e:
    print("Torob error:", e)
