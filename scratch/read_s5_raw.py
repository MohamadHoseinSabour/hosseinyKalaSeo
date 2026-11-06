import requests
import urllib3
import json
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
add_action('init', function() {
    global $wpdb;
    $s = $wpdb->get_var("SELECT code FROM {$wpdb->prefix}snippets WHERE id = 5");
    header('Content-Type: text/plain; charset=utf-8');
    echo $s;
    exit;
}, 1);
"""

requests.post(url, cookies=cookies, data={
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'temp_read_s5_raw.php',
    'text': php_code
}, verify=False)

r_trig = requests.get('https://hosseinykala.ir/?read_s5_raw=1', headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
print("Snippet 5 code in DB:\n", r_trig.text)

requests.post('https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER', cookies=cookies, data={
    'action': 'multiple',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'select0': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins/temp_read_s5_raw.php',
    'button': 'delete'
}, verify=False)
