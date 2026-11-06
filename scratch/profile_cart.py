import requests
import urllib3
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_tracer = """<?php
$GLOBALS['hk_t0'] = microtime(true);
$GLOBALS['hk_marks'] = [];

function hk_record_mark($name) {
    $GLOBALS['hk_marks'][$name] = round((microtime(true) - $GLOBALS['hk_t0']) * 1000, 1);
}

hk_record_mark('mu_start');

add_action('plugins_loaded', function() { hk_record_mark('plugins_loaded'); }, 9999);
add_action('init', function() { hk_record_mark('init'); }, 9999);
add_action('wp_loaded', function() { hk_record_mark('wp_loaded'); }, 9999);
add_action('template_redirect', function() { hk_record_mark('template_redirect'); }, 9999);
add_action('wp_head', function() { hk_record_mark('wp_head'); }, 9999);
add_action('shutdown', function() {
    hk_record_mark('shutdown');
    if (isset($_GET['hk_profile'])) {
        header('Content-Type: application/json');
        echo json_encode([
            'timing_ms' => $GLOBALS['hk_marks'],
            'query_count' => get_num_queries(),
            'memory_mb' => round(memory_get_peak_usage() / 1024 / 1024, 2)
        ], JSON_PRETTY_PRINT);
        exit;
    }
}, 9999);
"""

requests.post(url, cookies=cookies, data={
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'temp_tracer.php',
    'text': php_tracer
}, verify=False)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
r = requests.get('https://hosseinykala.ir/cart/?hk_profile=1', headers=headers, allow_redirects=False, verify=False)
print("Cart profile status:", r.status_code)
print("Cart profile output:\n", r.text[:1000])

# Clean up
requests.post('https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER', cookies=cookies, data={
    'action': 'multiple',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'select0': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins/temp_tracer.php',
    'button': 'delete'
}, verify=False)
