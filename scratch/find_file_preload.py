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
    $dir = get_stylesheet_directory();
    $files = glob($dir . '/*.php');
    $res = [];
    foreach ($files as $f) {
        $content = file_get_contents($f);
        if (strpos($content, 'ds1.webp') !== false || strpos($content, 'preload') !== false) {
            $res[basename($f)] = substr($content, 0, 500);
        }
    }
    
    // Check parent theme
    $pdir = get_template_directory();
    $pfiles = glob($pdir . '/*.php');
    foreach ($pfiles as $f) {
        $content = file_get_contents($f);
        if (strpos($content, 'ds1.webp') !== false) {
            $res['parent_' . basename($f)] = substr($content, 0, 500);
        }
    }
    
    // Also check active hooks on wp_head
    global $wp_filter;
    $head_hooks = array_keys($wp_filter['wp_head']->callbacks ?? []);
    
    echo json_encode(['theme_matches' => $res, 'head_hook_priorities' => $head_hooks]);
    exit;
}, 1);
"""

requests.post(url, cookies=cookies, data={
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'temp_find_file_preload.php',
    'text': php_code
}, verify=False)

r_trig = requests.get('https://hosseinykala.ir/?find_file_preload=1', headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
print("File preload result:\n", r_trig.text[:1500])

requests.post('https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER', cookies=cookies, data={
    'action': 'multiple',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'select0': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins/temp_find_file_preload.php',
    'button': 'delete'
}, verify=False)
