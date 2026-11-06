import requests
import urllib3
import json
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

# Let's search inside wp_options where ds1.webp appears
php_search_all = """<?php
add_action('init', function() {
    global $wpdb;
    $rows = $wpdb->get_results("SELECT option_name, SUBSTRING(option_value, 1, 200) as val_snippet FROM {$wpdb->options} WHERE option_value LIKE '%ds1.webp%'");
    echo json_encode($rows, JSON_PRETTY_PRINT);
    exit;
}, 1);
"""

requests.post(url, cookies=cookies, data={
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'temp_find_all_ds1.php',
    'text': php_search_all
}, verify=False)

r_trig = requests.get('https://hosseinykala.ir/?find_all_ds1=1', headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
print("All options containing ds1.webp:\n", r_trig.text)

requests.post('https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER', cookies=cookies, data={
    'action': 'multiple',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'select0': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins/temp_find_all_ds1.php',
    'button': 'delete'
}, verify=False)
