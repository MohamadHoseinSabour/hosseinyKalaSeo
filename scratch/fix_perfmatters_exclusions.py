import requests
import json

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# 1. Update Perfmatters to exclude jquery and wp-i18n from defer
payload = {
    'perfmatters': {
        'assets': {
            'js_exclusions': 'jquery.min.js, jquery.js, i18n.min.js, hooks.min.js'
        }
    }
}

r = requests.post('https://hosseinykala.ir/wp-json/hk-perf/v1/set-perf-options', auth=auth, headers=headers, json=payload, timeout=15)
print("Updated Perfmatters js_exclusions:", r.status_code, r.json())
