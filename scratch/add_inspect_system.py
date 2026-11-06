import urllib.request
import base64
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

creds = base64.b64encode(b'agent:Mlwg pHHX NQ64 drrz 7ca2 IVto').decode('utf-8')

# Read snippet 4
req = urllib.request.Request('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/4', headers={
    'Authorization': 'Basic ' + creds,
    'User-Agent': 'Mozilla/5.0'
})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode('utf-8'))

code = data.get('code', '')

# Add /inspect-system endpoint before the closing });
inspect_route = """
    register_rest_route('hk-perf/v1', '/inspect-system', [
        'methods' => 'GET',
        'permission_callback' => '__return_true',
        'callback' => function () {
            $ac_file = WP_CONTENT_DIR . '/advanced-cache.php';
            $mu_dir = WP_CONTENT_DIR . '/mu-plugins';
            $hk_cache_dir = WP_CONTENT_DIR . '/cache/hk_fastcache';
            
            $mu_files = is_dir($mu_dir) ? scandir($mu_dir) : [];
            $cache_files = is_dir($hk_cache_dir) ? count(scandir($hk_cache_dir)) - 2 : 0;
            
            return [
                'wp_cache_defined' => defined('WP_CACHE') ? WP_CACHE : 'NOT_DEFINED',
                'advanced_cache_exists' => file_exists($ac_file),
                'advanced_cache_size' => file_exists($ac_file) ? filesize($ac_file) : 0,
                'advanced_cache_preview' => file_exists($ac_file) ? substr(file_get_contents($ac_file), 0, 500) : '',
                'mu_plugins' => $mu_files,
                'hk_cache_dir_exists' => is_dir($hk_cache_dir),
                'hk_cache_file_count' => $cache_files,
                'server_software' => $_SERVER['SERVER_SOFTWARE'] ?? '',
                'lscwp_cache_enabled' => get_option('litespeed.conf.cache') ?: get_option('litespeed-cache-conf.cache')
            ];
        }
    ]);
"""

if '/inspect-system' not in code:
    code = code.replace("});", inspect_route + "\n});")

# Update snippet 4
update_req = urllib.request.Request(
    'https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/4',
    headers={
        'Authorization': 'Basic ' + creds,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    },
    data=json.dumps({'code': code}).encode('utf-8'),
    method='POST'
)
with urllib.request.urlopen(update_req, timeout=15) as resp:
    res = json.loads(resp.read().decode('utf-8'))
    print("Snippet 4 updated! ID:", res.get('id'), "Active:", res.get('active'))
