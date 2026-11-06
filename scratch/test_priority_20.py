import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
add_action('init', function() {
    $st = session_status();
    file_put_contents(WP_CONTENT_DIR . '/trace_19.txt', "Priority 19.9: session_status=$st\\n");
    
    global $wp_filter;
    if (isset($wp_filter['init']->callbacks[20])) {
        foreach ($wp_filter['init']->callbacks[20] as $idx => $handler) {
            $func = $handler['function'];
            $name = '';
            if (is_string($func)) $name = $func;
            elseif (is_array($func)) {
                $cls = is_object($func[0]) ? get_class($func[0]) : $func[0];
                $name = $cls . '::' . $func[1];
            } else $name = 'Closure';
            
            $wp_filter['init']->callbacks[20][$idx]['function'] = function(...$args) use ($func, $name) {
                $before = session_status();
                $res = call_user_func_array($func, $args);
                $after = session_status();
                if ($before === 1 && $after === 2) {
                    file_put_contents(WP_CONTENT_DIR . '/culprit_20.txt', "CULPRIT IS AT PRIORITY 20: $name");
                }
                return $res;
            };
        }
    }
}, 19.9);
"""

data = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'find_session.php',
    'text': php_code
}
requests.post(url, cookies=cookies, data=data, verify=False)
