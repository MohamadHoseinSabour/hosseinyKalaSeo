import urllib.request
import base64
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

creds = base64.b64encode(b'agent:Mlwg pHHX NQ64 drrz 7ca2 IVto').decode('utf-8')
headers = {
    'Authorization': 'Basic ' + creds,
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}

req = urllib.request.Request(
    'https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/7',
    headers=headers
)
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode('utf-8'))

current_code = data.get('code', '')

script_unload_block = r'''
// =========================================================================
// 6. ASSET UNLOADER & SCRIPT LIGHTENING FOR BLOG POSTS (Task T-3.4)
// =========================================================================
add_action('wp_print_scripts', function () {
    if (is_singular('post')) {
        global $wp_scripts;
        if ($wp_scripts instanceof WP_Scripts) {
            foreach ([
                'wc-cart-fragments',
                'wc-order-attribution',
                'sourcebuster-js',
                'lpl-ticket-public',
                'lpl-support-public',
                'jquery-ui-core'
            ] as $handle) {
                wp_dequeue_script($handle);
                wp_deregister_script($handle);
            }
        }
    }
}, 99999);

add_action('wp_print_footer_scripts', function () {
    if (is_singular('post')) {
        foreach ([
            'xts-mini-cart-quantity-method',
            'xts-single-product-quantity-method',
            'xts-xts-swiper-library',
            'xts-add-swiper-structure-method',
            'xts-swiper-init-method',
            'xts-product-wishlist-method',
            'xts-offcanvas-cart-widget-method'
        ] as $handle) {
            wp_dequeue_script($handle);
            wp_deregister_script($handle);
        }
    }
}, 1);
'''

# In the output buffer, also clean up strip for blog posts
buffer_strip_code = r'''
        // 3.6. Clean up unneeded product/swiper script tags on blog posts
        if (is_singular('post')) {
            $unneeded_ids = [
                'xts-mini-cart-quantity-method-js',
                'xts-single-product-quantity-method-js',
                'xts-xts-swiper-library-js',
                'xts-add-swiper-structure-method-js',
                'xts-swiper-init-method-js',
                'xts-offcanvas-cart-widget-method-js',
                'xts-product-wishlist-method-js'
            ];
            foreach ($unneeded_ids as $sid) {
                $buffer = preg_replace('/<script\s+[^>]*id=["\']' . preg_quote($sid, '/') . '["\'][^>]*>.*?<\/script>/is', '', $buffer);
            }
        }

        return $buffer;
    });'''

# Replace in buffer
current_code = current_code.replace("return $buffer;\n    });", buffer_strip_code)

idx = current_code.find('// 6. ASSET UNLOADER')
if idx != -1:
    updated_code = current_code[:idx] + script_unload_block.strip()
else:
    updated_code = current_code + "\n" + script_unload_block

payload = {
    'code': updated_code,
    'active': True
}

update_req = urllib.request.Request(
    'https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/7',
    headers=headers,
    data=json.dumps(payload).encode('utf-8'),
    method='POST'
)

with urllib.request.urlopen(update_req, timeout=15) as resp:
    res = json.loads(resp.read().decode('utf-8'))
    print("Snippet 7 updated with full T-3.4 unloader! Active:", res.get('active'))

# Purge cache
try:
    purge_req = urllib.request.Request(
        'https://hosseinykala.ir/wp-json/hk-perf/v1/purge-all',
        headers={'Authorization': 'Basic ' + creds},
        data=b'{}'
    )
    with urllib.request.urlopen(purge_req, timeout=15) as resp:
        print("Purge Cache Response:", resp.read().decode('utf-8'))
except Exception as e:
    print("Purge Cache Warning:", e)

print("T-3.4 full unloader complete.")
