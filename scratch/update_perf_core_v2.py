import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

perf_core_code = """<?php
/**
 * Plugin Name: Hosseiny Kala - Core Performance Optimization Engine
 * Description: Advanced optimization: Page Cache coordination, PHP Session limiter, Asset Dequeuing, and Core Web Vitals optimization.
 * Version: 2.0.0
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
   3. AUTOMATIC CACHE PURGE HOOKS
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
   4. CONDITIONAL ASSET LOADING & DEQUEUING BLOAT
   ========================================================================== */
add_action('wp_enqueue_scripts', function () {
    // 4.1. Disable Contact Form 7 assets on pages without forms
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

    // 4.2. Dequeue Dashicons on frontend for logged-out visitors
    if (!is_user_logged_in()) {
        wp_deregister_style('dashicons');
    }
}, 999);

/* ==========================================================================
   5. DISABLE CORE EMOJIS (Removes render-blocking JS & inline styles)
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
   6. HEARTBEAT API CONTROL (Reduces background server polling)
   ========================================================================== */
add_filter('heartbeat_settings', function ($settings) {
    if (!is_admin()) {
        $settings['interval'] = 120; // 2 minutes on frontend
    }
    return $settings;
});
"""

data = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': '00-hosseinykala-perf-core.php',
    'text': perf_core_code
}
r = requests.post(url, cookies=cookies, data=data, verify=False)
print('Updated 00-hosseinykala-perf-core.php v2.0.0:', r.status_code)
