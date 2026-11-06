<?php
/**
 * HosseinyKala - Master FastCache & Full-Site Performance Engine
 * High-speed caching (sub-50ms), LCP un-lazyload, accessibility & visual stability across all pages.
 */

// 1. FastCache Engine & Output Buffer Transformer
add_action('template_redirect', function () {
    if (is_admin()) {
        return;
    }

    $uri = $_SERVER['REQUEST_URI'] ?? '/';
    $method = $_SERVER['REQUEST_METHOD'] ?? 'GET';

    // 1.1. Check if page caching is bypassed
    $bypass_cache = false;
    if ($method !== 'GET' || (defined('DOING_CRON') && DOING_CRON) || (defined('REST_REQUEST') && REST_REQUEST)) {
        $bypass_cache = true;
    }

    // Bypass for transactional / dynamic pages
    if (
        strpos($uri, '/cart') !== false ||
        strpos($uri, '/checkout') !== false ||
        strpos($uri, '/my-account') !== false ||
        strpos($uri, '/wp-admin') !== false ||
        strpos($uri, '/wp-login') !== false ||
        strpos($uri, '/wp-json') !== false ||
        strpos($uri, '?wc-ajax=') !== false
    ) {
        $bypass_cache = true;
    }

    // Bypass for logged-in users or active shoppers
    if (!$bypass_cache) {
        if (is_user_logged_in()) {
            $bypass_cache = true;
        } elseif (function_exists('WC') && WC()->cart && !WC()->cart->is_empty()) {
            $bypass_cache = true;
        } else {
            foreach ($_COOKIE as $k => $v) {
                if (strpos($k, 'wordpress_logged_in_') === 0 || $k === 'woocommerce_items_in_cart' || $k === 'woocommerce_cart_hash') {
                    $bypass_cache = true;
                    break;
                }
            }
        }
    }

    $cache_dir = WP_CONTENT_DIR . '/cache/hk_fastcache';
    $cache_file = null;
    $cache_file_gz = null;

    if (!$bypass_cache) {
        $clean_path = rtrim(parse_url($uri, PHP_URL_PATH) ?: '/', '/') ?: '/';
        $query = parse_url($uri, PHP_URL_QUERY) ?: '';
        if (!empty($query)) {
            parse_str($query, $qp);
            foreach (['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'fbclid', 'gclid', '_ga'] as $tk) {
                unset($qp[$tk]);
            }
            ksort($qp);
            $query = http_build_query($qp);
        }
        $device_suffix = (function_exists('wp_is_mobile') && wp_is_mobile()) ? '_mob' : '_desk';
        $cache_key = md5('hk_' . $clean_path . ($query ? '?' . $query : '') . $device_suffix);
        $cache_file = $cache_dir . '/' . $cache_key . '.html';
        $cache_file_gz = $cache_file . '.gz';

        // Check cache HIT
        if (file_exists($cache_file) && (time() - filemtime($cache_file) < 86400)) {
            while (ob_get_level()) {
                ob_end_clean();
            }
            header('Content-Type: text/html; charset=UTF-8');
            header('X-HosseinyKala-Cache: HIT');
            header('Cache-Control: public, max-age=3600, stale-while-revalidate=86400');
            header('Vary: Accept-Encoding');

            $accept_encoding = $_SERVER['HTTP_ACCEPT_ENCODING'] ?? '';
            if (strpos($accept_encoding, 'gzip') !== false && file_exists($cache_file_gz)) {
                header('Content-Encoding: gzip');
                readfile($cache_file_gz);
                exit;
            } else {
                readfile($cache_file);
                exit;
            }
        }

        if (!is_dir($cache_dir)) {
            @mkdir($cache_dir, 0755, true);
        }
        header('X-HosseinyKala-Cache: MISS');
    }

    // Output Buffer Transformer (Applies across all frontend pages)
    ob_start(function ($html) use ($cache_file, $cache_file_gz, $bypass_cache) {
        if (strlen($html) < 500) {
            return $html;
        }

        // 1. Accessibility: Standardize Viewport across ALL pages
        $html = preg_replace(
            '/<meta\s+name=["\']viewport["\'][^>]*>/i',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            $html,
            1
        );

        // 2. Accessibility: Discernible names for Category links (.xts-cat-link)
        $html = preg_replace_callback(
            '/<a\b([^>]*class=["\'][^"\']*\bxts-cat-link\b[^"\']*["\'][^>]*)>/i',
            function ($m) {
                if (stripos($m[1], 'aria-label') !== false) return $m[0];
                return '<a' . $m[1] . ' aria-label="مشاهده محصولات این دسته‌بندی">';
            },
            $html
        );

        // 3. Accessibility: Discernible names for Enamad & empty links
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

        // 4. Accessibility: Main search button aria-label
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

        // 5. Un-lazyload Header Logo on ALL pages (prevents LCP delay on standard pages)
        $html = preg_replace_callback(
            '/<img\b([^>]*class=["\'][^"\']*\bxts-logo-main\b[^"\']*["\'][^>]*)>/i',
            function ($m) {
                $attrs = $m[1];
                $attrs = preg_replace('/\bloading=["\']lazy["\']/i', '', $attrs);
                if (stripos($attrs, 'loading=') === false) {
                    $attrs .= ' loading="eager"';
                }
                if (stripos($attrs, 'fetchpriority=') === false) {
                    $attrs .= ' fetchpriority="high"';
                }
                return '<img' . $attrs . '>';
            },
            $html,
            1
        );

        // 6. Homepage Hero Banners Un-lazyload
        if (is_front_page()) {
            // Mobile Square Banner
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
                    if (stripos($attrs, 'fetchpriority') === false) $attrs .= ' fetchpriority="high"';
                    if (stripos($attrs, 'loading=') === false) $attrs .= ' loading="eager"';
                    return '<img' . $attrs . '>';
                },
                $html,
                1
            );

            // Desktop Hero Banner
            $html = preg_replace_callback(
                '/<img\b([^>]*clover-home-appliances-october-sale-banner[^>]*)>/i',
                function ($m) {
                    $attrs = $m[1];
                    $attrs = preg_replace('/\bxts-lazy-load\b|\bxts-lazy-fade\b/i', 'xts-loaded', $attrs);
                    $real_src = 'https://hosseinykala.ir/wp-content/uploads/2026/10/clover-home-appliances-october-sale-banner.webp';
                    $attrs = preg_replace('/\bsrc=["\']data:image\/[^"\']+["\']/i', 'src="' . $real_src . '"', $attrs);
                    $attrs = preg_replace('/\bloading=["\']lazy["\']/i', '', $attrs);
                    if (stripos($attrs, 'fetchpriority') === false) $attrs .= ' fetchpriority="high"';
                    if (stripos($attrs, 'loading=') === false) $attrs .= ' loading="eager"';
                    return '<img' . $attrs . '>';
                },
                $html,
                1
            );
        }

        // 7. Single Product Page: Un-lazyload Featured Product Image
        if (function_exists('is_product') && is_product()) {
            $unlazy_p = false;
            $html = preg_replace_callback(
                '/<img\b([^>]*\b(?:wp-post-image|woocommerce-product-gallery__image|attachment-full)\b[^>]*)>/i',
                function ($m) use (&$unlazy_p) {
                    if ($unlazy_p) return $m[0];
                    $attrs = $m[1];
                    if (stripos($attrs, 'data-xts-src') === false && stripos($attrs, 'data-src') === false) return $m[0];
                    $unlazy_p = true;

                    $attrs = preg_replace('/\bxts-lazy-load\b|\bxts-lazy-fade\b/i', 'xts-loaded', $attrs);
                    if (preg_match('/data-xts-src=["\']([^"\']+)["\']/i', $attrs, $src_m)) {
                        $attrs = preg_replace('/\bsrc=["\']data:image\/[^"\']+["\']/i', 'src="' . $src_m[1] . '"', $attrs);
                    } elseif (preg_match('/data-src=["\']([^"\']+)["\']/i', $attrs, $src_m)) {
                        $attrs = preg_replace('/\bsrc=["\']data:image\/[^"\']+["\']/i', 'src="' . $src_m[1] . '"', $attrs);
                    }
                    if (preg_match('/data-srcset=["\']([^"\']+)["\']/i', $attrs, $srcset_m)) {
                        $attrs = preg_replace('/\bsrcset(=["\'][^"\']*["\'])?/i', 'srcset="' . $srcset_m[1] . '"', $attrs);
                    }
                    $attrs = preg_replace('/\bloading=["\']lazy["\']/i', '', $attrs);
                    if (stripos($attrs, 'fetchpriority') === false) $attrs .= ' fetchpriority="high"';
                    if (stripos($attrs, 'loading=') === false) $attrs .= ' loading="eager"';
                    return '<img' . $attrs . '>';
                },
                $html
            );
        }

        // 8. Shop / Category Archive: Un-lazyload first 2 product images
        if ((function_exists('is_shop') && is_shop()) || (function_exists('is_product_category') && is_product_category())) {
            $unlazy_count = 0;
            $html = preg_replace_callback(
                '/<img\b([^>]*\bxts-lazy-load\b[^>]*)>/i',
                function ($m) use (&$unlazy_count) {
                    if ($unlazy_count >= 2) return $m[0];
                    $attrs = $m[1];
                    if (stripos($attrs, 'data-xts-src') === false && stripos($attrs, 'data-src') === false) return $m[0];
                    $unlazy_count++;

                    $attrs = preg_replace('/\bxts-lazy-load\b|\bxts-lazy-fade\b/i', 'xts-loaded', $attrs);
                    if (preg_match('/data-xts-src=["\']([^"\']+)["\']/i', $attrs, $src_m)) {
                        $attrs = preg_replace('/\bsrc=["\']data:image\/[^"\']+["\']/i', 'src="' . $src_m[1] . '"', $attrs);
                    } elseif (preg_match('/data-src=["\']([^"\']+)["\']/i', $attrs, $src_m)) {
                        $attrs = preg_replace('/\bsrc=["\']data:image\/[^"\']+["\']/i', 'src="' . $src_m[1] . '"', $attrs);
                    }
                    if (preg_match('/data-srcset=["\']([^"\']+)["\']/i', $attrs, $srcset_m)) {
                        $attrs = preg_replace('/\bsrcset(=["\'][^"\']*["\'])?/i', 'srcset="' . $srcset_m[1] . '"', $attrs);
                    }
                    $attrs = preg_replace('/\bloading=["\']lazy["\']/i', '', $attrs);
                    if ($unlazy_count === 1) {
                        if (stripos($attrs, 'fetchpriority') === false) $attrs .= ' fetchpriority="high"';
                        if (stripos($attrs, 'loading=') === false) $attrs .= ' loading="eager"';
                    }
                    return '<img' . $attrs . '>';
                },
                $html
            );
        }

        // 9. Blog Archive: Un-lazyload first post image
        if ((function_exists('is_home') && is_home()) || (function_exists('is_archive') && is_archive() && !is_product_category())) {
            $unlazy_blog = false;
            $html = preg_replace_callback(
                '/<img\b([^>]*\b(?:xts-post-image|attachment-post-thumbnail)\b[^>]*)>/i',
                function ($m) use (&$unlazy_blog) {
                    if ($unlazy_blog) return $m[0];
                    $unlazy_blog = true;
                    $attrs = $m[1];
                    $attrs = preg_replace('/\bloading=["\']lazy["\']/i', '', $attrs);
                    if (stripos($attrs, 'fetchpriority') === false) $attrs .= ' fetchpriority="high"';
                    if (stripos($attrs, 'loading=') === false) $attrs .= ' loading="eager"';
                    return '<img' . $attrs . '>';
                },
                $html
            );
        }

        // 10. Save to FastCache if eligible
        if (!$bypass_cache && $cache_file && http_response_code() === 200 && strlen($html) > 1000) {
            $headers = headers_list();
            $set_cookie_found = false;
            foreach ($headers as $h) {
                if (stripos($h, 'Set-Cookie:') !== false && (stripos($h, 'wordpress_logged_in') !== false || stripos($h, 'woocommerce_items_in_cart') !== false)) {
                    $set_cookie_found = true;
                    break;
                }
            }
            if (!$set_cookie_found) {
                $signed = $html . "\n<!-- HK FastCache (" . gmdate('Y-m-d H:i:s') . " GMT) -->";
                @file_put_contents($cache_file, $signed);
                @file_put_contents($cache_file_gz, gzencode($signed, 6));
            }
        }

        return $html;
    });
}, 1);

