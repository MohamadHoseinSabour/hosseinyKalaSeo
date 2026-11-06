import urllib.request
import base64
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

creds = base64.b64encode(b'agent:Mlwg pHHX NQ64 drrz 7ca2 IVto').decode('utf-8')

# Read current snippet 5 from API
req = urllib.request.Request('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/5', headers={
    'Authorization': 'Basic ' + creds,
    'User-Agent': 'Mozilla/5.0'
})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode('utf-8'))

code = data.get('code', '')

# Insert the stub right after add_action('wp_head', function () {
target = "add_action('wp_head', function () {\n"
replacement = "add_action('wp_head', function () {\n    // 2.0. Prevent third-party / inline scripts throwing 'wp is not defined' before core i18n bundle loads\n    echo '<script id=\"hk-wp-i18n-stub\">window.wp=window.wp||{};window.wp.i18n=window.wp.i18n||{setLocaleData:function(d,n){window._wp_loc=window._wp_loc||{};window._wp_loc[n||\\'default\\']=d;},__:function(t){return t;},_x:function(t){return t;},_n:function(s,p,n){return n===1?s:p;},_nx:function(s,p,n){return n===1?s:p;},isRtl:function(){return true;},sprintf:function(){return arguments[0]||\"\";}};</script>' . \"\\n\";\n"

if 'hk-wp-i18n-stub' not in code:
    if target in code:
        code = code.replace(target, replacement, 1)
    else:
        # try CRLF
        target_crlf = "add_action('wp_head', function () {\r\n"
        code = code.replace(target_crlf, replacement, 1)

# Push back to Snippet 5
update_payload = json.dumps({'code': code}).encode('utf-8')
update_req = urllib.request.Request(
    'https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/5',
    headers={
        'Authorization': 'Basic ' + creds,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    },
    data=update_payload,
    method='POST'
)

with urllib.request.urlopen(update_req, timeout=15) as resp:
    res = json.loads(resp.read().decode('utf-8'))
    print("Snippet 5 updated successfully! ID:", res.get('id'), "Active:", res.get('active'))

# Purge caches
purge_req = urllib.request.Request(
    'https://hosseinykala.ir/wp-json/hk-perf/v1/purge-all',
    headers={'Authorization': 'Basic ' + creds},
    data=b'{}'
)
with urllib.request.urlopen(purge_req, timeout=15) as resp:
    print("Purge response:", resp.read().decode('utf-8'))
