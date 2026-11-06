import requests
import urllib3
import json
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_inspect = """<?php
add_action('init', function() {
    $opt = get_option('xts-luman-options');
    $matches = [];
    if (is_array($opt)) {
        foreach ($opt as $k => $v) {
            if (is_string($v) && strpos($v, 'ds1.webp') !== false) {
                $matches[$k] = $v;
            } elseif (is_array($v) && strpos(json_encode($v), 'ds1.webp') !== false) {
                $matches[$k] = $v;
            }
        }
    }
    echo json_encode(['matching_keys' => $matches]);
    exit;
}, 1);
"""

r = requests.post(url, cookies=cookies, data={
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'temp_inspect_opt.php',
    'text': php_inspect
}, verify=False)

r_trig = requests.get('https://hosseinykala.ir/?inspect_opt=1', headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
print("Inspect opt result:\n", r_trig.text[:500])

requests.post('https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER', cookies=cookies, data={
    'action': 'multiple',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'select0': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins/temp_inspect_opt.php',
    'button': 'delete'
}, verify=False)
