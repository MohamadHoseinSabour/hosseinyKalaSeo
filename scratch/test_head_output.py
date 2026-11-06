import requests
import urllib3
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_test = """<?php
add_action('init', function() {
    ob_start();
    do_action('wp_head');
    $head_out = ob_get_clean();
    header('Content-Type: text/plain; charset=utf-8');
    echo "--- CAPTURED WP_HEAD ---\n";
    echo substr($head_out, 0, 2000);
    exit;
}, 999);
"""

requests.post(url, cookies=cookies, data={
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'temp_test_wp_head.php',
    'text': php_test
}, verify=False)

r_trig = requests.get('https://hosseinykala.ir/?test_wp_head=1', headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
print("Captured wp_head:\n", r_trig.text[:2000])

requests.post('https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER', cookies=cookies, data={
    'action': 'multiple',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'select0': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins/temp_test_wp_head.php',
    'button': 'delete'
}, verify=False)
