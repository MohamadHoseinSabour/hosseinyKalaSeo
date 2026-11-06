import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
add_action('init', function() {
    global $wp_filter;
    if (!isset($wp_filter['init'])) return;
    
    // Iterate all callbacks from 10 to 20
    foreach ($wp_filter['init']->callbacks as $priority => $handlers) {
        if ($priority <= 10 || $priority > 20) continue;
        foreach ($handlers as $idx => $handler) {
            $func = $handler['function'];
            $name = '';
            if (is_string($func)) $name = $func;
            elseif (is_array($func)) {
                $cls = is_object($func[0]) ? get_class($func[0]) : $func[0];
                $name = $cls . '::' . $func[1];
            } elseif ($func instanceof Closure) {
                $name = 'Closure';
            }
            
            // Wrap callback
            $wp_filter['init']->callbacks[$priority][$idx]['function'] = function(...$args) use ($func, $name, $priority) {
                $before = session_status();
                $res = call_user_func_array($func, $args);
                $after = session_status();
                if ($before === 1 && $after === 2) {
                    file_put_contents(WP_CONTENT_DIR . '/culprit_exact.txt', "TRIGGERED BY [p=$priority]: $name");
                }
                return $res;
            };
        }
    }
}, 10.0001);
"""

data = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'find_session.php',
    'text': php_code
}
requests.post(url, cookies=cookies, data=data, verify=False)
