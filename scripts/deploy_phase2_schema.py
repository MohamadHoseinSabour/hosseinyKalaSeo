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

# Fetch Snippet 7 current code
req = urllib.request.Request(
    'https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/7',
    headers=headers
)
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode('utf-8'))

current_code = data.get('code', '')

schema_php_block = r'''

// =========================================================================
// 4. ADVANCED SCHEMA.ORG & GOOGLE MERCHANT VALIDATION ENGINE (Phase 2)
// =========================================================================
add_filter('rank_math/json_ld', function ($data, $jsonld) {
    if (empty($data)) return $data;

    // 4.1. PRODUCTS: Google Merchant Compliance (Offer, Return Policy, Shipping)
    if (is_product()) {
        foreach ($data as $key => &$entity) {
            if (isset($entity['@type']) && $entity['@type'] === 'Product') {
                if (empty($entity['brand'])) {
                    $entity['brand'] = [
                        '@type' => 'Brand',
                        'name' => 'حسینی کالا'
                    ];
                }

                $return_policy = [
                    '@type' => 'MerchantReturnPolicy',
                    'applicableCountry' => 'IR',
                    'returnPolicyCategory' => 'https://schema.org/MerchantReturnFiniteReturnWindow',
                    'merchantReturnDays' => 7,
                    'returnMethod' => 'https://schema.org/ReturnByMail',
                    'returnFees' => 'https://schema.org/FreeReturn'
                ];

                $shipping_details = [
                    '@type' => 'OfferShippingDetails',
                    'shippingDestination' => [
                        '@type' => 'DefinedRegion',
                        'addressCountry' => 'IR'
                    ],
                    'deliveryTime' => [
                        '@type' => 'ShippingDeliveryTime',
                        'handlingTime' => [
                            '@type' => 'QuantitativeValue',
                            'minValue' => 0,
                            'maxValue' => 1,
                            'unitCode' => 'DAY'
                        ],
                        'transitTime' => [
                            '@type' => 'QuantitativeValue',
                            'minValue' => 1,
                            'maxValue' => 3,
                            'unitCode' => 'DAY'
                        ]
                    ]
                ];

                if (isset($entity['offers'])) {
                    $price = isset($entity['offers']['lowPrice']) ? $entity['offers']['lowPrice'] : (isset($entity['offers']['price']) ? $entity['offers']['price'] : '0');
                    if (empty($price) || $price === '0') {
                        global $product;
                        if ($product && method_exists($product, 'get_price')) {
                            $price = $product->get_price();
                        }
                    }

                    $entity['offers']['@type'] = 'Offer';
                    $entity['offers']['price'] = (string)$price;
                    $entity['offers']['priceCurrency'] = 'IRR';
                    $entity['offers']['availability'] = 'https://schema.org/InStock';
                    $entity['offers']['itemCondition'] = 'https://schema.org/NewCondition';
                    $entity['offers']['priceValidUntil'] = date('Y-12-31', strtotime('+1 year'));
                    $entity['offers']['hasMerchantReturnPolicy'] = $return_policy;
                    $entity['offers']['shippingDetails'] = $shipping_details;
                    $entity['offers']['seller'] = [
                        '@type' => 'HomeGoodsStore',
                        'name' => 'فروشگاه لوازم خانگی حسینی کالا اهواز',
                        'url' => 'https://hosseinykala.ir'
                    ];
                }
            }
        }
    }

    // 4.2. HOMEPAGE: Local Store Entity + Remove Article Schema
    if (is_front_page() || is_home()) {
        foreach ($data as $key => &$entity) {
            if (isset($entity['@type']) && (
                $entity['@type'] === 'Article' || 
                (is_array($entity['@type']) && in_array('Article', $entity['@type']))
            )) {
                unset($data[$key]);
                continue;
            }

            if (isset($entity['@type']) && (
                $entity['@type'] === 'Organization' ||
                (is_array($entity['@type']) && in_array('Organization', $entity['@type']))
            )) {
                $entity['@type'] = ['HomeGoodsStore', 'Store'];
                $entity['name'] = 'فروشگاه لوازم خانگی حسینی';
                $entity['alternateName'] = 'حسینی کالا اهواز';
                $entity['url'] = 'https://hosseinykala.ir';
                $entity['telephone'] = '09379725440';
                $entity['priceRange'] = '$$';
                $entity['address'] = [
                    '@type' => 'PostalAddress',
                    'streetAddress' => 'خوزستان، اهواز، مرکز شهر، خیابان کیوان، بین موسوی و علم الهدی',
                    'addressLocality' => 'اهواز',
                    'addressRegion' => 'خوزستان',
                    'addressCountry' => 'IR'
                ];
                $entity['geo'] = [
                    '@type' => 'GeoCoordinates',
                    'latitude' => 31.3200,
                    'longitude' => 48.6700
                ];
                $entity['openingHoursSpecification'] = [
                    [
                        '@type' => 'OpeningHoursSpecification',
                        'dayOfWeek' => ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday'],
                        'opens' => '09:00',
                        'closes' => '22:00'
                    ]
                ];
            }
        }
    }

    // 4.3. BLOG POSTS: E-E-A-T Author Persona (تیم کارشناسی حسینی کالا)
    if (is_singular('post')) {
        foreach ($data as $key => &$entity) {
            if (isset($entity['@type']) && ($entity['@type'] === 'BlogPosting' || $entity['@type'] === 'Article')) {
                $entity['author'] = [
                    '@type' => 'Person',
                    'name' => 'تیم کارشناسی حسینی کالا',
                    'jobTitle' => 'کارشناس ارشد لوازم خانگی و خرید اقساطی',
                    'description' => 'تیم تخصصی بررسی مشخصات فنی و شرایط خرید اقساطی فروشگاه حسینی کالا با بیش از ۲۶ سال سابقه در اهواز',
                    'url' => 'https://hosseinykala.ir/about-us/'
                ];
                $entity['publisher'] = [
                    '@type' => 'HomeGoodsStore',
                    'name' => 'فروشگاه لوازم خانگی حسینی',
                    'url' => 'https://hosseinykala.ir',
                    'logo' => [
                        '@type' => 'ImageObject',
                        'url' => 'https://hosseinykala.ir/wp-content/uploads/2026/07/cropped-logo.webp'
                    ]
                ];
            }
        }
    }

    return $data;
}, 99, 2);
'''

if 'ADVANCED SCHEMA.ORG' not in current_code:
    updated_code = current_code + "\n" + schema_php_block
else:
    # Replace existing block if already present
    idx = current_code.find('// 4. ADVANCED SCHEMA.ORG')
    if idx != -1:
        updated_code = current_code[:idx] + schema_php_block.strip()
    else:
        updated_code = current_code + "\n" + schema_php_block

# Update Snippet 7
payload = {
    'code': updated_code,
    'active': True
}

update_req = urllib.request.Request(
    'https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/7',
    headers=headers,
    data=json.dumps(payload).encode('utf-8'),
    method='POST'
)

with urllib.request.urlopen(update_req, timeout=15) as resp:
    res = json.loads(resp.read().decode('utf-8'))
    print("Snippet 7 updated with Phase 2 Schema Engine! Active:", res.get('active'))

# Purge cache
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

print("Phase 2 deployment complete.")