// 2. Preload & Safe Visual Stability Engine
add_action('wp_head', function () {
    // 2.0. Prevent third-party / inline scripts throwing "wp is not defined" before core i18n bundle loads
    echo '<script id="hk-wp-i18n-stub">window.wp=window.wp||{};window.wp.i18n=window.wp.i18n||{setLocaleData:function(d,n){window._wp_loc=window._wp_loc||{};window._wp_loc[n||"default"]=d;},__:function(t){return t;},_x:function(t){return t;},_n:function(s,p,n){return n===1?s:p;},_nx:function(s,p,n){return n===1?s:p;},isRtl:function(){return true;},sprintf:function(){return arguments[0]||"";}};</script>' . "\n";

    // 2.1. Preload primary Persian WOFF2 fonts
    echo '<link rel="preload" href="/wp-content/themes/xts-luman/fonts/iranyekanx/woff2/IRANYekanXFaNum-Regular.woff2" as="font" type="font/woff2" crossorigin>' . "\n";
    echo '<link rel="preload" href="/wp-content/themes/xts-luman/fonts/iranyekanx/woff2/IRANYekanXFaNum-Bold.woff2" as="font" type="font/woff2" crossorigin>' . "\n";

    // 2.2. Preload true LCP Hero image (Targeted by device)
    if (is_front_page()) {
        if (wp_is_mobile()) {
            echo '<link rel="preload" as="image" href="https://hosseinykala.ir/wp-content/uploads/2026/10/clover-october-sale-square-banner-600x600.webp" fetchpriority="high">' . "\n";
        } else {
            echo '<link rel="preload" as="image" href="https://hosseinykala.ir/wp-content/uploads/2026/10/clover-home-appliances-october-sale-banner.webp" fetchpriority="high">' . "\n";
        }
    }

    // 2.3. Preload featured product image on single product pages
    if (function_exists('is_product') && is_product()) {
        $thumb_id = get_post_thumbnail_id();
        if ($thumb_id) {
            $img_url = wp_get_attachment_image_url($thumb_id, 'woocommerce_single') ?: wp_get_attachment_image_url($thumb_id, 'full');
            if ($img_url) {
                echo '<link rel="preload" as="image" href="' . esc_url($img_url) . '" fetchpriority="high">' . "\n";
            }
        }
    }

    // 2.4. Preload first product image on shop & category archives
    if ((function_exists('is_shop') && is_shop()) || (function_exists('is_product_category') && is_product_category())) {
        global $wp_query;
        if (!empty($wp_query->posts) && isset($wp_query->posts[0]->ID)) {
            $p_thumb = get_post_thumbnail_id($wp_query->posts[0]->ID);
            if ($p_thumb) {
                $p_url = wp_get_attachment_image_url($p_thumb, 'woocommerce_thumbnail') ?: wp_get_attachment_image_url($p_thumb, 'medium');
                if ($p_url) {
                    echo '<link rel="preload" as="image" href="' . esc_url($p_url) . '" fetchpriority="high">' . "\n";
                }
            }
        }
    }

    // 2.5. Safe UI, Accessibility Contrast & Visual Stability CSS
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

// 3. Dequeue non-critical styles across all frontend pages
add_action('wp_enqueue_scripts', function () {
    if (!is_admin()) {
        wp_dequeue_style('wc-blocks-style-rtl');
        wp_dequeue_style('wc-blocks-style');
        wp_dequeue_style('lpl-ticket');
        wp_dequeue_style('lpl-support-public');
        wp_dequeue_style('luman-ios-notification-style');
    }
}, 9999);
