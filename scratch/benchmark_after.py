"""Compare Before and After Benchmarks for hosseinykala.ir."""

import os
import sys
import time
import json
import requests
from bs4 import BeautifulSoup

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
}

URLS = {
    'Homepage': 'https://hosseinykala.ir/',
    'Product': 'https://hosseinykala.ir/product/depoint-decent-combi-refrigerator-freezer/',
    'Category': 'https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/',
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
    
    # Prime cache first
    try:
        session.get(url, timeout=25)
        time.sleep(0.5)
    except Exception as e:
        print(f"  Warmup error: {e}")
        
    timings = []
    ttfbs = []
    last_response = None
    
    for i in range(runs):
        start = time.perf_counter()
        r = session.get(url, timeout=30, stream=True)
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
        
        cache_status = r.headers.get('x-hosseinykala-cache', r.headers.get('x-litespeed-cache', 'none'))
        print(f"  Run {i+1}: TTFB = {ttfb*1000:.1f}ms | Total = {total_time*1000:.1f}ms | HTTP {r.status_code} | Cache: {cache_status}")
        time.sleep(0.5)
        
    avg_ttfb = sum(ttfbs) / len(ttfbs)
    avg_total = sum(timings) / len(timings)
    
    resp, html_bytes = last_response
    
    return {
        'name': name,
        'url': url,
        'http_status': resp.status_code,
        'avg_ttfb_ms': round(avg_ttfb * 1000, 1),
        'avg_total_ms': round(avg_total * 1000, 1),
        'min_ttfb_ms': round(min(ttfbs) * 1000, 1),
        'min_total_ms': round(min(timings) * 1000, 1),
        'cache_status': resp.headers.get('x-hosseinykala-cache', 'NONE'),
        'cache_control': resp.headers.get('cache-control', 'None'),
        'content_encoding': resp.headers.get('content-encoding', 'None')
    }

def main():
    os.makedirs('scratch/audit_results', exist_ok=True)
    results = {}
    for name, url in URLS.items():
        try:
            results[name] = benchmark_url(name, url, runs=3)
        except Exception as e:
            print(f"Error testing {name}: {e}")
            results[name] = {'error': str(e)}
            
    with open('scratch/audit_results/after_benchmark.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\n[SUCCESS] After benchmarks saved to scratch/audit_results/after_benchmark.json")

if __name__ == '__main__':
    main()
