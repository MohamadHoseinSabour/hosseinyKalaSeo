import requests
import urllib3
urllib3.disable_warnings()

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
/**
 * Fix unconditional empty PHP sessions from breaking LiteSpeed Cache
 */

// 1. Tell PHP to NOT send automatic no-cache headers when session_start() is called
if (function_exists('session_cache_limiter')) {
    session_cache_limiter('');
}

// 2. For guests on public pages, if $_SESSION was left empty, clean up headers
add_action('send_headers', function() {
    if (is_admin() || wp_doing_ajax()) return;
    if (is_user_logged_in()) return;
    
    // Check if cart has items
    if (function_exists('WC') && WC()->cart && !WC()->cart->is_empty()) {
        return;
    }
    
    // If session is active but has no data, allow LiteSpeed caching
    if (session_status() === PHP_SESSION_ACTIVE && empty($_SESSION)) {
        header_remove('Pragma');
        header_remove('Expires');
        header_remove('Cache-Control');
        
        // Remove PHPSESSID cookie for guests
        if (!headers_sent()) {
            setcookie(session_name(), '', time() - 3600, '/');
        }
    }
}, 99999);
"""

data = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'find_session.php',
    'text': php_code
}
requests.post(url, cookies=cookies, data=data, verify=False)
