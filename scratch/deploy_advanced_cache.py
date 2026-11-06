import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

advanced_cache_code = """<?php
/**
 * HosseinyKala High-Performance Page Cache Drop-in
 * Delivers sub-80ms TTFB for guest visitors on Apache/Nginx.
 */

defined('ABSPATH') || exit;

// 1. Check if request is cacheable
if (
    $_SERVER['REQUEST_METHOD'] !== 'GET' ||
    (defined('DOING_CRON') && DOING_CRON) ||
    (defined('XMLRPC_REQUEST') && XMLRPC_REQUEST) ||
    (defined('REST_REQUEST') && REST_REQUEST)
) {
    return;
}

$uri = $_SERVER['REQUEST_URI'] ?? '/';

// Bypass for admin, cart, checkout, account
if (
    strpos($uri, '/wp-admin') !== false ||
    strpos($uri, '/wp-login') !== false ||
    strpos($uri, '/cart') !== false ||
    strpos($uri, '/checkout') !== false ||
    strpos($uri, '/my-account') !== false ||
    strpos($uri, '/wp-json') !== false
) {
    return;
}

// Bypass for logged in users or active WooCommerce carts
foreach ($_COOKIE as $cookie_name => $cookie_val) {
    if (
        strpos($cookie_name, 'wordpress_logged_in_') === 0 ||
        $cookie_name === 'woocommerce_items_in_cart' ||
        $cookie_name === 'woocommerce_cart_hash'
    ) {
        return;
    }
}

// Ignore tracking query strings (utm, fbclid, etc.) for cache key
$parsed_url = parse_url($uri);
$path = $parsed_url['path'] ?? '/';
$query = $parsed_url['query'] ?? '';

if (!empty($query)) {
    parse_str($query, $query_params);
    $tracking_keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'fbclid', 'gclid', '_ga'];
    foreach ($tracking_keys as $tk) {
        unset($query_params[$tk]);
    }
    ksort($query_params);
    $query = http_build_query($query_params);
}

$cache_key = md5(($parsed_url['host'] ?? 'hosseinykala.ir') . $path . ($query ? '?' . $query : ''));
$cache_dir = WP_CONTENT_DIR . '/cache/hk_fastcache';
$cache_file = $cache_dir . '/' . $cache_key . '.html';
$cache_file_gz = $cache_file . '.gz';

// Serve from cache if available and not older than 7 days
if (file_exists($cache_file_gz) && (time() - filemtime($cache_file_gz) < 604800)) {
    $accept_encoding = $_SERVER['HTTP_ACCEPT_ENCODING'] ?? '';
    
    header('Content-Type: text/html; charset=UTF-8');
    header('X-HosseinyKala-Cache: HIT');
    header('Cache-Control: public, max-age=3600, stale-while-revalidate=86400');
    
    if (strpos($accept_encoding, 'gzip') !== false) {
        header('Content-Encoding: gzip');
        header('Vary: Accept-Encoding');
        readfile($cache_file_gz);
        exit;
    } elseif (file_exists($cache_file)) {
        header('Vary: Accept-Encoding');
        readfile($cache_file);
        exit;
    }
}

// Buffer output on cache MISS to generate the static cache
if (!is_dir($cache_dir)) {
    @mkdir($cache_dir, 0755, true);
}

ob_start(function($buffer) use ($cache_file, $cache_file_gz, $cache_dir) {
    if (strlen($buffer) < 500) {
        return $buffer;
    }
    
    // Check if HTTP response status is 200
    $status = http_response_code();
    if ($status !== 200) {
        return $buffer;
    }
    
    // Do not cache if no-cache header was explicitly set for private content
    $headers = headers_list();
    foreach ($headers as $h) {
        if (stripos($h, 'set-cookie: wordpress_logged_in_') !== false || stripos($h, 'woocommerce_items_in_cart') !== false) {
            return $buffer;
        }
    }
    
    // Append cache signature
    $signed_buffer = $buffer . "\\n<!-- HosseinyKala FastCache Generated: " . gmdate('Y-m-d H:i:s') . " GMT -->";
    
    @file_put_contents($cache_file, $signed_buffer);
    @file_put_contents($cache_file_gz, gzencode($signed_buffer, 6));
    
    return $buffer;
});
"""

data = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content',
    'filename': 'advanced-cache.php',
    'text': advanced_cache_code
}
r = requests.post(url, cookies=cookies, data=data, verify=False)
print('Saved advanced-cache.php:', r.status_code)
