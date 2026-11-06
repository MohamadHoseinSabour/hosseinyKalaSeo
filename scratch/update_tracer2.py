import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
$GLOBALS['hook_log'] = [];

add_action('all', function($tag) {
    if (session_status() === PHP_SESSION_ACTIVE) {
        if (!defined('SESSION_FOUND_EXACT')) {
            define('SESSION_FOUND_EXACT', true);
            $last_hooks = array_slice($GLOBALS['hook_log'], -15);
            $bt = debug_backtrace(DEBUG_BACKTRACE_IGNORE_ARGS, 10);
            $trace = [];
            foreach ($bt as $b) {
                $f = isset($b['file']) ? $b['file'] : '';
                $l = isset($b['line']) ? $b['line'] : '';
                $fn = isset($b['function']) ? $b['function'] : '';
                $trace[] = $f . ':' . $l . ' (' . $fn . ')';
            }
            $out = [
                'active_tag' => $tag,
                'last_hooks_before_session' => $last_hooks,
                'trace' => $trace
            ];
            file_put_contents(WP_CONTENT_DIR . '/session_exact.json', json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
        }
    } else {
        $GLOBALS['hook_log'][] = $tag;
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
