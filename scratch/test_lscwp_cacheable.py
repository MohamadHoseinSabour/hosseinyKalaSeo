import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
add_action('shutdown', function() {
    $info = [];
    if (class_exists('LiteSpeed\Control')) {
        $info['is_cacheable'] = \LiteSpeed\Control::is_cacheable();
        $info['get_nocache_reason'] = method_exists('LiteSpeed\Control', 'get_nocache_reason') ? \LiteSpeed\Control::get_nocache_reason() : 'N/A';
    }
    $info['headers'] = headers_list();
    file_put_contents(WP_CONTENT_DIR . '/lscwp_cacheable.json', json_encode($info, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
}, 99999);
"""

data = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'inspect_cacheable.php',
    'text': php_code
}
requests.post(url, cookies=cookies, data=data, verify=False)
