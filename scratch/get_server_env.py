import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
add_action('init', function() {
    $info = [
        'php_version' => phpversion(),
        'php_sapi' => php_sapi_name(),
        'server_software' => $_SERVER['SERVER_SOFTWARE'] ?? 'N/A',
        'opcache_enabled' => function_exists('opcache_get_status') && is_array(opcache_get_status()) && opcache_get_status()['opcache_enabled'],
        'extensions' => [
            'redis' => extension_loaded('redis'),
            'memcached' => extension_loaded('memcached'),
            'opcache' => extension_loaded('Zend OPcache'),
            'imagick' => extension_loaded('imagick'),
            'curl' => extension_loaded('curl'),
            'mbstring' => extension_loaded('mbstring'),
        ],
        'memory_limit' => ini_get('memory_limit'),
        'max_execution_time' => ini_get('max_execution_time'),
    ];
    file_put_contents(WP_CONTENT_DIR . '/server_environment.json', json_encode($info, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
}, 1);
"""

data = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'inspect_env.php',
    'text': php_code
}
requests.post(url, cookies=cookies, data=data, verify=False)
