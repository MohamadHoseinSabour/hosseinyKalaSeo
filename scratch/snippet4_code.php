/**
 * HK Performance API Endpoint - Full Purge & Settings & Diagnostics & Fixes
 */
add_action('rest_api_init', function () {
    register_rest_route('hk-perf/v1', '/get-diagnostics', [
        'methods' => 'GET',
        'permission_callback' => '__return_true',
        'callback' => function () {
            $ht_path = ABSPATH . '.htaccess';
            return [
                'perfmatters' => get_option('perfmatters_options'),
                'lscache_conf' => class_exists('LiteSpeed\Conf') ? LiteSpeed\Conf::get_instance()->get_options() : null,
                'active_plugins' => get_option('active_plugins'),
                'htaccess_exists' => file_exists($ht_path),
                'htaccess_writable' => is_writable($ht_path),
                'htaccess_size' => file_exists($ht_path) ? filesize($ht_path) : 0,
            ];
        }
    ]);

    register_rest_route('hk-perf/v1', '/inspect-htaccess', [
        'methods' => 'GET',
        'permission_callback' => '__return_true',
        'callback' => function () {
            $ht_path = ABSPATH . '.htaccess';
            if (!file_exists($ht_path)) {
                return ['success' => false, 'error' => 'Not found'];
            }
            return [
                'success' => true,
                'writable' => is_writable($ht_path),
                'content' => file_get_contents($ht_path)
            ];
        }
    ]);

    register_rest_route('hk-perf/v1', '/fix-htaccess-ttl', [
        'methods' => 'POST',
        'permission_callback' => '__return_true',
        'callback' => function () {
            $ht_path = ABSPATH . '.htaccess';
            if (!file_exists($ht_path) || !is_writable($ht_path)) {
                return ['success' => false, 'error' => 'File not writable'];
            }
            $content = file_get_contents($ht_path);
            
            // Backup
            @file_put_contents($ht_path . '.bak_perf_' . date('Ymd_His'), $content);
            
            // Fix overflow value 3155760000 -> 31536000 (1 year standard)
            $new_content = str_replace('3155760000', '31536000', $content);
            
            // Ensure mod_headers sets immutable cache-control for static assets
            $header_block = "\n# BEGIN HK_STATIC_CACHE_LIFETIME\n<IfModule mod_headers.c>\n" .
                "  <FilesMatch \"\.(ico|pdf|flv|jpg|jpeg|png|gif|webp|avif|swf|svg|woff|woff2|ttf|otf|eot)(\.gz)?$\">\n" .
                "    Header set Cache-Control \"max-age=31536000, public, immutable\"\n" .
                "    Header set Access-Control-Allow-Origin \"*\"\n" .
                "  </FilesMatch>\n" .
                "  <FilesMatch \"\.(css|js)(\.gz)?$\">\n" .
                "    Header set Cache-Control \"max-age=31536000, public, immutable\"\n" .
                "  </FilesMatch>\n" .
                "</IfModule>\n# END HK_STATIC_CACHE_LIFETIME\n";
            
            if (strpos($new_content, 'HK_STATIC_CACHE_LIFETIME') === false) {
                // Insert after mod_expires block
                if (strpos($new_content, '### marker BROWSER CACHE end ###') !== false) {
                    $new_content = str_replace(
                        '### marker BROWSER CACHE end ###',
                        "### marker BROWSER CACHE end ###\n" . $header_block,
                        $new_content
                    );
                } else {
                    $new_content = $header_block . "\n" . $new_content;
                }
            }
            
            $written = file_put_contents($ht_path, $new_content);
            return [
                'success' => $written !== false,
                'bytes_written' => $written
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
