import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
/**
 * Plugin Name: Hosseiny Kala - Core Performance Optimization Engine
 * Description: Fixes PHP session cache leakage, enables LiteSpeed page cache for guests, and optimizes frontend assets.
 * Version: 1.0.0
 * Author: Antigravity Performance Engine
 */

defined('ABSPATH') || exit;

// 1. Prevent PHP from sending no-cache headers when session_start() is called by third-party plugins
if (function_exists('session_cache_limiter')) {
    session_cache_limiter('');
}

// 2. Allow LiteSpeed to cache public guest pages
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

    // For public guest pages, if session contains no custom data, allow LiteSpeed Cache
    if (empty($_SESSION)) {
        header_remove('Pragma');
        header_remove('Expires');
        header_remove('Cache-Control');
        
        // Signal LiteSpeed Server Cache to cache this page
        header('X-LiteSpeed-Cache-Control: public, max-age=604800');
        header('Cache-Control: public, max-age=3600, stale-while-revalidate=86400');
        
        // Remove PHPSESSID cookie so LiteSpeed won't bypass cache on subsequent requests
        if (!headers_sent()) {
            setcookie('PHPSESSID', '', time() - 3600, '/');
        }
    }
}, 9999);
"""

data = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': '00-hosseinykala-perf-core.php',
    'text': php_code
}
r = requests.post(url, cookies=cookies, data=data, verify=False)
print('Saved 00-hosseinykala-perf-core.php:', r.status_code)

# Clean up find_session.php
requests.post(url, cookies=cookies, data={'action': 'delete', 'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins', 'select0': 'find_session.php'}, verify=False)
requests.post(url, cookies=cookies, data={'action': 'delete', 'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins', 'select0': 'inspect_litespeed.php'}, verify=False)
requests.post(url, cookies=cookies, data={'action': 'delete', 'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins', 'select0': 'inspect_cacheable.php'}, verify=False)
print('Cleaned up diagnostic plugins.')
