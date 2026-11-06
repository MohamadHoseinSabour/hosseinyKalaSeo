import requests
import urllib3
import json
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

# Ephemeral cleanup script that runs on init, outputs JSON, and deletes itself
php_cleanup = """<?php
add_action('init', function() {
    if (!isset($_GET['hk_do_db_clean']) || $_GET['hk_do_db_clean'] !== '489c72a81f33') {
        return;
    }
    
    global $wpdb;
    
    $stats = [];
    
    // 1. Expired Transients
    $now = time();
    $sql_trans = "
        DELETE a, b FROM {$wpdb->options} a, {$wpdb->options} b 
        WHERE a.option_name LIKE '_transient_%' 
        AND a.option_name NOT LIKE '_transient_timeout_%' 
        AND b.option_name = CONCAT('_transient_timeout_', SUBSTRING(a.option_name, 12)) 
        AND b.option_value < {$now}
    ";
    $cleaned_transients = $wpdb->query($sql_trans);
    $cleaned_trans_timeouts = $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_timeout_%' AND option_value < {$now}");
    $stats['expired_transients_cleaned'] = ($cleaned_transients ?: 0) + ($cleaned_trans_timeouts ?: 0);
    
    // 2. Action Scheduler completed actions older than 14 days
    if ($wpdb->get_var("SHOW TABLES LIKE '{$wpdb->prefix}actionscheduler_actions'")) {
        $fourteen_days_ago = date('Y-m-d H:i:s', strtotime('-14 days'));
        
        // Find action IDs to clean
        $action_ids = $wpdb->get_col($wpdb->prepare("
            SELECT action_id FROM {$wpdb->prefix}actionscheduler_actions 
            WHERE status IN ('complete', 'canceled', 'failed') 
            AND scheduled_date_gmt < %s
            LIMIT 5000
        ", $fourteen_days_ago));
        
        if (!empty($action_ids)) {
            $ids_placeholder = implode(',', array_map('intval', $action_ids));
            $wpdb->query("DELETE FROM {$wpdb->prefix}actionscheduler_logs WHERE action_id IN ($ids_placeholder)");
            $wpdb->query("DELETE FROM {$wpdb->prefix}actionscheduler_actions WHERE action_id IN ($ids_placeholder)");
            $stats['action_scheduler_cleaned'] = count($action_ids);
        } else {
            $stats['action_scheduler_cleaned'] = 0;
        }
    }
    
    // 3. Post revisions trimming: Keep max 5 revisions per post
    $posts_with_revisions = $wpdb->get_col("
        SELECT post_parent FROM {$wpdb->posts} 
        WHERE post_type = 'revision' 
        GROUP BY post_parent 
        HAVING COUNT(*) > 5
    ");
    
    $deleted_revisions = 0;
    foreach ($posts_with_revisions as $parent_id) {
        $rev_ids_to_keep = $wpdb->get_col($wpdb->prepare("
            SELECT ID FROM {$wpdb->posts} 
            WHERE post_type = 'revision' AND post_parent = %d 
            ORDER BY post_date DESC 
            LIMIT 5
        ", $parent_id));
        
        if (!empty($rev_ids_to_keep)) {
            $keep_str = implode(',', array_map('intval', $rev_ids_to_keep));
            $del_rev_ids = $wpdb->get_col($wpdb->prepare("
                SELECT ID FROM {$wpdb->posts} 
                WHERE post_type = 'revision' AND post_parent = %d 
                AND ID NOT IN ($keep_str)
            ", $parent_id));
            
            if (!empty($del_rev_ids)) {
                $del_str = implode(',', array_map('intval', $del_rev_ids));
                $wpdb->query("DELETE FROM {$wpdb->posts} WHERE ID IN ($del_str)");
                $wpdb->query("DELETE FROM {$wpdb->postmeta} WHERE post_id IN ($del_str)");
                $deleted_revisions += count($del_rev_ids);
            }
        }
    }
    $stats['trimmed_excess_revisions'] = $deleted_revisions;
    
    // 4. Orphan Postmeta
    $orphan_pm = $wpdb->query("
        DELETE pm FROM {$wpdb->postmeta} pm 
        LEFT JOIN {$wpdb->posts} p ON p.ID = pm.post_id 
        WHERE p.ID IS NULL
    ");
    $stats['orphan_postmeta_cleaned'] = $orphan_pm ?: 0;
    
    // 5. Autoload analysis
    $autoload_stats = $wpdb->get_row("
        SELECT COUNT(*) as count, round(SUM(LENGTH(option_value))/1024, 2) as size_kb 
        FROM {$wpdb->options} 
        WHERE autoload = 'yes' OR autoload = 'on'
    ");
    $stats['current_autoload_count'] = (int) $autoload_stats->count;
    $stats['current_autoload_kb'] = (float) $autoload_stats->size_kb;
    
    header('Content-Type: application/json');
    echo json_encode($stats, JSON_PRETTY_PRINT);
    exit;
}, 1);
"""

# Upload to mu-plugins temporarily
r_up = requests.post(url, cookies=cookies, data={
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'temp_db_cleaner.php',
    'text': php_cleanup
}, verify=False)
print("Uploaded temp_db_cleaner.php:", r_up.status_code)

# Trigger cleanup
r_trig = requests.get('https://hosseinykala.ir/?hk_do_db_clean=489c72a81f33', verify=False)
print("Trigger status:", r_trig.status_code)
print("Stats response:\n", r_trig.text)

# Immediately delete the cleaner
r_del = requests.post('https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER', cookies=cookies, data={
    'action': 'multiple',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'select0': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins/temp_db_cleaner.php',
    'button': 'delete'
}, verify=False)
print("Deleted cleaner:", r_del.status_code)
