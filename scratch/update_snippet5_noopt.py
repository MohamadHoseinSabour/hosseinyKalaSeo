import requests
import urllib3
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

snippet_code = r"""/**
 * HosseinyKala - Core Web Vitals, LCP Preload & Layout Reservation Engine
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

    // 4. Critical Layout Reservation with data-no-optimize="1"
    echo '<style id="hk-lcp-cls-optimizer" data-no-optimize="1">
    .xts-iimage-img-wrapper, .xts-iimage-img { aspect-ratio: 2057 / 765; width: 100%; display: block; background-color: #f5f5f7; overflow: hidden; }
    .xts-iimage-img img { aspect-ratio: 2057 / 765; width: 100%; height: auto; object-fit: cover; }
    .xts-logo img.xts-logo-main { width: 250px !important; height: 52px !important; aspect-ratio: 300 / 62; max-width: 100%; height: auto; display: inline-block; }
    .xts-product-thumb, .xts-product-image { aspect-ratio: 1 / 1; width: 100%; background-color: #f8f8fa; display: block; overflow: hidden; }
    .xts-product-image img { aspect-ratio: 1 / 1; width: 100%; height: 100%; object-fit: contain; }
    .xts-cat-thumbnail, .xts-cat-image { aspect-ratio: 1 / 1; width: 100%; background-color: #f8f8fa; overflow: hidden; }
    .woocommerce-product-gallery__wrapper, .woocommerce-product-gallery__image { aspect-ratio: 1 / 1; width: 100%; background-color: #ffffff; }
    @media (min-width: 768px) { .elementor-element.e-parent:nth-child(n+3), .xts-footer { content-visibility: auto; contain-intrinsic-size: 0 600px; } }
    @media (max-width: 767px) { .elementor-element.e-parent:nth-child(n+2), .xts-footer { content-visibility: auto; contain-intrinsic-size: 0 450px; } }
    body, button, input, select, textarea, h1, h2, h3, h4, h5, h6, .xts-entities-title { font-display: swap !important; }
    </style>' . "\n";
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
            'name' => 'Preload & Layout Reservation - Core Web Vitals',
            'code' => $code,
            'active' => 1
        ],
        ['id' => 5]
    );
    echo json_encode(['status' => 'snippet_5_noopt_updated']);
    exit;
}, 1);
"""

requests.post(url, cookies=cookies, data={
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'temp_update_s5_noopt.php',
    'text': php_update_script
}, verify=False)

r_trig = requests.get('https://hosseinykala.ir/?update_s5_noopt=1', headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
print("Update Snippet 5 result:\n", r_trig.text)

requests.post('https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER', cookies=cookies, data={
    'action': 'multiple',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'select0': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins/temp_update_s5_noopt.php',
    'button': 'delete'
}, verify=False)
