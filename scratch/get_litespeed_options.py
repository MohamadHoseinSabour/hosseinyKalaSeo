import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
add_action('init', function() {
    global $wpdb;
    $rows = $wpdb->get_results("SELECT option_name, option_value FROM {$wpdb->options} WHERE option_name LIKE '%litespeed%'");
    $data = [];
    foreach ($rows as $r) {
        $val = maybe_unserialize($r->option_value);
        $data[$r->option_name] = $val;
    }
    file_put_contents(WP_CONTENT_DIR . '/litespeed_db_options.json', json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
}, 5);
"""

data = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'inspect_litespeed.php',
    'text': php_code
}
requests.post(url, cookies=cookies, data=data, verify=False)
