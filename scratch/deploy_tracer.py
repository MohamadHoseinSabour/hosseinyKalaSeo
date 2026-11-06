import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
add_action('all', function($tag) {
    if (session_status() === PHP_SESSION_ACTIVE && !defined('SESSION_LOGGED')) {
        define('SESSION_LOGGED', true);
        $bt = debug_backtrace(DEBUG_BACKTRACE_IGNORE_ARGS, 15);
        $trace = [];
        foreach ($bt as $b) {
            $f = isset($b['file']) ? $b['file'] : '';
            $l = isset($b['line']) ? $b['line'] : '';
            $fn = isset($b['function']) ? $b['function'] : '';
            $trace[] = $f . ':' . $l . ' (' . $fn . ')';
        }
        $info = [
            'hook' => $tag,
            'session_keys' => isset($_SESSION) ? array_keys($_SESSION) : [],
            'trace' => $trace
        ];
        file_put_contents(WP_CONTENT_DIR . '/session_culprit.json', json_encode($info, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
    }
});
"""

data = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'find_session.php',
    'text': php_code
}
r = requests.post(url, cookies=cookies, data=data, verify=False)
print('Save find_session.php response:', r.status_code, r.text[:100])
