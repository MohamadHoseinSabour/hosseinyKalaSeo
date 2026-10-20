import sys
import json
import urllib.parse
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

POST_TARGETS = {
    3000: 'portable-cellulose-air-cooler-guide',
    3098: 'mini-hotel-refrigerator-buying-guide',
    3099: '15-place-dishwasher-buying-guide',
    3100: 'combi-vs-twin-refrigerator-guide',
    3101: 'clover-brand-review',
    3102: 'economical-dowry-checklist-guide'
}

PRODUCT_TARGETS = {
    3453: 'electrosteel-future-twin-refrigerator-21ft',
    2972: 'clover-glory-plus-54ft-twin-refrigerator',
    3395: 'himalia-alpha-twin-refrigerator-28ft',
    3266: 'pakshoma-18000-split-air-conditioner'
}

def get_item_info(endpoint, item_id):
    url = f"https://hosseinykala.ir/wp-json/wp/v2/{endpoint}/{item_id}"
    try:
        r = requests.get(url, auth=AUTH, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            data = r.json()
            return {
                'id': item_id,
                'slug': data.get('slug'),
                'link': data.get('link'),
                'title': data.get('title', {}).get('rendered', '')
            }
        else:
            print(f"[ERR] Failed to get {endpoint}/{item_id}: HTTP {r.status_code}", flush=True)
            return None
    except Exception as e:
        print(f"[ERR] Exception fetching {endpoint}/{item_id}: {e}", flush=True)
        return None

def update_slug(endpoint, item_id, new_slug):
    url = f"https://hosseinykala.ir/wp-json/wp/v2/{endpoint}/{item_id}"
    payload = {'slug': new_slug}
    try:
        r = requests.post(url, json=payload, auth=AUTH, headers=HEADERS, timeout=20)
        if r.status_code == 200:
            data = r.json()
            returned_slug = data.get('slug')
            link = data.get('link')
            return {
                'success': True,
                'slug': returned_slug,
                'link': link
            }
        else:
            return {
                'success': False,
                'status_code': r.status_code,
                'error': r.text[:200]
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def test_url_redirect(old_url, new_url):
    results = {}
    try:
        # Test old URL without following redirects
        r_old = requests.get(old_url, headers=HEADERS, allow_redirects=False, timeout=15)
        results['old_status'] = r_old.status_code
        results['old_location'] = r_old.headers.get('Location', '')
        
        # Test old URL following redirects
        r_old_follow = requests.get(old_url, headers=HEADERS, allow_redirects=True, timeout=15)
        results['old_final_url'] = r_old_follow.url
        results['old_final_status'] = r_old_follow.status_code
    except Exception as e:
        results['old_err'] = str(e)

    try:
        # Test new URL directly
        r_new = requests.get(new_url, headers=HEADERS, allow_redirects=False, timeout=15)
        results['new_status'] = r_new.status_code
        results['new_location'] = r_new.headers.get('Location', '')
        
        if r_new.status_code in [301, 302, 307, 308]:
            r_new_follow = requests.get(new_url, headers=HEADERS, allow_redirects=True, timeout=15)
            results['new_final_url'] = r_new_follow.url
            results['new_final_status'] = r_new_follow.status_code
    except Exception as e:
        results['new_err'] = str(e)

    return results

def main():
    print("=" * 60, flush=True)
    print("PHASE 1: Fetching current state of posts and products", flush=True)
    print("=" * 60, flush=True)
    
    before_posts = {}
    for pid in POST_TARGETS:
        info = get_item_info('posts', pid)
        if info:
            before_posts[pid] = info
            print(f"[POST {pid}] Current slug: {info['slug']} | Link: {info['link']}", flush=True)
    
    before_products = {}
    for pid in PRODUCT_TARGETS:
        info = get_item_info('product', pid)
        if info:
            before_products[pid] = info
            print(f"[PRODUCT {pid}] Current slug: {info['slug']} | Link: {info['link']}", flush=True)

    print("\n" + "=" * 60, flush=True)
    print("PHASE 2: Updating Slugs to English", flush=True)
    print("=" * 60, flush=True)
    
    after_posts = {}
    for pid, target_slug in POST_TARGETS.items():
        print(f"Updating Post {pid} -> '{target_slug}'...", end=" ", flush=True)
        res = update_slug('posts', pid, target_slug)
        if res.get('success'):
            print(f"SUCCESS! New slug: '{res['slug']}', New link: {res['link']}", flush=True)
            after_posts[pid] = res
        else:
            print(f"FAILED! Error: {res}", flush=True)
            after_posts[pid] = res

    after_products = {}
    for pid, target_slug in PRODUCT_TARGETS.items():
        print(f"Updating Product {pid} -> '{target_slug}'...", end=" ", flush=True)
        res = update_slug('product', pid, target_slug)
        if res.get('success'):
            print(f"SUCCESS! New slug: '{res['slug']}', New link: {res['link']}", flush=True)
            after_products[pid] = res
        else:
            print(f"FAILED! Error: {res}", flush=True)
            after_products[pid] = res

    print("\n" + "=" * 60, flush=True)
    print("PHASE 3: Verifying HTTP Codes & Redirects", flush=True)
    print("=" * 60, flush=True)

    test_results = {'posts': {}, 'products': {}}

    print("\n--- Verifying Posts ---", flush=True)
    for pid, target_slug in POST_TARGETS.items():
        old_info = before_posts.get(pid, {})
        new_info = after_posts.get(pid, {})
        
        old_url = old_info.get('link')
        new_url = new_info.get('link')
        
        # If old_url equals new_url (for instance if it was already updated or same), construct old url from old slug
        if old_url and new_url:
            print(f"\n[Test Post {pid}]", flush=True)
            print(f"  Old URL: {old_url}", flush=True)
            print(f"  New URL: {new_url}", flush=True)
            
            res = test_url_redirect(old_url, new_url)
            test_results['posts'][pid] = {
                'old_url': old_url,
                'new_url': new_url,
                'checks': res
            }
            print(f"  Old URL Status: {res.get('old_status')} -> Location: {res.get('old_location')}", flush=True)
            print(f"  Old Follow Final: {res.get('old_final_status')} ({res.get('old_final_url')})", flush=True)
            print(f"  New URL Status: {res.get('new_status')}", flush=True)

    print("\n--- Verifying Products ---", flush=True)
    for pid, target_slug in PRODUCT_TARGETS.items():
        old_info = before_products.get(pid, {})
        new_info = after_products.get(pid, {})
        
        old_url = old_info.get('link')
        new_url = new_info.get('link')
        
        if old_url and new_url:
            print(f"\n[Test Product {pid}]", flush=True)
            print(f"  Old URL: {old_url}", flush=True)
            print(f"  New URL: {new_url}", flush=True)
            
            res = test_url_redirect(old_url, new_url)
            test_results['products'][pid] = {
                'old_url': old_url,
                'new_url': new_url,
                'checks': res
            }
            print(f"  Old URL Status: {res.get('old_status')} -> Location: {res.get('old_location')}", flush=True)
            print(f"  Old Follow Final: {res.get('old_final_status')} ({res.get('old_final_url')})", flush=True)
            print(f"  New URL Status: {res.get('new_status')}", flush=True)

    # Save summary report
    summary = {
        'before_posts': before_posts,
        'after_posts': after_posts,
        'before_products': before_products,
        'after_products': after_products,
        'test_results': test_results
    }
    with open('slug_update_verification_report.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60, flush=True)
    print("FINISHED. Report saved to slug_update_verification_report.json", flush=True)
    print("=" * 60, flush=True)

if __name__ == '__main__':
    main()
