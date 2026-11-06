import requests
import urllib3
import time

urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
add_action('init', function() {
    global $wpdb;
    $wpdb->query("UPDATE {$wpdb->options} SET autoload = 'no' WHERE option_name LIKE 'revslider%' AND autoload = 'yes'");
}, 1);
"""

requests.post(url, cookies=cookies, data={'action': 'edit', 'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins', 'filename': 'clean_rev.php', 'text': php_code}, verify=False)
time.sleep(1)
requests.get('https://hosseinykala.ir/?clean_rev=1', headers={'User-Agent': 'Mozilla/5.0'})
time.sleep(1)
requests.post(url, cookies=cookies, data={'action': 'delete', 'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins', 'select0': 'clean_rev.php'}, verify=False)
print('Disabled autoload for all remaining revslider options!')
