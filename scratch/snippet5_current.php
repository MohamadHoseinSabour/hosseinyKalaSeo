/**
 * HosseinyKala - Core Web Vitals & Visual Stability Engine
 */
add_action('wp_head', function () {
    // 1. Preload primary Persian fonts with font-display: swap
    echo '<link rel="preload" href="/wp-content/themes/xts-luman/fonts/iranyekanx/woff2/IRANYekanXFaNum-Regular.woff2" as="font" type="font/woff2" crossorigin>' . "\n";
    echo '<link rel="preload" href="/wp-content/themes/xts-luman/fonts/iranyekanx/woff2/IRANYekanXFaNum-Bold.woff2" as="font" type="font/woff2" crossorigin>' . "\n";

    // 2. Responsive Hero image Preload on Homepage
    if (is_front_page()) {
        echo '<link rel="preload" as="image" href="https://hosseinykala.ir/wp-content/uploads/2026/10/clover-home-appliances-october-sale-banner.webp" media="(min-width: 768px)" fetchpriority="high">' . "\n";
        echo '<link rel="preload" as="image" href="https://hosseinykala.ir/wp-content/uploads/2026/10/clover-october-sale-square-banner.webp" media="(max-width: 767px)" fetchpriority="high">' . "\n";
    }

    // 3. Preload featured product image on single product pages
    if (function_exists('is_product') && is_product()) {
        $thumb_id = get_post_thumbnail_id();
        if ($thumb_id) {
            $img_url = wp_get_attachment_image_url($thumb_id, 'woocommerce_single');
            if ($img_url) {
                echo '<link rel="preload" as="image" href="' . esc_url($img_url) . '" fetchpriority="high">' . "\n";
            }
        }
    }

    // 4. Safe UI & Visual Stability CSS
    echo '<style id="hk-core-stability-css">
    /* ==========================================================================
       Mobile Drawer & Off-canvas Flash Prevention (FOOS Fix)
       ========================================================================== */
    /* Desktop: Never show mobile drawer or burger */
    @media (min-width: 1025px) {
        .xts-side-mobile,
        .xts-header-mobile-burger {
            display: none !important;
        }
    }

    /* While page is loading (before ready): absolutely no transitions and strictly hidden */
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

    /* Base closed state */
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

    /* Open state */
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

    /* Header Logo Normalization: Prevents deformation */
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

    /* Hero Banner: Mobile (Clean natural fit without cropping or void) */
    @media (max-width: 767px) {
        /* Reduce excess top gap between header and mobile banner */
        .home .xts-header {
            margin-bottom: 8px !important;
        }
        .home .xts-site-content {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        .home #main-content,
        .home .xts-content-area,
        .home article#post-43 {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        /* Hide the completely empty shortcode container sitting above hero */
        .home .elementor-element-2c289bf {
            display: none !important;
            margin: 0 !important;
            padding: 0 !important;
            height: 0 !important;
            min-height: 0 !important;
        }
        /* Clean hero container spacing */
        .home .elementor-element-e82e234 {
            margin-top: 0 !important;
            padding-top: 0 !important;
            --margin-top: 0px !important;
            --padding-top: 0px !important;
        }
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
            min-height: auto !important;
            max-height: none !important;
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

    /* Font display swap */
    body, button, input, select, textarea, h1, h2, h3, h4, h5, h6, .xts-entities-title {
        font-display: swap !important;
    }
    </style>' . "\n";

    echo '<script>document.addEventListener("DOMContentLoaded",function(){document.documentElement.classList.add("xts-ready");});</script>' . "\n";
}, 1);
