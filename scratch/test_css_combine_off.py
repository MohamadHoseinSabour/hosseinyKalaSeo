import requests
import json

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# Test turning off optm-css_comb in LiteSpeed
payload = {
    'lscache_conf': {
        'optm-css_comb': '',
        'optm-css_comb_ext_inl': '',
        'optm-css_min': '1'
    }
}

r = requests.post('https://hosseinykala.ir/wp-json/hk-perf/v1/set-perf-options', auth=auth, headers=headers, json=payload, timeout=15)
print("Updated options:", r.json())

# Purge cache
r_p = requests.post('https://hosseinykala.ir/wp-json/hk-perf/v1/purge-all', auth=auth, headers=headers, timeout=15)
print("Purge status:", r_p.json())
