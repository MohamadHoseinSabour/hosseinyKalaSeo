import requests
import json
import re

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# 1. Fetch current snippet 5
r = requests.get('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/5', auth=auth, headers=headers, timeout=15)
s5 = r.json()
code = s5['code']

# 2. Add priority 1 to template_redirect if not present
# Currently: add_action('template_redirect', function () {
# Replace with: add_action('template_redirect', function () { ... }, 1);
# Look for the closing of template_redirect
# Let's inspect where template_redirect closes:
# Line 301: });

target_open = "add_action('template_redirect', function () {"
if target_open in code:
    print("Found target_open")

# Add the fast redirect logic
fast_redirect_block = """    // 1.2 Fast trailing slash canonical redirect (sub-10ms redirect vs 3.5s slow WordPress bootstrap)
    if (!$bypass_cache) {
        $raw_path = parse_url($uri, PHP_URL_PATH) ?: '/';
        if ($raw_path !== '/' && substr($raw_path, -1) !== '/' && !pathinfo($raw_path, PATHINFO_EXTENSION)) {
            $query_str = parse_url($uri, PHP_URL_QUERY);
            $redirect_url = $raw_path . '/' . ($query_str ? '?' . $query_str : '');
            header('Location: ' . $redirect_url, true, 301);
            header('X-HosseinyKala-Cache: FAST-REDIRECT');
            exit;
        }
    }
"""

if "FAST-REDIRECT" not in code:
    # Insert right after bypass_cache checks (line 48)
    # Target anchor: $cache_dir = WP_CONTENT_DIR . '/cache/hk_fastcache';
    anchor = "$cache_dir = WP_CONTENT_DIR . '/cache/hk_fastcache';"
    if anchor in code:
        code = code.replace(anchor, fast_redirect_block + "\n    " + anchor, 1)
        print("Inserted fast_redirect_block before cache_dir")
    else:
        print("Anchor not found!")

# Change closing of template_redirect to priority 1
# Let's check how the action ends:
# It's at the end of the ob_start block:
#     return $html;
# });
# We want:
#     return $html;
# }, 1);
target_close = "    return $html;\n});"
replacement_close = "    return $html;\n}, 1);"

if target_close in code:
    code = code.replace(target_close, replacement_close, 1)
    print("Updated template_redirect priority to 1")
else:
    # Check CRLF
    target_close_crlf = "    return $html;\r\n});"
    if target_close_crlf in code:
        code = code.replace(target_close_crlf, replacement_close, 1)
        print("Updated template_redirect priority to 1 (CRLF)")

s5['code'] = code
res = requests.post('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/5', auth=auth, headers=headers, json={'code': code}, timeout=15)
print("Snippet 5 update status:", res.status_code)

# Purge cache
r_purge = requests.post('https://hosseinykala.ir/wp-json/hk-perf/v1/purge-all', auth=auth, timeout=15)
print("Purge status:", r_purge.status_code, r_purge.json() if r_purge.status_code == 200 else r_purge.text)
