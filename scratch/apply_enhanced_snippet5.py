import requests
import json

auth = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# Read Snippet 5
r = requests.get('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/5', auth=auth, headers=headers, timeout=10)
s5 = r.json()

new_snippet_5 = r"""/**
 * HosseinyKala - Core Web Vitals, LCP Un-lazyload, Font & Visual Stability Engine
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

// 2. Un-lazyload LCP Hero Banner & Serve Responsive WebP on Homepage
add_action('template_redirect', function () {
    if (is_admin() || !is_front_page()) {
        return;
    }

    ob_start(function ($html) {
        if (strlen($html) < 500) {
            return $html;
        }

        // 2.1. Transform Mobile Square Banner: remove lazyload, set 600x600 webp src, high priority
        $html = preg_replace_callback(
            '/<img\b([^>]*clover-october-sale-square-banner[^>]*)>/i',
            function ($m) {
                $attrs = $m[1];
                // Remove lazyload classes
                $attrs = preg_replace('/\bxts-lazy-load\b|\bxts-lazy-fade\b/i', 'xts-loaded', $attrs);
                // Replace placeholder base64 src with real 600x600 webp
                $real_src = 'https://hosseinykala.ir/wp-content/uploads/2026/10/clover-october-sale-square-banner-600x600.webp';
                $attrs = preg_replace('/\bsrc=["\']data:image\/[^"\']+["\']/i', 'src="' . $real_src . '"', $attrs);
                // Set sizes and dimensions for 600x600
                $attrs = preg_replace('/\bwidth=["\']\d+["\']/i', 'width="600"', $attrs);
                $attrs = preg_replace('/\bheight=["\']\d+["\']/i', 'height="600"', $attrs);
                $attrs = preg_replace('/\bsizes=["\'][^"\']+["\']/i', 'sizes="(max-width: 767px) 100vw, 600px"', $attrs);
                // Ensure fetchpriority=high and remove lazy loading
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

        // 2.2. Transform Desktop Hero Banner: remove lazyload, set full webp src, high priority
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

    // 3.4. Safe UI & Visual Stability CSS
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
"""

s5['code'] = new_snippet_5
res = requests.put('https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/5', auth=auth, headers=headers, json=s5, timeout=15)
print("Updated Snippet 5 status:", res.status_code)

# Purge cache
r_purge = requests.post('https://hosseinykala.ir/wp-json/hk-perf/v1/purge-all', auth=auth, headers=headers, timeout=15)
print("Purged cache status:", r_purge.status_code, r_purge.json())
