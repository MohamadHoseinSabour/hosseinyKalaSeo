import urllib.request
import json
import urllib.parse
import sys
sys.stdout.reconfigure(encoding='utf-8')

query = "پتوشور پاکیزان 30"
url = f"https://api.torob.com/v4/base-product/search/?sort=popularity&page=0&size=5&query={urllib.parse.quote(query)}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        results = data.get('results', [])
        print(f"Results for '{query}': {len(results)}")
        for r in results[:3]:
            print(f" - Title: {r.get('name1')}")
            print(f"   Image URL: {r.get('image_url')}")
except Exception as e:
    print("Error:", e)
