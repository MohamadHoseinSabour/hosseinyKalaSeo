import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
add_action('init', function() {
    $info = [];
    if (class_exists('XTS\Modules\WC_Social_Authentication')) {
        $rc = new ReflectionClass('XTS\Modules\WC_Social_Authentication');
        $info['social_auth_file'] = $rc->getFileName();
        if ($rc->hasMethod('authentication')) {
            $rm = $rc->getMethod('authentication');
            $info['authentication_start_line'] = $rm->getStartLine();
        }
    }
    file_put_contents(WP_CONTENT_DIR . '/reflection_info.json', json_encode($info, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
}, 19);
"""

data = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'find_session.php',
    'text': php_code
}
requests.post(url, cookies=cookies, data=data, verify=False)
