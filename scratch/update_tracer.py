import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
add_action('init', function() {
    file_put_contents(WP_CONTENT_DIR . '/init_start.txt', 'init start session_status: ' . session_status());
}, -99999);

add_action('all', function($tag) {
    static $first = true;
    if ($first && session_status() === PHP_SESSION_ACTIVE) {
        $first = false;
        file_put_contents(WP_CONTENT_DIR . '/first_active.txt', 'Active on hook: ' . $tag . "\n" . print_r(debug_backtrace(DEBUG_BACKTRACE_IGNORE_ARGS, 8), true));
    }
});
"""

data = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'find_session.php',
    'text': php_code
}
requests.post(url, cookies=cookies, data=data, verify=False)
