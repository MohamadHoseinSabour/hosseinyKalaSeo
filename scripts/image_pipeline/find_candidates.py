import os
import sys
import re
import requests
import json
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

def clean_query(text):
    # Remove emojis and unnecessary symbols
    text = re.sub(r'[📂◀↳]', '', text)
    return text.strip()

def search_digikala_candidates(query, max_items=5):
    candidates = []
    try:
        url = "https://api.digikala.com/v1/search/"
        params = {"q": clean_query(query)}
        resp = requests.get(url, params=params, headers=HEADERS, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            products = data.get('data', {}).get('products', [])
            for p in products[:max_items]:
                main_img = p.get('images', {}).get('main', {}).get('url', [])
                if main_img:
                    raw_url = main_img[0].split('?')[0]  # remove resize parameters for maximum quality
                    candidates.append({
                        'source': 'digikala',
                        'product_id': p.get('id'),
                        'title': p.get('title_fa'),
                        'url': raw_url
                    })
    except Exception as e:
        print(f"Error searching Digikala for '{query}': {e}")
    return candidates

def download_candidate(img_url, dest_path):
    try:
        resp = requests.get(img_url, headers=HEADERS, timeout=15)
        if resp.status_code == 200 and len(resp.content) > 5000:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, 'wb') as f:
                f.write(resp.content)
            
            # Verify valid image
            img = Image.open(dest_path)
            width, height = img.size
            return {
                'status': 'success',
                'path': dest_path,
                'width': width,
                'height': height,
                'format': img.format,
                'bytes': len(resp.content)
            }
    except Exception as e:
        return {'status': 'error', 'error': str(e)}
    return {'status': 'failed'}

if __name__ == '__main__':
    q = sys.argv[1] if len(sys.argv) > 1 else 'هیمالیا آیس پول'
    cands = search_digikala_candidates(q)
    print(json.dumps(cands, ensure_ascii=False, indent=2))
