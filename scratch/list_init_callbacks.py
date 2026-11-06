import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
add_action('wp_loaded', function() {
    global $wp_filter;
    $callbacks = [];
    if (isset($wp_filter['init'])) {
        foreach ($wp_filter['init']->callbacks as $priority => $handlers) {
            foreach ($handlers as $idx => $handler) {
                $func = $handler['function'];
                $name = '';
                if (is_string($func)) {
                    $name = $func;
                } elseif (is_array($func)) {
                    $class = is_object($func[0]) ? get_class($func[0]) : $func[0];
                    $name = $class . '::' . $func[1];
                } elseif ($func instanceof Closure) {
                    $rf = new ReflectionFunction($func);
                    $name = 'Closure at ' . $rf->getFileName() . ':' . $rf->getStartLine();
                }
                $callbacks[] = "[$priority] " . $name;
            }
        }
    }
    file_put_contents(WP_CONTENT_DIR . '/init_callbacks.txt', implode("\n", $callbacks));
}, 99999);
"""

data = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'find_session.php',
    'text': php_code
}
requests.post(url, cookies=cookies, data=data, verify=False)
