import requests
import json

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

r = requests.get('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/5', auth=auth, headers=headers, timeout=10)
s5 = r.json()

# Append conditional dequeue logic to snippet 5
dequeue_code = r"""
// 4. Dequeue non-critical styles from Homepage
add_action('wp_enqueue_scripts', function () {
    if (is_front_page()) {
        wp_dequeue_style('wc-blocks-style-rtl');
        wp_dequeue_style('wc-blocks-style');
        wp_dequeue_style('lpl-ticket');
        wp_dequeue_style('lpl-support-public');
        wp_dequeue_style('luman-ios-notification-style');
    }
}, 9999);
"""

if 'Dequeue non-critical styles' not in s5['code']:
    s5['code'] += dequeue_code

res = requests.put('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/5', auth=auth, headers=headers, json=s5, timeout=15)
print("Updated Snippet 5 with dequeue logic:", res.status_code)

# Purge cache
r_p = requests.post('https://hosseinykala.ir/wp-json/hk-perf/v1/purge-all', auth=auth, headers=headers, timeout=15)
print("Purge cache:", r_p.json())
