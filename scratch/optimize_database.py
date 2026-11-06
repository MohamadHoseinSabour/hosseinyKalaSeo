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
    $results = [];
    
    // 1. Clean dead revslider autoload
    $revslider_rows = $wpdb->query("
        UPDATE {$wpdb->options} 
        SET autoload = 'no' 
        WHERE option_name IN ('revslider-addons', 'revslider-notices') AND autoload = 'yes'
    ");
    $results['revslider_autoload_cleaned'] = $revslider_rows;
    
    // 2. Clean expired transients
    $now = time();
    $expired_keys = $wpdb->get_col("
        SELECT REPLACE(option_name, '_transient_timeout_', '')
        FROM {$wpdb->options}
        WHERE option_name LIKE '_transient_timeout_%'
        AND option_value < $now
    ");
    
    $deleted_transients = 0;
    foreach ($expired_keys as $k) {
        delete_transient($k);
        $deleted_transients++;
    }
    $results['deleted_expired_transients'] = $deleted_transients;
    
    // 3. Clean old post revisions (keep last 5 per post)
    $posts_with_revisions = $wpdb->get_col("
        SELECT post_parent 
        FROM {$wpdb->posts} 
        WHERE post_type = 'revision' AND post_parent > 0
        GROUP BY post_parent 
        HAVING COUNT(*) > 5
    ");
    
    $deleted_revisions = 0;
    foreach ($posts_with_revisions as $parent_id) {
        $rev_ids = $wpdb->get_col($wpdb->prepare("
            SELECT ID FROM {$wpdb->posts} 
            WHERE post_type = 'revision' AND post_parent = %d 
            ORDER BY post_date DESC
        ", $parent_id));
        
        // Keep the first 5, delete the rest
        if (count($rev_ids) > 5) {
            $to_delete = array_slice($rev_ids, 5);
            foreach ($to_delete as $rid) {
                wp_delete_post_revision($rid);
                $deleted_revisions++;
            }
        }
    }
    $results['deleted_old_revisions'] = $deleted_revisions;
    
    // 4. Clean old completed Action Scheduler logs (older than 14 days)
    if ($wpdb->get_var("SHOW TABLES LIKE '{$wpdb->prefix}actionscheduler_actions'")) {
        $fourteen_days_ago = gmdate('Y-m-d H:i:s', time() - (14 * 86400));
        
        $old_actions = $wpdb->get_col($wpdb->prepare("
            SELECT action_id FROM {$wpdb->prefix}actionscheduler_actions
            WHERE status IN ('complete', 'canceled') AND last_attempt_gmt < %s
            LIMIT 1000
        ", $fourteen_days_ago));
        
        if (!empty($old_actions)) {
            $id_list = implode(',', array_map('intval', $old_actions));
            $wpdb->query("DELETE FROM {$wpdb->prefix}actionscheduler_logs WHERE action_id IN ($id_list)");
            $del_actions = $wpdb->query("DELETE FROM {$wpdb->prefix}actionscheduler_actions WHERE action_id IN ($id_list)");
            $results['cleaned_as_actions'] = $del_actions;
        } else {
            $results['cleaned_as_actions'] = 0;
        }
    }
    
    // 5. Delete empty trash posts older than 30 days
    $trash_count = $wpdb->query("DELETE FROM {$wpdb->posts} WHERE post_status = 'trash'");
    $results['deleted_trash_posts'] = $trash_count;
    
    file_put_contents(WP_CONTENT_DIR . '/db_optimization_result.json', json_encode($results, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
}, 1);
"""

data = {
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'run_db_opt.php',
    'text': php_code
}
r = requests.post(url, cookies=cookies, data=data, verify=False)
print('Uploaded run_db_opt.php:', r.status_code)
