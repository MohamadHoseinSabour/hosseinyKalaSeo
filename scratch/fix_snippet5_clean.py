import requests
import urllib3
import json
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

# Plain valid PHP snippet code
snippet_code = r"""/**
 * HosseinyKala - Core Web Vitals & LCP Image & Font Preload Engine
 */
add_action('wp_head', function () {
    // 1. Preload primary Persian fonts for instant text rendering (Eliminates FOUT/FOIT)
    echo '<link rel="preload" href="/wp-content/themes/xts-luman/fonts/iranyekanx/woff2/IRANYekanXFaNum-Regular.woff2" as="font" type="font/woff2" crossorigin>' . "\n";
    echo '<link rel="preload" href="/wp-content/themes/xts-luman/fonts/iranyekanx/woff2/IRANYekanXFaNum-Bold.woff2" as="font" type="font/woff2" crossorigin>' . "\n";

    // 2. Preload true LCP Hero image on Homepage
    if (is_front_page()) {
        echo '<link rel="preload" as="image" href="https://hosseinykala.ir/wp-content/uploads/2026/10/clover-home-appliances-october-sale-banner.webp" fetchpriority="high">' . "\n";
    }

    // 3. Preload featured product image on single product pages
    if (function_exists('is_product') && is_product()) {
        $thumb_id = get_post_thumbnail_id();
        if ($thumb_id) {
            $img_url = wp_get_attachment_image_url($thumb_id, 'woocommerce_single');
            if ($img_url) {
                echo '<link rel="preload" as="image" href="' . esc_url($img_url) . '" fetchpriority="high">' . "\n";
            }
        }
    }
}, 1);"""

php_update_script = """<?php
add_action('init', function() {
    global $wpdb;
    $table = $wpdb->prefix . 'snippets';
    $code = <<<'EOD'
""" + snippet_code + """
EOD;
    $wpdb->update(
        $table,
        [
            'name' => 'Preload - فونت‌ها و بنر LCP اصلی',
            'code' => $code,
            'active' => 1
        ],
        ['id' => 5]
    );
    echo json_encode(['status' => 'success']);
    exit;
}, 1);
"""

requests.post(url, cookies=cookies, data={
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'temp_fix_s5.php',
    'text': php_update_script
}, verify=False)

r_trig = requests.get('https://hosseinykala.ir/?fix_s5=1', headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
print("Fix Snippet 5 result:\n", r_trig.text)

requests.post('https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER', cookies=cookies, data={
    'action': 'multiple',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'select0': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins/temp_fix_s5.php',
    'button': 'delete'
}, verify=False)
