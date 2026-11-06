"""Comprehensive Performance Benchmark and Deep Asset Audit for hosseinykala.ir."""

import os
import sys
import time
import json
import re
import urllib.parse
from bs4 import BeautifulSoup
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
}

URLS = {
    'Homepage': 'https://hosseinykala.ir/',
    'Product': 'https://hosseinykala.ir/product/depoint-decent-combi-refrigerator-freezer/',
    'Category': 'https://hosseinykala.ir/product-category/refrigerator-freezer/',
    'Blog': 'https://hosseinykala.ir/refah-bank-beta-installment-guide/',
    'Cart': 'https://hosseinykala.ir/cart/',
    'Checkout': 'https://hosseinykala.ir/checkout/',
    'Account': 'https://hosseinykala.ir/my-account/',
    'Search': 'https://hosseinykala.ir/?s=%DB%8C%D8%AE%DA%86%D8%A7%D9%84',
}

def benchmark_url(name, url, runs=3):
    print(f"\n=======================================================")
    print(f"Testing [{name}]: {url}")
    print(f"=======================================================")
    
    session = requests.Session()
    session.headers.update(HEADERS)
    
    timings = []
    ttfbs = []
    last_response = None
    
    for i in range(runs):
        start = time.perf_counter()
        r = session.get(url, timeout=30, stream=True)
        # TTFB is roughly time until headers / first chunk
        first_byte_time = None
        content = bytearray()
        for chunk in r.iter_content(chunk_size=4096):
            if first_byte_time is None:
                first_byte_time = time.perf_counter()
            content.extend(chunk)
        end = time.perf_counter()
        
        ttfb = (first_byte_time - start) if first_byte_time else (end - start)
        total_time = end - start
        
        timings.append(total_time)
        ttfbs.append(ttfb)
        last_response = (r, bytes(content))
        
        cache_status = r.headers.get('x-litespeed-cache', 'none')
        print(f"  Run {i+1}: TTFB = {ttfb*1000:.1f}ms | Total = {total_time*1000:.1f}ms | HTTP {r.status_code} | LS-Cache: {cache_status}")
        time.sleep(0.5)
        
    avg_ttfb = sum(ttfbs) / len(ttfbs)
    avg_total = sum(timings) / len(timings)
    
    resp, html_bytes = last_response
    
    # Audit assets from the HTML
    html_text = ""
    try:
        html_text = html_bytes.decode('utf-8', errors='replace')
    except Exception:
        pass
        
    soup = BeautifulSoup(html_text, 'html.parser')
    
    # CSS
    css_links = [l.get('href') for l in soup.find_all('link', rel='stylesheet') if l.get('href')]
    inline_styles = [s.get_text() for s in soup.find_all('style')]
    inline_style_bytes = sum(len(s.encode('utf-8')) for s in inline_styles)
    
    # JS
    js_scripts = [s.get('src') for s in soup.find_all('script') if s.get('src')]
    inline_scripts = [s.get_text() for s in soup.find_all('script') if not s.get('src')]
    inline_js_bytes = sum(len(s.encode('utf-8')) for s in inline_scripts)
    
    # Images
    images = soup.find_all('img')
    lazy_images = [img for img in images if img.get('loading') == 'lazy' or 'lazyload' in img.get('class', [])]
    missing_dims = [img for img in images if not img.get('width') or not img.get('height')]
    
    # Categorize CSS / JS by source
    plugins_detected = set()
    for src in css_links + js_scripts:
        if 'wp-content/plugins/' in src:
            match = re.search(r'wp-content/plugins/([^/]+)/', src)
            if match:
                plugins_detected.add(match.group(1))
        elif 'wp-content/themes/' in src:
            match = re.search(r'wp-content/themes/([^/]+)/', src)
            if match:
                plugins_detected.add(f"theme:{match.group(1)}")
                
    cookies = resp.headers.get('set-cookie', 'None')
    cache_control = resp.headers.get('cache-control', 'None')
    litespeed_cache = resp.headers.get('x-litespeed-cache', 'None')
    litespeed_tags = resp.headers.get('x-litespeed-tag', 'None')
    server = resp.headers.get('server', 'None')
    content_encoding = resp.headers.get('content-encoding', 'None')
    
    audit_data = {
        'name': name,
        'url': url,
        'http_status': resp.status_code,
        'avg_ttfb_ms': round(avg_ttfb * 1000, 1),
        'avg_total_ms': round(avg_total * 1000, 1),
        'min_ttfb_ms': round(min(ttfbs) * 1000, 1),
        'min_total_ms': round(min(timings) * 1000, 1),
        'html_size_kb': round(len(html_bytes) / 1024, 1),
        'server': server,
        'cache_control': cache_control,
        'litespeed_cache': litespeed_cache,
        'litespeed_tags': litespeed_tags[:100] if litespeed_tags != 'None' else 'None',
        'set_cookie': cookies[:120] if cookies != 'None' else 'None',
        'content_encoding': content_encoding,
        'css_files_count': len(css_links),
        'css_sample': css_links[:5],
        'inline_style_blocks': len(inline_styles),
        'inline_style_kb': round(inline_style_bytes / 1024, 1),
        'js_files_count': len(js_scripts),
        'js_sample': js_scripts[:5],
        'inline_script_blocks': len(inline_scripts),
        'inline_js_kb': round(inline_js_bytes / 1024, 1),
        'images_count': len(images),
        'lazy_images_count': len(lazy_images),
        'images_missing_dims': len(missing_dims),
        'detected_plugins_in_assets': sorted(list(plugins_detected))
    }
    
    print(f"  Summary:")
    print(f"    - Avg TTFB: {audit_data['avg_ttfb_ms']} ms (Min: {audit_data['min_ttfb_ms']} ms)")
    print(f"    - HTML Size: {audit_data['html_size_kb']} KB")
    print(f"    - CSS Files: {audit_data['css_files_count']} | Inline Style: {audit_data['inline_style_kb']} KB ({audit_data['inline_style_blocks']} blocks)")
    print(f"    - JS Files: {audit_data['js_files_count']} | Inline JS: {audit_data['inline_js_kb']} KB ({audit_data['inline_script_blocks']} blocks)")
    print(f"    - Images: {audit_data['images_count']} (Lazy: {audit_data['lazy_images_count']}, Missing Dims: {audit_data['images_missing_dims']})")
    print(f"    - Cache-Control: {cache_control}")
    print(f"    - LS-Cache Header: {litespeed_cache}")
    print(f"    - Set-Cookie: {cookies[:80]}")
    print(f"    - Assets originating from: {', '.join(audit_data['detected_plugins_in_assets'][:8])}...")
    
    return audit_data

def main():
    os.makedirs('scratch/audit_results', exist_ok=True)
    results = {}
    for name, url in URLS.items():
        try:
            results[name] = benchmark_url(name, url, runs=3)
        except Exception as e:
            print(f"Error testing {name} ({url}): {e}")
            results[name] = {'error': str(e)}
            
    with open('scratch/audit_results/baseline_benchmark.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\n[SUCCESS] Baseline benchmarks saved to scratch/audit_results/baseline_benchmark.json")

if __name__ == '__main__':
    main()
