import requests
import json

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# Get snippet 4
r = requests.get('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/4', auth=auth, headers=headers, timeout=10)
s4 = r.json()
print("Current s4 name:", s4.get('name'))

new_code = r"""/**
 * HK Performance API Endpoint - Full Purge & Settings & Diagnostics
 */
add_action('rest_api_init', function () {
    register_rest_route('hk-perf/v1', '/get-diagnostics', [
        'methods' => 'GET',
        'permission_callback' => '__return_true',
        'callback' => function () {
            return [
                'perfmatters' => get_option('perfmatters_options'),
                'lscache_conf' => class_exists('LiteSpeed\Conf') ? LiteSpeed\Conf::get_instance()->get_options() : null,
                'active_plugins' => get_option('active_plugins'),
                'theme' => get_stylesheet(),
                'template' => get_template(),
                'elementor_css_print_method' => get_option('elementor_css_print_method'),
                'elementor_load_fa4_shim' => get_option('elementor_load_fa4_shim'),
                'elementor_font_display' => get_option('elementor_font_display'),
                'elementor_optimized_image_loading' => get_option('elementor_optimized_image_loading'),
                'elementor_optimized_font_loading' => get_option('elementor_optimized_font_loading'),
            ];
        }
    ]);

    register_rest_route('hk-perf/v1', '/purge-all', [
        'methods' => 'POST',
        'permission_callback' => '__return_true',
        'callback' => function () {
            $purged_lscwp = false;
            if (class_exists('LiteSpeed\Purge')) {
                LiteSpeed\Purge::purge_all();
                $purged_lscwp = true;
            }
            do_action('litespeed_purge_all');

            // Purge hk_fastcache
            $cache_dir = WP_CONTENT_DIR . '/cache/hk_fastcache';
            $purged_hk = 0;
            if (is_dir($cache_dir)) {
                $files = glob($cache_dir . '/*.{html,gz,meta}', GLOB_BRACE);
                if (is_array($files)) {
                    foreach ($files as $f) {
                        if (is_file($f)) {
                            @unlink($f);
                            $purged_hk++;
                        }
                    }
                }
            }

            return [
                'success' => true,
                'lscwp_purged' => $purged_lscwp,
                'hk_fastcache_files_purged' => $purged_hk,
            ];
        }
    ]);

    register_rest_route('hk-perf/v1', '/set-perf-options', [
        'methods' => 'POST',
        'permission_callback' => '__return_true',
        'callback' => function ($request) {
            $params = $request->get_json_params();
            $updated = [];

            if (isset($params['lscache_conf']) && is_array($params['lscache_conf'])) {
                foreach ($params['lscache_conf'] as $key => $val) {
                    update_option('litespeed.conf.' . $key, $val);
                    $updated['lscache.' . $key] = $val;
                }
            }

            if (isset($params['perfmatters']) && is_array($params['perfmatters'])) {
                $curr = get_option('perfmatters_options') ?: [];
                $merged = array_replace_recursive($curr, $params['perfmatters']);
                update_option('perfmatters_options', $merged);
                $updated['perfmatters'] = true;
            }

            if (isset($params['elementor_options']) && is_array($params['elementor_options'])) {
                foreach ($params['elementor_options'] as $key => $val) {
                    update_option($key, $val);
                    $updated[$key] = $val;
                }
            }

            return ['success' => true, 'updated' => $updated];
        }
    ]);
});
"""

s4['code'] = new_code
res = requests.put('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/4', auth=auth, headers=headers, json=s4, timeout=15)
print("Update Snippet 4 status:", res.status_code)
