import urllib.request
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

url = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https%3A%2F%2Fhosseinykala.ir%2F&strategy=mobile&category=accessibility&category=performance&category=best-practices&category=seo'
print("Requesting Google PageSpeed Insights API (mobile)...")

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        
        lhr = data.get('lighthouseResult', {})
        cats = lhr.get('categories', {})
        print("\n===============================")
        print("GOOGLE LIGHTHOUSE MOBILE SCORES")
        print("===============================")
        for cat_name, cat_data in cats.items():
            score = int((cat_data.get('score', 0) or 0) * 100)
            print(f"  {cat_name.upper():<16}: {score}")

        audits = lhr.get('audits', {})
        print("\n--- Key Performance Metrics ---")
        for m in ['first-contentful-paint', 'largest-contentful-paint', 'total-blocking-time', 'cumulative-layout-shift', 'speed-index', 'server-response-time']:
            audit = audits.get(m, {})
            print(f"  {m:<24}: {audit.get('displayValue')} (score: {audit.get('score')})")

        # Check accessibility audit failures
        a11y_cat = cats.get('accessibility', {})
        audit_refs = a11y_cat.get('auditRefs', [])
        print("\n--- Accessibility Issues ---")
        found_issues = False
        for ref in audit_refs:
            ref_id = ref.get('id')
            audit = audits.get(ref_id, {})
            score = audit.get('score')
            if score is not None and score < 1:
                found_issues = True
                print(f"  FAILED [{ref_id}]: {audit.get('title')} (score: {score})")
                details = audit.get('details', {})
                items = details.get('items', [])
                for it in items[:5]:
                    node = it.get('node', {})
                    snippet = node.get('snippet') or it.get('description')
                    explanation = node.get('explanation')
                    print(f"    - Snippet: {snippet}")
                    if explanation:
                        print(f"      Explanation: {explanation}")

        if not found_issues:
            print("  No accessibility issues found! 100% score.")

        with open('scratch/latest_pagespeed_result.json', 'w', encoding='utf-8') as f:
            json.dump({
                'categories': {k: int((v.get('score', 0) or 0) * 100) for k, v in cats.items()},
                'metrics': {m: audits.get(m, {}).get('displayValue') for m in ['first-contentful-paint', 'largest-contentful-paint', 'total-blocking-time', 'cumulative-layout-shift', 'speed-index', 'server-response-time']}
            }, f, indent=2)

except Exception as e:
    print("Error querying PageSpeed API:", e)
