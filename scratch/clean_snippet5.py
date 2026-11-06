import requests
import json

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# 1. Fetch current snippet 5
r = requests.get('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/5', auth=auth, headers=headers, timeout=15)
s5 = r.json()
code = s5['code']

# Remove FAST-REDIRECT block
if "FAST-REDIRECT" in code:
    code = code.replace("""    // 1.2 Fast trailing slash canonical redirect (sub-10ms redirect vs 3.5s slow WordPress bootstrap)
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
""", "")
    print("Removed FAST-REDIRECT block from top")

# Ensure priority is 1
target_open = "add_action('template_redirect', function () {"
if target_open in code:
    print("template_redirect found")

# Push update
s5['code'] = code
res = requests.post('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/5', auth=auth, headers=headers, json={'code': code}, timeout=15)
print("Update status:", res.status_code)
