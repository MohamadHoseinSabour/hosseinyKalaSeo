import requests
import urllib3
import time
import sys

urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
add_action('init', function() {
    global $wpdb;
    $rows = $wpdb->get_results("SELECT option_name, autoload, LENGTH(option_value) as len FROM {$wpdb->options} WHERE option_name LIKE '%revslider%'");
    file_put_contents(WP_CONTENT_DIR . '/revslider_test.json', json_encode($rows, JSON_PRETTY_PRINT));
}, 1);
"""

requests.post(url, cookies=cookies, data={'action': 'edit', 'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins', 'filename': 'check_rev.php', 'text': php_code}, verify=False)
time.sleep(1)
requests.get('https://hosseinykala.ir/?check_rev=1', headers={'User-Agent': 'Mozilla/5.0'})
time.sleep(1)
r = requests.get('https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER/domains/hosseinykala.ir/public_html/wp-content/revslider_test.json', cookies=cookies, verify=False)
print('Revslider rows:\n', r.text)

requests.post(url, cookies=cookies, data={'action': 'delete', 'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins', 'select0': 'check_rev.php'}, verify=False)
requests.post(url, cookies=cookies, data={'action': 'delete', 'path': '/domains/hosseinykala.ir/public_html/wp-content', 'select0': 'revslider_test.json'}, verify=False)
