import urllib.request
import base64
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

creds = base64.b64encode(b'agent:Mlwg pHHX NQ64 drrz 7ca2 IVto').decode('utf-8')
headers = {
    'Authorization': 'Basic ' + creds,
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}

php_code = r'''/**
 * HK Advanced SEO & Meta Architecture Engine (Phase 1)
 * Author: Hosseiny Kala SEO Team
 */

// 1. SITEMAP & NOINDEX FOR XTS-TEMPLATE
// 1.1. Official Rank Math filter to exclude post type
add_filter('rank_math/sitemap/exclude_post_type', function ($exclude, $type) {
    if ($type === 'xts-template' || $type === 'xts_template') {
        return true;
    }
    return $exclude;
}, 10, 2);

// 1.2. Also hook post_types filter
add_filter('rank_math/sitemap/post_types', function ($post_types) {
    if (is_array($post_types)) {
        unset($post_types['xts-template']);
        unset($post_types['xts_template']);
    }
    return $post_types;
}, 99);

// 1.3. Direct XML text filter as ultimate guarantee
add_filter('rank_math/sitemap/xml_text', function ($xml) {
    if (is_string($xml) && strpos($xml, 'xts-template') !== false) {
        $xml = preg_replace('/<sitemap>\s*<loc>[^<]*xts-template[^<]*<\/loc>.*?<\/sitemap>/is', '', $xml);
    }
    return $xml;
}, 99);

add_action('init', function () {
    // Rank Math sitemap cache invalidation
    if (isset($_GET['flush_rm_sitemap'])) {
        if (class_exists('\RankMath\Sitemap\Cache')) {
            \RankMath\Sitemap\Cache::invalidate_storage();
        }
        delete_transient('rank_math_sitemap_index');
        delete_transient('rank_math_sitemap_xts-template');
        global $wpdb;
        $wpdb->query("DELETE FROM $wpdb->options WHERE option_name LIKE '%rank_math_sitemap_%'");
        $wpdb->query("DELETE FROM $wpdb->options WHERE option_name LIKE '%transient_rank_math_%'");
        echo "Rank Math sitemap storage invalidated";
        exit;
    }

    // Block direct access to xts-template-sitemap.xml
    if (isset($_SERVER['REQUEST_URI']) && strpos($_SERVER['REQUEST_URI'], 'xts-template-sitemap.xml') !== false) {
        status_header(404);
        nocache_headers();
        header('Content-Type: text/xml; charset=utf-8');
        echo '<?xml version="1.0" encoding="UTF-8"?><error>404 Not Found</error>';
        exit;
    }
}, 1);

add_filter('rank_math/frontend/robots', function ($robots) {
    if (is_singular('xts-template') || get_query_var('xts-template') || (isset($_GET['xts-template']))) {
        $robots['index'] = 'noindex';
        $robots['follow'] = 'nofollow';
    }
    return $robots;
}, 99);

// 2. CATEGORY META DESCRIPTION OPTIMIZATION (Fix 2,739 chars bloat)
add_filter('rank_math/frontend/description', function ($description) {
    if (is_product_category() || is_tax('product_cat') || is_category()) {
        $term = get_queried_object();
        $custom_descs = [
            'یخچال-فریزر' => 'خرید انواع یخچال فریزر دوقلو، ساید و کمبی از برندهای کلور، دیپوینت و ایستکول با تضمین اصالت و امکان خرید اقساطی در اهواز با ارسال سریع از حسینی کالا.',
            'refrigerator-freezer' => 'خرید انواع یخچال فریزر دوقلو، ساید و کمبی از برندهای کلور، دیپوینت و ایستکول با تضمین اصالت و امکان خرید اقساطی در اهواز با ارسال سریع از حسینی کالا.',
            'washing-machine' => 'خرید انواع ماشین لباسشویی ایرانی و خارجی با گارانتی معتبر شرکتی. شرایط ویژه خرید نقد و اقساطی در اهواز و ارسال سریع به سراسر کشور از حسینی کالا.',
            'ماشین-لباسشویی' => 'خرید انواع ماشین لباسشویی ایرانی و خارجی با گارانتی معتبر شرکتی. شرایط ویژه خرید نقد و اقساطی در اهواز و ارسال سریع به سراسر کشور از حسینی کالا.',
            'dishwasher' => 'بررسی و خرید انواع ماشین ظرفشویی رومیزی و مبله با بهترین قیمت بازار و ضمانت اصالت فیزیکی. امکان خرید اقساطی در اهواز با ارسال سریع از حسینی کالا.',
            'ماشین-ظرفشویی' => 'بررسی و خرید انواع ماشین ظرفشویی رومیزی و مبله با بهترین قیمت بازار و ضمانت اصالت فیزیکی. امکان خرید اقساطی در اهواز با ارسال سریع از حسینی کالا.',
            'air-cooler' => 'خرید آنلاین و اقساطی انواع کولر آبی پرقدرت متناسب با آب‌وهوای گرمسیری با بهترین قیمت و گارانتی معتبر شرکتی در فروشگاه لوازم خانگی حسینی اهواز.',
            'کولر-آبی' => 'خرید آنلاین و اقساطی انواع کولر آبی پرقدرت متناسب با آب‌وهوای گرمسیری با بهترین قیمت و گارانتی معتبر شرکتی در فروشگاه لوازم خانگی حسینی اهواز.',
            'vacuum-cleaner' => 'خرید انواع جاروبرقی کیسه‌ای، مخزنی و سطلی با مکش قدرتمند و گارانتی شرکتی. خرید نقد و اقساطی در اهواز و ارسال مطمئن به سراسر ایران از حسینی کالا.',
            'جاروبرقی' => 'خرید انواع جاروبرقی کیسه‌ای، مخزنی و سطلی با مکش قدرتمند و گارانتی شرکتی. خرید نقد و اقساطی در اهواز و ارسال مطمئن به سراسر ایران از حسینی کالا.',
            'water-purifier' => 'خرید انواع دستگاه تصفیه آب خانگی چند مرحله‌ای با فیلترهای استاندارد و تضمین سلامت آب. شرایط خرید اقساطی در اهواز با ارسال سریع از حسینی کالا.',
            'تصفیه-کننده-آب' => 'خرید انواع دستگاه تصفیه آب خانگی چند مرحله‌ای با فیلترهای استاندارد و تضمین سلامت آب. شرایط خرید اقساطی در اهواز با ارسال سریع از حسینی کالا.',
        ];

        if ($term && isset($term->slug)) {
            $slug_decoded = urldecode($term->slug);
            if (isset($custom_descs[$slug_decoded])) {
                return $custom_descs[$slug_decoded];
            }
            if (isset($custom_descs[$term->slug])) {
                return $custom_descs[$term->slug];
            }
        }

        if (empty($description) || mb_strlen($description, 'UTF-8') > 165) {
            if ($term && !empty($term->description)) {
                $clean = wp_strip_all_tags($term->description);
                $clean = preg_replace('/\s+/', ' ', trim($clean));
                if (mb_strlen($clean, 'UTF-8') > 155) {
                    return mb_substr($clean, 0, 152, 'UTF-8') . '...';
                }
                return $clean;
            }
        }
    }
    return $description;
}, 99);

// 3. ENFORCE HTTPS ON INTERNAL LINKS & FIX H1 IN OUTPUT
add_action('template_redirect', function () {
    if (is_admin() || wp_doing_ajax() || (defined('REST_REQUEST') && REST_REQUEST)) {
        return;
    }

    ob_start(function ($buffer) {
        if (empty($buffer) || strlen($buffer) < 200) {
            return $buffer;
        }

        // 3.1. Enforce HTTPS on all internal links
        $buffer = str_replace('http://hosseinykala.ir/', 'https://hosseinykala.ir/', $buffer);
        $buffer = str_replace('http://www.hosseinykala.ir/', 'https://hosseinykala.ir/', $buffer);
        $buffer = str_replace('http:\/\/hosseinykala.ir\/', 'https:\/\/hosseinykala.ir\/', $buffer);

        // 3.2. Single Post Title: Replace <h3 ...> with <h1 ...>
        if (is_singular('post')) {
            $buffer = preg_replace(
                '/<h3([^>]*class=["\'][^"\']*xts-title[^"\']*["\'][^>]*)>(.*?)<\/h3>/is',
                '<h1$1 class="xts-title title entry-title">$2</h1>',
                $buffer,
                1
            );
        }

        // 3.3. Homepage H1 Injection (if no H1 exists)
        if ((is_front_page() || is_home()) && stripos($buffer, '<h1') === false) {
            $h1_tag = '<h1 class="xts-screen-reader-text" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">فروشگاه لوازم خانگی حسینی کالا اهواز | خرید نقد و اقساطی</h1>';
            if (stripos($buffer, '<div id="main-content"') !== false) {
                $buffer = preg_replace('/(<div id="main-content"[^>]*>)/i', '$1' . $h1_tag, $buffer, 1);
            } elseif (stripos($buffer, '<main') !== false) {
                $buffer = preg_replace('/(<main[^>]*>)/i', '$1' . $h1_tag, $buffer, 1);
            } elseif (stripos($buffer, '<body') !== false) {
                $buffer = preg_replace('/(<body[^>]*>)/i', '$1' . $h1_tag, $buffer, 1);
            }
        }

        // 3.4. Product Category Archive H1 Injection (if no H1 exists)
        if ((is_product_category() || is_tax('product_cat')) && stripos($buffer, '<h1') === false) {
            $term = get_queried_object();
            $title_text = ($term && isset($term->name)) ? esc_html($term->name) : 'محصولات فروشگاه حسینی کالا';
            $h1_tag = '<h1 class="xts-screen-reader-text" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">خرید و قیمت ' . $title_text . ' - حسینی کالا اهواز</h1>';
            if (stripos($buffer, '<div id="main-content"') !== false) {
                $buffer = preg_replace('/(<div id="main-content"[^>]*>)/i', '$1' . $h1_tag, $buffer, 1);
            } elseif (stripos($buffer, '<main') !== false) {
                $buffer = preg_replace('/(<main[^>]*>)/i', '$1' . $h1_tag, $buffer, 1);
            } elseif (stripos($buffer, '<body') !== false) {
                $buffer = preg_replace('/(<body[^>]*>)/i', '$1' . $h1_tag, $buffer, 1);
            }
        }

        return $buffer;
    });
}, 1);
'''

payload = {
    'name': 'HK Advanced SEO & Meta Architecture Engine',
    'code': php_code,
    'active': True,
    'scope': 'global'
}

req = urllib.request.Request(
    'https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/7',
    headers=headers,
    data=json.dumps(payload).encode('utf-8'),
    method='POST'
)

with urllib.request.urlopen(req, timeout=15) as resp:
    res = json.loads(resp.read().decode('utf-8'))
    print("Snippet 7 updated! Active:", res.get('active'))

# Trigger flush Rank Math sitemap
try:
    flush_req = urllib.request.Request('https://hosseinykala.ir/?flush_rm_sitemap=1', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(flush_req, timeout=15) as resp:
        print("Sitemap flush:", resp.read().decode('utf-8')[:100])
except Exception as e:
    print("Flush warning:", e)

# Purge caches via hk-perf
try:
    purge_req = urllib.request.Request(
        'https://hosseinykala.ir/wp-json/hk-perf/v1/purge-all',
        headers={'Authorization': 'Basic ' + creds},
        data=b'{}'
    )
    with urllib.request.urlopen(purge_req, timeout=15) as resp:
        print("Purge Cache Response:", resp.read().decode('utf-8'))
except Exception as e:
    print("Purge Cache Warning:", e)
