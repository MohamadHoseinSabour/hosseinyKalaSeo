import requests
import urllib3
import json
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
add_action('init', function() {
    global $wp_filter;
    $res = [];
    if (isset($wp_filter['wp_head'])) {
        foreach ($wp_filter['wp_head']->callbacks as $prio => $cbs) {
            foreach ($cbs as $id => $cb) {
                if ($cb['function'] instanceof Closure) {
                    $ref = new ReflectionFunction($cb['function']);
                    $res[] = [
                        'priority' => $prio,
                        'file' => $ref->getFileName(),
                        'start_line' => $ref->getStartLine(),
                        'end_line' => $ref->getEndLine()
                    ];
                }
            }
        }
    }
    echo json_encode($res, JSON_PRETTY_PRINT);
    exit;
}, 1);
"""

requests.post(url, cookies=cookies, data={
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'temp_reflect_head.php',
    'text': php_code
}, verify=False)

r_trig = requests.get('https://hosseinykala.ir/?reflect_head=1', headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
print("wp_head closures:\n", r_trig.text)

requests.post('https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER', cookies=cookies, data={
    'action': 'multiple',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'select0': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins/temp_reflect_head.php',
    'button': 'delete'
}, verify=False)
