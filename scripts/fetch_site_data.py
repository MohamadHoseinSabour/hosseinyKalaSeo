import os
import sys
import json
import urllib.parse
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Reconfigure stdout for Persian characters
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_categories():
    print("Fetching categories from hosseinykala.ir...", flush=True)
    categories = []
    seen_urls = set()

    source_urls = [
        'https://hosseinykala.ir/',
        'https://hosseinykala.ir/shop/'
    ]

    for source in source_urls:
        try:
            r = requests.get(source, headers=HEADERS, timeout=15)
            if r.status_code != 200:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')
            
            for a in soup.find_all('a', href=True):
                href = a['href']
                text = a.get_text(strip=True)
                
                if 'product-category' in href or 'product_cat' in href:
                    clean_url = href.split('?')[0].rstrip('/') + '/'
                    if clean_url not in seen_urls and text:
                        seen_urls.add(clean_url)
                        slug = clean_url.rstrip('/').split('/')[-1]
                        categories.append({
                            'name': text,
                            'url': clean_url,
                            'slug': urllib.parse.unquote(slug)
                        })
        except Exception as e:
            print(f"Error fetching {source}: {e}", flush=True)

    print(f"Total categories discovered: {len(categories)}", flush=True)
    return categories

def extract_product_info(url):
    for attempt in range(2):
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code != 200:
                continue

            soup = BeautifulSoup(r.text, 'html.parser')

            product_data = {
                'url': url,
                'slug': urllib.parse.unquote(url.rstrip('/').split('/')[-1]),
                'name': '',
                'price': None,
                'currency': 'IRT',
                'in_stock': True,
                'category': '',
                'sku': '',
                'image': '',
                'short_description': '',
                'description': ''
            }

            h1 = soup.find('h1')
            if h1:
                product_data['name'] = h1.get_text(strip=True)

            for s in soup.find_all('script', type='application/ld+json'):
                try:
                    data = json.loads(s.string)
                    graph = data.get('@graph', [data]) if isinstance(data, dict) else data
                    for item in graph:
                        if isinstance(item, dict) and item.get('@type') == 'Product':
                            if item.get('name'):
                                product_data['name'] = item['name']
                            if item.get('sku'):
                                product_data['sku'] = str(item['sku'])
                            if item.get('description'):
                                product_data['description'] = item['description']
                            if item.get('image'):
                                img = item['image']
                                if isinstance(img, list) and len(img) > 0:
                                    product_data['image'] = img[0]
                                elif isinstance(img, str):
                                    product_data['image'] = img
                                elif isinstance(img, dict) and img.get('url'):
                                    product_data['image'] = img['url']
                            
                            offers = item.get('offers')
                            if isinstance(offers, list) and len(offers) > 0:
                                offers = offers[0]
                            if isinstance(offers, dict):
                                product_data['price'] = offers.get('price')
                                product_data['currency'] = offers.get('priceCurrency', 'IRT')
                                avail = offers.get('availability', '')
                                product_data['in_stock'] = 'InStock' in avail
                        
                        elif isinstance(item, dict) and item.get('@type') == 'BreadcrumbList':
                            elems = item.get('itemListElement', [])
                            if len(elems) >= 2:
                                product_data['category'] = elems[-2].get('item', {}).get('name', '')
                except Exception:
                    pass

            if not product_data['price']:
                price_elem = soup.find('p', class_='price') or soup.find('span', class_='woocommerce-Price-amount')
                if price_elem:
                    product_data['price'] = price_elem.get_text(strip=True)

            if not product_data['category']:
                cat_elem = soup.find('span', class_='posted_in')
                if cat_elem:
                    product_data['category'] = cat_elem.get_text(strip=True).replace('دسته:', '').replace('Category:', '').strip()

            if not product_data['image']:
                img_elem = soup.find('img', class_='wp-post-image') or soup.find('meta', property='og:image')
                if img_elem:
                    product_data['image'] = img_elem.get('src') or img_elem.get('content') or ''

            return product_data
        except Exception as e:
            if attempt == 1:
                print(f"Failed extracting {url}: {e}", flush=True)

    return None

def fetch_products():
    print("Fetching product list from sitemap...", flush=True)
    sitemap_url = 'https://hosseinykala.ir/product-sitemap.xml'
    r = requests.get(sitemap_url, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        print("Failed to fetch product-sitemap.xml", flush=True)
        return []

    root = ET.fromstring(r.content)
    prod_urls = [child[0].text for child in root if child[0].tag.endswith('loc')]
    print(f"Discovered {len(prod_urls)} product URLs in sitemap.", flush=True)

    products = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(extract_product_info, prod_urls))
        for p in results:
            if p:
                products.append(p)

    print(f"Successfully extracted {len(products)} products.", flush=True)
    return products

def main():
    cats = fetch_categories()
    cat_file = os.path.join(DATA_DIR, 'categories.json')
    with open(cat_file, 'w', encoding='utf-8') as f:
        json.dump(cats, f, ensure_ascii=False, indent=2)
    print(f"Saved categories to {cat_file}", flush=True)

    prods = fetch_products()
    prod_file = os.path.join(DATA_DIR, 'products.json')
    with open(prod_file, 'w', encoding='utf-8') as f:
        json.dump(prods, f, ensure_ascii=False, indent=2)
    print(f"Saved products to {prod_file}", flush=True)

if __name__ == '__main__':
    main()
