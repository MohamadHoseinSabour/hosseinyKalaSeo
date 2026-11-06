import requests
import urllib3
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

perf_core_v25 = """<?php
/**
 * Plugin Name: Hosseiny Kala - Core Performance Optimization Engine
 * Description: High-Performance Caching, LCP Optimization, Image Box Reservation, and Core Web Vitals Stabilization.
 * Version: 2.5.0
 * Author: Antigravity Performance Engine
 */

defined('ABSPATH') || exit;

/* ==========================================================================
   1. SESSION CACHE-LIMITER FIX (Prevents PHP session from issuing no-cache)
   ========================================================================== */
if (function_exists('session_cache_limiter')) {
    session_cache_limiter('');
}

/* ==========================================================================
   2. GUEST CACHE-CONTROL HEADERS (Signal Browser, CDN & Web Server to Cache)
   ========================================================================== */
add_action('template_redirect', function () {
    if (is_admin() || wp_doing_ajax() || (defined('REST_REQUEST') && REST_REQUEST)) {
        return;
    }

    // Do NOT cache logged in users
    if (is_user_logged_in()) {
        return;
    }

    // Do NOT cache active WooCommerce carts or checkout
    if (function_exists('is_cart') && is_cart()) return;
    if (function_exists('is_checkout') && is_checkout()) return;
    if (function_exists('is_account_page') && is_account_page()) return;
    if (function_exists('WC') && WC()->cart && !WC()->cart->is_empty()) return;

    // For public guest pages, if session contains no custom data, allow clean caching
    if (empty($_SESSION)) {
        header_remove('Pragma');
        header_remove('Expires');
        header_remove('Cache-Control');
        
        header('Cache-Control: public, max-age=3600, stale-while-revalidate=86400');
        
        // Remove empty PHPSESSID cookie so requests remain cacheable
        if (!headers_sent()) {
            setcookie('PHPSESSID', '', time() - 3600, '/');
        }
    }
}, 9999);

/* ==========================================================================
   3. LAYOUT RESERVATION CSS & CONTENT VISIBILITY (Eliminates CLS, Boosts LCP)
   ========================================================================== */
add_action('wp_head', function () {
    ?>
    <style id="hk-lcp-cls-optimizer">
    /* 1. Reserve exact Hero Banner space before images load */
    .xts-iimage-img-wrapper,
    .xts-iimage-img {
        aspect-ratio: 2057 / 765;
        width: 100%;
        display: block;
        background-color: #f5f5f7;
        overflow: hidden;
    }
    .xts-iimage-img img {
        aspect-ratio: 2057 / 765;
        width: 100%;
        height: auto;
        object-fit: cover;
    }

    /* 2. Header Logo exact space reservation */
    .xts-logo img.xts-logo-main {
        width: 250px !important;
        height: 52px !important;
        aspect-ratio: 300 / 62;
        max-width: 100%;
        height: auto;
        display: inline-block;
    }

    /* 3. Product Cards Aspect-Ratio Reservation */
    .xts-product-thumb,
    .xts-product-image {
        aspect-ratio: 1 / 1;
        width: 100%;
        background-color: #f8f8fa;
        display: block;
        overflow: hidden;
    }
    .xts-product-image img {
        aspect-ratio: 1 / 1;
        width: 100%;
        height: 100%;
        object-fit: contain;
    }

    /* 4. Category Thumbnails Aspect-Ratio Reservation */
    .xts-cat-thumbnail,
    .xts-cat-image {
        aspect-ratio: 1 / 1;
        width: 100%;
        background-color: #f8f8fa;
        overflow: hidden;
    }

    /* 5. Single Product Gallery Reservation */
    .woocommerce-product-gallery__wrapper,
    .woocommerce-product-gallery__image {
        aspect-ratio: 1 / 1;
        width: 100%;
        background-color: #ffffff;
    }

    /* 6. Content Visibility: Skip off-screen DOM calculations on initial paint */
    @media (min-width: 768px) {
        .elementor-element.e-parent:nth-child(n+3),
        .xts-footer {
            content-visibility: auto;
            contain-intrinsic-size: 0 600px;
        }
    }
    @media (max-width: 767px) {
        .elementor-element.e-parent:nth-child(n+2),
        .xts-footer {
            content-visibility: auto;
            contain-intrinsic-size: 0 450px;
        }
    }

    /* 7. Font display swap enforcement */
    body, button, input, select, textarea, h1, h2, h3, h4, h5, h6, .xts-entities-title {
        font-display: swap !important;
    }
    </style>
    <?php
}, 2);

/* ==========================================================================
   4. LCP IMAGE UN-LAZYLOAD & LOGO SIZING TRANSFORMER
   ========================================================================== */
add_action('template_redirect', function () {
    if (is_admin() || wp_doing_ajax() || (defined('REST_REQUEST') && REST_REQUEST)) {
        return;
    }

    ob_start(function ($html) {
        if (strlen($html) < 500) {
            return $html;
        }

        // 4.1. Un-lazyload Hero Banner on Front Page
        if (is_front_page()) {
            $html = preg_replace_callback(
                '/<img\\b([^>]*clover-home-appliances-october-sale-banner[^>]*)>/i',
                function ($match) {
                    $tag = $match[0];
                    // Extract data-xts-src
                    if (preg_match('/data-xts-src=[\'"]([^\'"]+)[\'"]/i', $tag, $src_m)) {
                        $real_src = $src_m[1];
                        $tag = preg_replace('/src=[\'"][^\'"]*[\'"]/i', 'src="' . $real_src . '"', $tag);
                    }
                    // Extract data-srcset
                    if (preg_match('/data-srcset=[\'"]([^\'"]+)[\'"]/i', $tag, $srcset_m)) {
                        $real_srcset = $srcset_m[1];
                        $tag = preg_replace('/srcset=[\'"][^\'"]*[\'"]/i', 'srcset="' . $real_srcset . '"', $tag);
                    }
                    // Replace loading="lazy" with eager
                    $tag = preg_replace('/loading=[\'"]lazy[\'"]/i', 'loading="eager" fetchpriority="high"', $tag);
                    if (strpos($tag, 'fetchpriority') === false) {
                        $tag = preg_replace('/<img\\s+/i', '<img fetchpriority="high" ', $tag);
                    }
                    // Remove lazy classes
                    $tag = str_replace(['xts-lazy-load', 'xts-lazy-fade'], '', $tag);
                    return $tag;
                },
                $html
            );

            // 4.2. Logo sizing and un-lazyload
            $html = preg_replace_callback(
                '/<img\\b([^>]*class=[\'"][^\'"]*xts-logo-main[^\'"]*[\'"][^>]*)>/i',
                function ($match) {
                    $tag = $match[0];
                    if (strpos($tag, 'width=') === false) {
                        $tag = preg_replace('/<img\\s+/i', '<img width="250" height="52" fetchpriority="high" ', $tag);
                    }
                    if (preg_match('/data-src=[\'"]([^\'"]+)[\'"]/i', $tag, $src_m)) {
                        $real_src = $src_m[1];
                        $tag = preg_replace('/src=[\'"][^\'"]*[\'"]/i', 'src="' . $real_src . '"', $tag);
                        $tag = preg_replace('/data-lazyloaded=[\'"][^\'"]*[\'"]/i', '', $tag);
                    }
                    return $tag;
                },
                $html,
                1
            );
        }

        // 4.3. Single Product Main Image Eager Loading
        if (function_exists('is_product') && is_product()) {
            $html = preg_replace_callback(
                '/<img\\b([^>]*wp-post-image[^>]*)>/i',
                function ($match) {
                    $tag = $match[0];
                    $tag = preg_replace('/loading=[\'"]lazy[\'"]/i', 'loading="eager" fetchpriority="high"', $tag);
                    if (strpos($tag, 'fetchpriority') === false) {
                        $tag = preg_replace('/<img\\s+/i', '<img fetchpriority="high" ', $tag);
                    }
                    return $tag;
                },
                $html,
                1
            );
        }

        return $html;
    });
}, 2);

/* ==========================================================================
   5. AUTOMATIC CACHE PURGE HOOKS
   ========================================================================== */
function hk_purge_page_cache($post_id = null) {
    $dir = WP_CONTENT_DIR . '/cache/hk_fastcache';
    if (!is_dir($dir)) return;
    
    if ($post_id) {
        $url = get_permalink($post_id);
        if ($url) {
            $parsed = parse_url($url);
            $key = md5(($parsed['host'] ?? 'hosseinykala.ir') . ($parsed['path'] ?? '/'));
            @unlink("$dir/$key.html");
            @unlink("$dir/$key.html.gz");
        }
    }
    
    // Always purge homepage on content change
    $home_key = md5('hosseinykala.ir/');
    @unlink("$dir/$home_key.html");
    @unlink("$dir/$home_key.html.gz");
}

add_action('save_post', 'hk_purge_page_cache');
add_action('edit_post', 'hk_purge_page_cache');
add_action('woocommerce_update_product', 'hk_purge_page_cache');
add_action('clean_post_cache', 'hk_purge_page_cache');

/* ==========================================================================
   6. CONDITIONAL ASSET LOADING & DEQUEUING BLOAT
   ========================================================================== */
add_action('wp_enqueue_scripts', function () {
    // 6.1. Disable Contact Form 7 assets on pages without forms
    if (!is_admin()) {
        global $post;
        $has_form = false;
        if (is_a($post, 'WP_Post') && has_shortcode($post->post_content, 'contact-form-7')) {
            $has_form = true;
        }
        if (!$has_form) {
            wp_dequeue_script('contact-form-7');
            wp_dequeue_style('contact-form-7');
        }
    }

    // 6.2. Dequeue Dashicons on frontend for logged-out visitors
    if (!is_user_logged_in()) {
        wp_deregister_style('dashicons');
    }
}, 999);

/* ==========================================================================
   7. DISABLE CORE EMOJIS (Removes render-blocking JS & inline styles)
   ========================================================================== */
add_action('init', function () {
    remove_action('wp_head', 'print_emoji_detection_script', 7);
    remove_action('admin_print_scripts', 'print_emoji_detection_script');
    remove_action('wp_print_styles', 'print_emoji_styles');
    remove_action('admin_print_styles', 'print_emoji_styles');
    remove_filter('the_content_feed', 'wp_staticize_emoji');
    remove_filter('comment_text_rss', 'wp_staticize_emoji');
    remove_filter('wp_mail', 'wp_staticize_emoji_for_email');
});

/* ==========================================================================
   8. HEARTBEAT API CONTROL (Reduces background server polling)
   ========================================================================== */
add_filter('heartbeat_settings', function ($settings) {
    if (!is_admin()) {
        $settings['interval'] = 120; // 2 minutes on frontend
    }
    return $settings;
});
"""

r_up = requests.post(url, cookies=cookies, data={
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': '00-hosseinykala-perf-core.php',
    'text': perf_core_v25
}, verify=False)
print("Uploaded 00-hosseinykala-perf-core.php v2.5.0:", r_up.status_code)

# Clear hk_fastcache directory to regenerate fresh static pages with LCP optimizations
php_clear_cache = """<?php
add_action('init', function() {
    $dir = WP_CONTENT_DIR . '/cache/hk_fastcache';
    $count = 0;
    if (is_dir($dir)) {
        $files = glob($dir . '/*');
        foreach ($files as $f) {
            if (is_file($f)) {
                @unlink($f);
                $count++;
            }
        }
    }
    echo json_encode(['purged_cache_files' => $count]);
    exit;
}, 1);
"""

requests.post(url, cookies=cookies, data={
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'temp_clear_cache.php',
    'text': php_clear_cache
}, verify=False)

r_clear = requests.get('https://hosseinykala.ir/?clear_cache=1', headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
print("Purged old static cache files:", r_clear.text)

requests.post('https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER', cookies=cookies, data={
    'action': 'multiple',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'select0': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins/temp_clear_cache.php',
    'button': 'delete'
}, verify=False)
print("Deployment complete.")
