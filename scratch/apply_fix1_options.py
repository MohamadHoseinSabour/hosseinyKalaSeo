import requests
import json

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

payload = {
    'lscache_conf': {
        'cache-ttl_browser': '31536000',
        'optm-ucss': '',
        'optm-ccss_per_url': ''
    },
    'elementor_options': {
        'elementor_font_display': 'swap',
        'elementor_optimized_font_loading': '1'
    }
}

r = requests.post('https://hosseinykala.ir/wp-json/hk-perf/v1/set-perf-options', auth=auth, headers=headers, json=payload, timeout=15)
print("Set options status:", r.status_code)
print(r.json())

# Now purge all caches
r_purge = requests.post('https://hosseinykala.ir/wp-json/hk-perf/v1/purge-all', auth=auth, headers=headers, timeout=15)
print("Purge status:", r_purge.status_code, r_purge.json())
