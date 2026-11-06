import requests
import urllib3
import json
import sys
urllib3.disable_warnings()

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cookies = {'session': '4JSQFGWGGQBXS2BZHCGHLXYQJCSGY3IZCD5WHTI'}
url = 'https://server152c.irwebspace.com:2223/CMD_API_FILE_MANAGER'

# Full enhanced code for Snippet 6
snippet_6_code = r"""/**
 * HosseinyKala - Server-side Accessibility, LCP Optimization & Layout Reservation Engine
 * Runs on frontend to boost Core Web Vitals and eliminate CLS.
 */

add_action('template_redirect', function () {

    if (is_admin() || !is_front_page()) {
        return;
    }

    ob_start(function ($html) {
        if (strlen($html) < 500) {
            return $html;
        }

        /*
         * ----------------------------------------------------------
         * 1. Viewport
         * ----------------------------------------------------------
         */
        $html = preg_replace(
            '/<meta\s+name=["\']viewport["\'][^>]*>/i',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            $html,
            1
        );

        /*
         * ----------------------------------------------------------
         * 2. Main landmark
         * ----------------------------------------------------------
         */
        $html = preg_replace_callback(
            '/<div([^>]*\bid=["\']main-content["\'][^>]*)>/i',
            function ($match) {
                if (preg_match('/\brole=["\']main["\']/i', $match[1])) {
                    return $match[0];
                }
                return '<div' . $match[1] . ' role="main">';
            },
            $html,
            1
        );

        /*
         * ----------------------------------------------------------
         * 3. Search buttons aria-label
         * ----------------------------------------------------------
         */
        $html = preg_replace_callback(
            '/<button\b([^>]*)>/i',
            function ($match) {
                $attrs = $match[1];
                if (
                    preg_match('/class=["\'][^"\']*\bsearchsubmit\b[^"\']*["\']/i', $attrs)
                    && !preg_match('/\baria-label=/i', $attrs)
                ) {
                    return '<button' . $attrs . ' aria-label="جستجو">';
                }
                return $match[0];
            },
            $html
        );

        /*
         * ----------------------------------------------------------
         * 4. Decorative arrow images
         * ----------------------------------------------------------
         */
        $html = preg_replace_callback(
            '/<img\b([^>]*(?:src|data-src)=["\'][^"\']*arrow-left(?:-1)?\.svg[^"\']*["\'][^>]*)>/i',
            function ($match) {
                $attrs = $match[1];
                if (!preg_match('/\balt=/i', $attrs)) {
                    return '<img' . $attrs . ' alt="">';
                }
                return $match[0];
            },
            $html
        );

        /*
         * ----------------------------------------------------------
         * 5. Category overlay links aria-label
         * ----------------------------------------------------------
         */
        $category_labels = [
            'یخچال-فریزر'              => 'یخچال فریزر',
            'تصفیه-کننده-آب'            => 'تصفیه کننده آب',
            'اصلاح-و-زیبایی'            => 'زیبایی و سلامت فردی',
            'لوازم-برقی-آشپزخانه'       => 'لوازم برقی و پخت و پز',
            'washing-cleaning'          => 'شستشو و نظافت',
            'drink-makers'              => 'نوشیدنی ساز',
            'heating-cooling'           => 'سرمایش و گرمایش',
            'audio-video'               => 'صوتی و تصویری',
        ];

        $html = preg_replace_callback(
            '/<a\b([^>]*class=["\'][^"\']*\bxts-cat-link\b[^"\']*["\'][^>]*)>/i',
            function ($match) use ($category_labels) {
                $attrs = $match[1];
                if (preg_match('/\baria-label=/i', $attrs)) {
                    return $match[0];
                }
                if (preg_match('/\bhref=["\']([^"\']+)["\']/i', $attrs, $href_match)) {
                    $url = urldecode($href_match[1]);
                    foreach ($category_labels as $slug => $label) {
                        if (strpos($url, $slug) !== false) {
                            return '<a' . $attrs . ' aria-label="' . esc_attr($label) . '">';
                        }
                    }
                }
                return $match[0];
            },
            $html
        );

        /*
         * ----------------------------------------------------------
         * 6. Promotional links aria-label
         * ----------------------------------------------------------
         */
        $html = preg_replace_callback(
            '/<a\b([^>]*)>/i',
            function ($match) {
                $attrs = $match[1];
                if (preg_match('/\baria-label=/i', $attrs) || !preg_match('/\bhref=["\']([^"\']+)["\']/i', $attrs, $href_match)) {
                    return $match[0];
                }
                $url = urldecode($href_match[1]);
                if (strpos($url, '/تخفیف-ها-و-پیشنهادات/') !== false) {
                    return '<a' . $attrs . ' aria-label="پیشنهادات و تخفیف‌های ویژه">';
                }
                if (strpos($url, 'trustseal.enamad.ir') !== false) {
                    return '<a' . $attrs . ' aria-label="نماد اعتماد الکترونیکی">';
                }
                return $match[0];
            },
            $html
        );

        /*
         * ----------------------------------------------------------
         * 7. CORE WEB VITALS: Layout Reservation & Content-Visibility CSS
         * ----------------------------------------------------------
         */
        $layout_css = '<style id="hk-lcp-cls-optimizer">
        /* 1. Hero banner space reservation */
        .xts-iimage-img-wrapper,
        .xts-iimage-img {
            aspect-ratio: 2057 / 765;
            width: 100%;
            display: block;
            background-color: #f5f5f7;
            overflow: hidden;
        }
        .xts-iimage-img img {
            aspect-ratio: 2057 / 765;
            width: 100%;
            height: auto;
            object-fit: cover;
        }

        /* 2. Header logo space reservation */
        .xts-logo img.xts-logo-main {
            width: 250px !important;
            height: 52px !important;
            aspect-ratio: 300 / 62;
            max-width: 100%;
            height: auto;
            display: inline-block;
        }

        /* 3. Product cards aspect-ratio reservation */
        .xts-product-thumb,
        .xts-product-image {
            aspect-ratio: 1 / 1;
            width: 100%;
            background-color: #f8f8fa;
            display: block;
            overflow: hidden;
        }
        .xts-product-image img {
            aspect-ratio: 1 / 1;
            width: 100%;
            height: 100%;
            object-fit: contain;
        }

        /* 4. Category thumbnails aspect-ratio reservation */
        .xts-cat-thumbnail,
        .xts-cat-image {
            aspect-ratio: 1 / 1;
            width: 100%;
            background-color: #f8f8fa;
            overflow: hidden;
        }

        /* 5. Content Visibility: Skip off-screen rendering for below-the-fold sections */
        @media (min-width: 768px) {
            .elementor-element.e-parent:nth-child(n+3),
            .xts-footer {
                content-visibility: auto;
                contain-intrinsic-size: 0 600px;
            }
        }
        @media (max-width: 767px) {
            .elementor-element.e-parent:nth-child(n+2),
            .xts-footer {
                content-visibility: auto;
                contain-intrinsic-size: 0 450px;
            }
        }

        /* 6. Instant font rendering override */
        body, button, input, select, textarea, h1, h2, h3, h4, h5, h6, .xts-entities-title {
            font-display: swap !important;
        }
        </style>';

        $html = str_replace('</head>', $layout_css . "\n</head>", $html);

        /*
         * ----------------------------------------------------------
         * 8. LCP HERO BANNER UN-LAZYLOAD
         * ----------------------------------------------------------
         */
        $html = preg_replace_callback(
            '/<img\b([^>]*clover-home-appliances-october-sale-banner[^>]*)>/i',
            function ($match) {
                $tag = $match[0];
                if (preg_match('/data-xts-src=[\'"]([^\'"]+)[\'"]/i', $tag, $src_m)) {
                    $real_src = $src_m[1];
                    $tag = preg_replace('/src=[\'"][^\'"]*[\'"]/i', 'src="' . $real_src . '"', $tag);
                }
                if (preg_match('/data-srcset=[\'"]([^\'"]+)[\'"]/i', $tag, $srcset_m)) {
                    $real_srcset = $srcset_m[1];
                    $tag = preg_replace('/srcset=[\'"][^\'"]*[\'"]/i', 'srcset="' . $real_srcset . '"', $tag);
                }
                $tag = preg_replace('/loading=[\'"]lazy[\'"]/i', 'loading="eager" fetchpriority="high"', $tag);
                if (strpos($tag, 'fetchpriority') === false) {
                    $tag = preg_replace('/<img\s+/i', '<img fetchpriority="high" ', $tag);
                }
                $tag = str_replace(['xts-lazy-load', 'xts-lazy-fade'], '', $tag);
                return $tag;
            },
            $html
        );

        /*
         * ----------------------------------------------------------
         * 9. LOGO SIZING & UN-LAZYLOAD
         * ----------------------------------------------------------
         */
        $html = preg_replace_callback(
            '/<img\b([^>]*class=[\'"][^\'"]*xts-logo-main[^\'"]*[\'"][^>]*)>/i',
            function ($match) {
                $tag = $match[0];
                if (strpos($tag, 'width=') === false) {
                    $tag = preg_replace('/<img\s+/i', '<img width="250" height="52" fetchpriority="high" ', $tag);
                }
                if (preg_match('/data-src=[\'"]([^\'"]+)[\'"]/i', $tag, $src_m)) {
                    $real_src = $src_m[1];
                    $tag = preg_replace('/src=[\'"][^\'"]*[\'"]/i', 'src="' . $real_src . '"', $tag);
                    $tag = preg_replace('/data-lazyloaded=[\'"][^\'"]*[\'"]/i', '', $tag);
                }
                return $tag;
            },
            $html,
            1
        );

        return $html;
    });
});"""

php_update_script = """<?php
add_action('init', function() {
    global $wpdb;
    $table = $wpdb->prefix . 'snippets';
    $code = <<<'EOD'
""" + snippet_6_code + """
EOD;
    $wpdb->update(
        $table,
        [
            'name' => 'دسترسی‌پذیری و بهینه‌سازی LCP و چیدمان فرانت‌اند',
            'code' => $code,
            'active' => 1
        ],
        ['id' => 6]
    );
    echo json_encode(['status' => 'snippet_6_updated']);
    exit;
}, 1);
"""

requests.post(url, cookies=cookies, data={
    'action': 'edit',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'filename': 'temp_update_s6.php',
    'text': php_update_script
}, verify=False)

r_trig = requests.get('https://hosseinykala.ir/?update_s6=1', headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
print("Update Snippet 6 result:\n", r_trig.text)

requests.post('https://server152c.irwebspace.com:2223/CMD_FILE_MANAGER', cookies=cookies, data={
    'action': 'multiple',
    'path': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins',
    'select0': '/domains/hosseinykala.ir/public_html/wp-content/mu-plugins/temp_update_s6.php',
    'button': 'delete'
}, verify=False)
