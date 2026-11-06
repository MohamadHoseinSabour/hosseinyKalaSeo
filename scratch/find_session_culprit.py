import requests
import time
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0'}

def check_homepage_session():
    r = requests.get('https://hosseinykala.ir/', headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    has_session = 'PHPSESSID' in r.headers.get('set-cookie', '')
    cc = r.headers.get('cache-control', '')
    return has_session, cc

baseline_session, baseline_cc = check_homepage_session()
print(f"Baseline: PHPSESSID={baseline_session} | Cache-Control={baseline_cc}")

candidate_plugins = [
    'ClubCoreWP-main/clubcore',
    'RTL-CareUnit/RTL-CareUnit',
    'sync-basalam-plugin-pro/sync-basalam-pro',
    'sync-basalam/sync-basalam',
    'products-extractor-for-woocommerce/wcpe',
    'emalls-extraction-api-official/emalls-extraction-api-official',
    'webp-express/webp-express',
    'wp-parsidate/wp-parsidate',
    'contact-form-7/wp-contact-form-7',
    'luman-plus/luman-plus'
]

culprit = None

for plugin in candidate_plugins:
    print(f"\nTesting deactivation of: {plugin} ...")
    # Deactivate
    r_deact = requests.post(
        f'https://hosseinykala.ir/wp-json/wp/v2/plugins/{plugin}',
        auth=auth,
        headers=headers,
        json={'status': 'inactive'},
        timeout=15
    )
    if r_deact.status_code != 200:
        print(f"  Failed to deactivate {plugin}: {r_deact.status_code}")
        continue
    
    time.sleep(0.5)
    has_session, cc = check_homepage_session()
    print(f"  Result: PHPSESSID={has_session} | Cache-Control={cc}")
    
    # Reactivate immediately
    r_act = requests.post(
        f'https://hosseinykala.ir/wp-json/wp/v2/plugins/{plugin}',
        auth=auth,
        headers=headers,
        json={'status': 'active'},
        timeout=15
    )
    if r_act.status_code == 200:
        print(f"  Reactivated {plugin} successfully.")
    else:
        print(f"  ERROR reactivating {plugin}: {r_act.status_code}")
        
    if not has_session:
        print(f"\n🎯 FOUND CULPRIT: {plugin} is the source of PHPSESSID!")
        culprit = plugin
        break

if not culprit:
    print("\nNone of the candidate plugins was the culprit. It may be in WooCommerce, Elementor, RankMath, or Theme.")
