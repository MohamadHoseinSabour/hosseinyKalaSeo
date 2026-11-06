import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
$priorities = [-100, -11, -9, -2, 0, 1, 2, 5, 10, 20];
foreach ($priorities as $p) {
    add_action('init', function() use ($p) {
        $st = session_status();
        $msg = "init at priority {$p}: session_status={$st}\\n";
        file_put_contents(WP_CONTENT_DIR . '/session_p_trace.txt', $msg, FILE_APPEND);
    }, $p);
}
"""

data = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'find_session.php',
    'text': php_code
}
requests.post(url, cookies=cookies, data=data, verify=False)
