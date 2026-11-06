import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
add_action('init', function() {
    $mods = function_exists('apache_get_modules') ? apache_get_modules() : 'N/A';
    file_put_contents(WP_CONTENT_DIR . '/apache_mods.json', json_encode($mods, JSON_PRETTY_PRINT));
}, 1);
"""

data = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'inspect_env.php',
    'text': php_code
}
requests.post(url, cookies=cookies, data=data, verify=False)
