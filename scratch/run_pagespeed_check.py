import requests
import json
import time

url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://hosseinykala.ir/&strategy=mobile"
print("Running Google PageSpeed Insights API for https://hosseinykala.ir/ (mobile)...")
t0 = time.time()
try:
    r = requests.get(url, timeout=90)
    dur = time.time() - t0
    print(f"PageSpeed API response status: {r.status_code} in {dur:.1f}s")
    if r.status_code == 200:
        data = r.json()
        lh = data.get('lighthouseResult', {})
        cats = lh.get('categories', {})
        perf_score = int(cats.get('performance', {}).get('score', 0) * 100)
        audits = lh.get('audits', {})
        
        fcp = audits.get('first-contentful-paint', {}).get('displayValue')
        lcp = audits.get('largest-contentful-paint', {}).get('displayValue')
        tbt = audits.get('total-blocking-time', {}).get('displayValue')
        cls = audits.get('cumulative-layout-shift', {}).get('displayValue')
        si = audits.get('speed-index', {}).get('displayValue')
        
        rb = audits.get('render-blocking-resources', {})
        rb_savings = rb.get('details', {}).get('overallSavingsMs', 0) if rb.get('details') else 0
        
        img_savings = audits.get('uses-optimized-images', {}).get('details', {}).get('overallSavingsBytes', 0)
        cache_savings = audits.get('uses-long-cache-ttl', {}).get('details', {}).get('overallSavingsBytes', 0)

        print("\n=== GOOGLE PAGESPEED RESULTS (MOBILE) ===")
        print(f"Performance Score: {perf_score}")
        print(f"FCP:               {fcp}")
        print(f"LCP:               {lcp}")
        print(f"TBT:               {tbt}")
        print(f"CLS:               {cls}")
        print(f"Speed Index:       {si}")
        print(f"Render Blocking:   {rb_savings} ms savings")
        print(f"Image Savings:     {img_savings / 1024:.1f} KB")
        print(f"Cache TTL Savings: {cache_savings / 1024:.1f} KB")
        
        with open('scratch/pagespeed_after.json', 'w', encoding='utf-8') as f:
            json.dump({
                'score': perf_score,
                'fcp': fcp,
                'lcp': lcp,
                'tbt': tbt,
                'cls': cls,
                'speed_index': si,
                'rb_savings_ms': rb_savings,
                'img_savings_bytes': img_savings,
                'cache_savings_bytes': cache_savings
            }, f, indent=2)
    else:
        print("PageSpeed error:", r.text[:300])
except Exception as e:
    print("PageSpeed request failed:", e)
