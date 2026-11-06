import requests
import urllib3
import json
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

php_code = """<?php
add_action('init', function() {
    global $wpdb;
    
    // 1. Total Autoload Size & Count
    $total_autoload = $wpdb->get_row("
        SELECT COUNT(*) as count, SUM(LENGTH(option_value)) as size 
        FROM {$wpdb->options} 
        WHERE autoload = 'yes' OR autoload = 'on'
    ");
    
    // 2. Top 20 Largest Autoloaded Options
    $top_autoload = $wpdb->get_results("
        SELECT option_name, LENGTH(option_value) as length, autoload 
        FROM {$wpdb->options} 
        WHERE autoload = 'yes' OR autoload = 'on'
        ORDER BY length DESC 
        LIMIT 25
    ");
    
    // 3. Expired Transients Count & Size
    $now = time();
    $expired_transients = $wpdb->get_row("
        SELECT COUNT(*) as count, SUM(LENGTH(option_value)) as size
        FROM {$wpdb->options}
        WHERE option_name LIKE '_transient_timeout_%'
        AND option_value < $now
    ");
    
    $total_transients = $wpdb->get_row("
        SELECT COUNT(*) as count, SUM(LENGTH(option_value)) as size
        FROM {$wpdb->options}
        WHERE option_name LIKE '_transient_%' OR option_name LIKE '_site_transient_%'
    ");
    
    // 4. Post Revisions Count
    $revisions_count = $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type = 'revision'");
    $auto_drafts_count = $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_status = 'auto-draft'");
    $trash_posts_count = $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_status = 'trash'");
    
    // 5. Orphan Meta
    $orphan_postmeta = $wpdb->get_var("
        SELECT COUNT(*) FROM {$wpdb->postmeta} pm 
        LEFT JOIN {$wpdb->posts} p ON p.ID = pm.post_id 
        WHERE p.ID IS NULL
    ");
    
    // 6. Action Scheduler queue status
    $as_actions = [];
    if ($wpdb->get_var("SHOW TABLES LIKE '{$wpdb->prefix}actionscheduler_actions'")) {
        $as_rows = $wpdb->get_results("SELECT status, COUNT(*) as count FROM {$wpdb->prefix}actionscheduler_actions GROUP BY status");
        foreach ($as_rows as $row) {
            $as_actions[$row->status] = $row->count;
        }
    }
    
    // 7. Table sizes
    $tables = $wpdb->get_results("
        SELECT table_name AS name, 
               round(((data_length + index_length) / 1024 / 1024), 2) AS size_mb,
               table_rows AS rows_count
        FROM information_schema.TABLES 
        WHERE table_schema = DATABASE()
        ORDER BY (data_length + index_length) DESC
        LIMIT 20
    ");
    
    $report = [
        'total_autoload_count' => (int) $total_autoload->count,
        'total_autoload_kb' => round($total_autoload->size / 1024, 2),
        'top_autoload' => $top_autoload,
        'expired_transients_count' => (int) $expired_transients->count,
        'expired_transients_kb' => round(($expired_transients->size ?? 0) / 1024, 2),
        'total_transients_count' => (int) $total_transients->count,
        'total_transients_kb' => round($total_transients->size / 1024, 2),
        'revisions_count' => (int) $revisions_count,
        'auto_drafts_count' => (int) $auto_drafts_count,
        'trash_posts_count' => (int) $trash_posts_count,
        'orphan_postmeta_count' => (int) $orphan_postmeta,
        'action_scheduler_status' => $as_actions,
        'top_tables' => $tables
    ];
    
    file_put_contents(WP_CONTENT_DIR . '/db_audit_report.json', json_encode($report, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
}, 1);
"""

data = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'db_audit.php',
    'text': php_code
}
r = requests.post(url, cookies=cookies, data=data, verify=False)
print('Uploaded db_audit.php:', r.status_code)
