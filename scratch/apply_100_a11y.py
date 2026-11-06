import requests
import json

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

r = requests.get('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/5', auth=auth, headers=headers, timeout=10)
s5 = r.json()

new_snippet_5 = r"""/**
 * HosseinyKala - Core Web Vitals, LCP Un-lazyload, Accessibility (A11y 100%) & Visual Stability Engine
 */

// 1. Defer jQuery in Frontend (Eliminates Render-Blocking)
add_filter('script_loader_tag', function ($tag, $handle) {
    if (($handle === 'jquery-core' || $handle === 'jquery') && !is_admin()) {
        if (strpos($tag, 'defer') === false && strpos($tag, 'async') === false) {
            $tag = str_replace(' src=', ' defer="defer" src=', $tag);
        }
    }
    return $tag;
}, 10, 2);

// 2. Un-lazyload LCP Hero Banner & 100% Accessibility Enhancer
add_action('template_redirect', function () {
    if (is_admin() || !is_front_page()) {
        return;
    }

    ob_start(function ($html) {
        if (strlen($html) < 500) {
            return $html;
        }

        // 2.1. Accessibility: Fix viewport zoom restriction (Eliminates meta-viewport 10-point penalty)
        $html = preg_replace(
            '/<meta\s+name=["\']viewport["\'][^>]*>/i',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            $html,
            1
        );

        // 2.2. Accessibility: Discernible names for Category links (.xts-cat-link)
        $html = preg_replace_callback(
            '/<a\b([^>]*class=["\'][^"\']*\bxts-cat-link\b[^"\']*["\'][^>]*)>/i',
            function ($m) {
                if (stripos($m[1], 'aria-label') !== false) return $m[0];
                return '<a' . $m[1] . ' aria-label="مشاهده محصولات این دسته‌بندی">';
            },
            $html
        );

        // 2.3. Accessibility: Discernible names for Elementor banner links & empty category links
        $html = preg_replace_callback(
            '/<a\b([^>]*href=["\'][^"\']+["\'][^>]*)>(?=\s*<img\b[^>]*\balt=["\']\s*["\'])/i',
            function ($m) {
                $attrs = $m[1];
                if (stripos($attrs, 'aria-label') !== false) return $m[0];

                $label = 'مشاهده جزئیات و خرید کالا';
                if (stripos($attrs, '%db%8c%d8%ae%da%86%d8%a7%d9%84') !== false || stripos($attrs, 'refrigerator') !== false) {
                    $label = 'خرید و قیمت انواع یخچال و فریزر';
                } elseif (stripos($attrs, '%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d9%84%d8%a8%d8%a7%d8%b3%d8%b4%d9%88%db%8c%db%8c') !== false || stripos($attrs, 'washing') !== false) {
                    $label = 'خرید و قیمت انواع ماشین لباسشویی';
                } elseif (stripos($attrs, '%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d8%b8%d8%b1%d9%81%d8%b4%d9%88%db%8c%db%8c') !== false || stripos($attrs, 'dishwasher') !== false) {
                    $label = 'خرید و قیمت انواع ماشین ظرفشویی';
                } elseif (stripos($attrs, '%da%a9%d9%88%d9%84%d8%b1') !== false || stripos($attrs, 'cooling') !== false) {
                    $label = 'خرید و قیمت انواع کولر آبی';
                } elseif (stripos($attrs, '%d8%aa%d8%ae%d9%81%db%8c%d9%81') !== false) {
                    $label = 'مشاهده تخفیف‌ها و پیشنهادات شگفت‌انگیز حسینی کالا';
                }

                return '<a' . $attrs . ' aria-label="' . $label . '">';
            },
            $html
        );

        // 2.4. Accessibility: Discernible names for Enamad & empty links
        $html = preg_replace(
            '/<a\b([^>]*trustseal\.enamad\.ir[^>]*)>/i',
            '<a$1 aria-label="نماد اعتماد الکترونیکی حسینی کالا">',
            $html
        );
        $html = preg_replace(
            '/<a\s+href=["\']#["\'](\s*class=["\'][^"\']*["\'])?\s*>/i',
            '<a href="#"$1 aria-label="لینک ناوبری">',
            $html
        );

        // 2.5. Accessibility: Main search button aria-label
        $html = preg_replace_callback(
            '/<button\b([^>]*)>/i',
            function ($m) {
                $attrs = $m[1];
                if (stripos($attrs, 'searchsubmit') !== false && stripos($attrs, 'aria-label') === false) {
                    return '<button' . $attrs . ' aria-label="جستجو در فروشگاه">';
                }
                return $m[0];
            },
            $html
        );

        // 2.6. Transform Mobile Square Banner: remove lazyload, set 600x600 webp src, high priority
        $html = preg_replace_callback(
            '/<img\b([^>]*clover-october-sale-square-banner[^>]*)>/i',
            function ($m) {
                $attrs = $m[1];
                $attrs = preg_replace('/\bxts-lazy-load\b|\bxts-lazy-fade\b/i', 'xts-loaded', $attrs);
                $real_src = 'https://hosseinykala.ir/wp-content/uploads/2026/10/clover-october-sale-square-banner-600x600.webp';
                $attrs = preg_replace('/\bsrc=["\']data:image\/[^"\']+["\']/i', 'src="' . $real_src . '"', $attrs);
                $attrs = preg_replace('/\bwidth=["\']\d+["\']/i', 'width="600"', $attrs);
                $attrs = preg_replace('/\bheight=["\']\d+["\']/i', 'height="600"', $attrs);
                $attrs = preg_replace('/\bsizes=["\'][^"\']+["\']/i', 'sizes="(max-width: 767px) 100vw, 600px"', $attrs);
                $attrs = preg_replace('/\bloading=["\']lazy["\']/i', '', $attrs);
                if (stripos($attrs, 'fetchpriority') === false) {
                    $attrs .= ' fetchpriority="high"';
                }
                if (stripos($attrs, 'loading=') === false) {
                    $attrs .= ' loading="eager"';
                }
                return '<img' . $attrs . '>';
            },
            $html,
            1
        );

        // 2.7. Transform Desktop Hero Banner: remove lazyload, set full webp src, high priority
        $html = preg_replace_callback(
            '/<img\b([^>]*clover-home-appliances-october-sale-banner[^>]*)>/i',
            function ($m) {
                $attrs = $m[1];
                $attrs = preg_replace('/\bxts-lazy-load\b|\bxts-lazy-fade\b/i', 'xts-loaded', $attrs);
                $real_src = 'https://hosseinykala.ir/wp-content/uploads/2026/10/clover-home-appliances-october-sale-banner.webp';
                $attrs = preg_replace('/\bsrc=["\']data:image\/[^"\']+["\']/i', 'src="' . $real_src . '"', $attrs);
                $attrs = preg_replace('/\bloading=["\']lazy["\']/i', '', $attrs);
                if (stripos($attrs, 'fetchpriority') === false) {
                    $attrs .= ' fetchpriority="high"';
                }
                if (stripos($attrs, 'loading=') === false) {
                    $attrs .= ' loading="eager"';
                }
                return '<img' . $attrs . '>';
            },
            $html,
            1
        );

        return $html;
    });
}, 1);

// 3. Preload & Safe Visual Stability Engine
add_action('wp_head', function () {
    // 3.1. Preload primary Persian WOFF2 fonts
    echo '<link rel="preload" href="/wp-content/themes/xts-luman/fonts/iranyekanx/woff2/IRANYekanXFaNum-Regular.woff2" as="font" type="font/woff2" crossorigin>' . "\n";
    echo '<link rel="preload" href="/wp-content/themes/xts-luman/fonts/iranyekanx/woff2/IRANYekanXFaNum-Bold.woff2" as="font" type="font/woff2" crossorigin>' . "\n";

    // 3.2. Responsive Hero image Preload on Homepage
    if (is_front_page()) {
        echo '<link rel="preload" as="image" href="https://hosseinykala.ir/wp-content/uploads/2026/10/clover-home-appliances-october-sale-banner.webp" media="(min-width: 768px)" fetchpriority="high">' . "\n";
        echo '<link rel="preload" as="image" href="https://hosseinykala.ir/wp-content/uploads/2026/10/clover-october-sale-square-banner-600x600.webp" media="(max-width: 767px)" fetchpriority="high">' . "\n";
    }

    // 3.3. Preload featured product image on single product pages
    if (function_exists('is_product') && is_product()) {
        $thumb_id = get_post_thumbnail_id();
        if ($thumb_id) {
            $img_url = wp_get_attachment_image_url($thumb_id, 'woocommerce_single');
            if ($img_url) {
                echo '<link rel="preload" as="image" href="' . esc_url($img_url) . '" fetchpriority="high">' . "\n";
            }
        }
    }

    // 3.4. Safe UI, Accessibility Contrast & Visual Stability CSS
    echo '<style id="hk-core-stability-css">
    /* Explicit WOFF2 font bindings (Eliminates redundant WOFF downloads) */
    @font-face {
        font-family: "IRANYekanX";
        font-style: normal;
        font-weight: 400;
        font-display: swap;
        src: url("/wp-content/themes/xts-luman/fonts/iranyekanx/woff2/IRANYekanXFaNum-Regular.woff2") format("woff2");
    }
    @font-face {
        font-family: "IRANYekanX";
        font-style: normal;
        font-weight: 700;
        font-display: swap;
        src: url("/wp-content/themes/xts-luman/fonts/iranyekanx/woff2/IRANYekanXFaNum-Bold.woff2") format("woff2");
    }

    /* Accessibility (A11y): High Contrast Ratios (WCAG 4.5:1 Compliant) */
    .xts-search-wrapper input.s,
    .xts-search-wrapper input.s::placeholder {
        color: #4a4a4a !important;
    }
    .xts-cat-count,
    .xts-cat-count span,
    .xts-cat-count-text {
        color: #444444 !important;
    }
    span.price del,
    span.price del bdi,
    span.price del .woocommerce-Price-amount {
        color: #555555 !important;
    }
    .elementor-heading-title,
    .elementor-image-box-description,
    .elementor-icon-list-text {
        color: #444444 !important;
    }
    .elementor-button .elementor-button-text {
        color: #262299 !important;
    }
    footer a,
    .xts-footer a {
        color: #444444 !important;
    }

    /* Mobile Drawer & Off-canvas Flash Prevention */
    @media (min-width: 1025px) {
        .xts-side-mobile,
        .xts-header-mobile-burger {
            display: none !important;
        }
    }

    html:not(.xts-ready) .xts-side-mobile:not(.xts-opened),
    html:not(.xts-ready) .xts-cart-widget-side:not(.xts-opened),
    html:not(.xts-ready) .xts-side-hidden:not(.xts-opened) {
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        transform: translate3d(100%, 0, 0) !important;
        -webkit-transform: translate3d(100%, 0, 0) !important;
        transition: none !important;
    }

    .xts-side-mobile:not(.xts-opened),
    .xts-cart-widget-side:not(.xts-opened),
    .xts-side-hidden:not(.xts-opened) {
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        transform: translate3d(100%, 0, 0) !important;
        -webkit-transform: translate3d(100%, 0, 0) !important;
        transition: transform .3s cubic-bezier(.19, 1, .22, 1), opacity .2s ease, visibility 0s linear .3s !important;
    }

    .xts-side-mobile.xts-opened,
    .xts-cart-widget-side.xts-opened,
    .xts-side-hidden.xts-opened {
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        transform: translate3d(0, 0, 0) !important;
        -webkit-transform: translate3d(0, 0, 0) !important;
        transition: transform .35s cubic-bezier(.19, 1, .22, 1), opacity .25s ease !important;
    }

    /* Header Logo Normalization */
    .xts-logo img.xts-logo-main {
        width: auto !important;
        max-width: 160px !important;
        max-height: 46px !important;
        height: auto !important;
        aspect-ratio: 300 / 62;
        object-fit: contain !important;
        display: inline-block;
    }
    @media (max-width: 767px) {
        .xts-logo img.xts-logo-main {
            max-width: 130px !important;
            max-height: 36px !important;
        }
    }

    /* Hero Banner: Desktop */
    @media (min-width: 768px) {
        .elementor-element-818edb4 .xts-iimage-img-wrapper,
        .elementor-element-818edb4 .xts-iimage-img {
            aspect-ratio: 2057 / 765;
            width: 100%;
            display: block;
        }
        .elementor-element-818edb4 .xts-iimage-img img {
            aspect-ratio: 2057 / 765;
            width: 100%;
            height: auto;
            object-fit: cover;
        }
    }

    /* Hero Banner: Mobile */
    @media (max-width: 767px) {
        .home .xts-header {
            margin-bottom: 8px !important;
        }
        .home .xts-site-content,
        .home #main-content,
        .home .xts-content-area,
        .home article#post-43 {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        .home .elementor-element-2c289bf {
            display: none !important;
            height: 0 !important;
        }
        .home .elementor-element-e82e234,
        .home .elementor-element-e6d7e87 {
            margin-top: 0 !important;
            padding-top: 0 !important;
            --margin-top: 0px !important;
            --padding-top: 0px !important;
        }
        .elementor-element-e6d7e87 .xts-iimage-img-wrapper {
            width: 100% !important;
            height: auto !important;
            min-height: auto !important;
            max-height: none !important;
            aspect-ratio: 1 / 1 !important;
            background-color: transparent !important;
            overflow: hidden;
        }
        .elementor-element-e6d7e87 .xts-iimage-img-wrapper img,
        .elementor-element-e6d7e87 .elementor-repeater-item-5d48057 .xts-iimage .xts-iimage-img-wrapper :is(img,video) {
            width: 100% !important;
            height: auto !important;
            aspect-ratio: 1 / 1 !important;
            object-fit: contain !important;
            object-position: top center !important;
            display: block !important;
        }
    }

    /* Category Thumbnails: Transparent PNG fix */
    .xts-cat-thumbnail, .xts-cat-image {
        background-color: transparent !important;
    }

    /* Sticky Header Floating Line Fix */
    .xts-header.xts-sticked .xts-header-inner,
    .xts-header.xts-sticked .xts-header-main,
    .xts-header.xts-sticked .xts-header-row,
    .xts-header.xts-sticked .xts-header-row-inner {
        border-bottom: none !important;
        border-top: none !important;
        box-shadow: none !important;
    }
    .xts-header.xts-sticked .xts-header-bottom {
        display: none !important;
        border: none !important;
    }

    /* Blog Cards Normalization (16:9 ratio) */
    .xts-posts .xts-post-thumb .xts-post-image,
    .xts-post .xts-post-thumb .xts-post-image {
        aspect-ratio: 16 / 9;
        width: 100%;
        overflow: hidden;
    }
    .xts-posts .xts-post-thumb .xts-post-image img,
    .xts-post .xts-post-thumb .xts-post-image img {
        width: 100%;
        height: 100%;
        aspect-ratio: 16 / 9;
        object-fit: cover !important;
    }

    /* Global Font Display Swap */
    body, button, input, select, textarea, h1, h2, h3, h4, h5, h6, .xts-entities-title {
        font-display: swap !important;
    }
    </style>' . "\n";

    echo '<script>document.addEventListener("DOMContentLoaded",function(){document.documentElement.classList.add("xts-ready");});</script>' . "\n";
}, 1);

// 4. Dequeue non-critical styles from Homepage
add_action('wp_enqueue_scripts', function () {
    if (is_front_page()) {
        wp_dequeue_style('wc-blocks-style-rtl');
        wp_dequeue_style('wc-blocks-style');
        wp_dequeue_style('lpl-ticket');
        wp_dequeue_style('lpl-support-public');
        wp_dequeue_style('luman-ios-notification-style');
    }
}, 9999);
"""

s5['code'] = new_snippet_5
res = requests.put('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/5', auth=auth, headers=headers, json=s5, timeout=15)
print("Updated Snippet 5 status:", res.status_code)

# Purge cache
r_p = requests.post('https://hosseinykala.ir/wp-json/hk-perf/v1/purge-all', auth=auth, headers=headers, timeout=15)
print("Purge cache:", r_p.json())
