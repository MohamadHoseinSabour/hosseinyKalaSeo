import requests
import urllib3
import json
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_search = """<?php
add_action('init', function() {
    global $wpdb;
    $opt = $wpdb->get_results("SELECT option_name FROM {$wpdb->options} WHERE option_value LIKE '%ds1.webp%'");
    $posts = $wpdb->get_results("SELECT ID, post_title FROM {$wpdb->posts} WHERE post_content LIKE '%ds1.webp%' LIMIT 5");
    echo json_encode(['options' => $opt, 'posts' => $posts]);
    exit;
}, 1);
"""

r = requests.post(url, cookies=cookies, data={
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'temp_find_preload.php',
    'text': php_search
}, verify=False)

r_trig = requests.get('https://hosseinykala.ir/?find_preload=1', headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
print("Find preload result:\n", r_trig.text[:500])

requests.post('https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER', cookies=cookies, data={
    'action': 'multiple',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'select0': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins/temp_find_preload.php',
    'button': 'delete'
}, verify=False)
