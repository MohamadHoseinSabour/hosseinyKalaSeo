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

req = urllib.request.Request(
    'https://hosseinykala.ir/wp-json/code-snippets/v1/snippets/7',
    headers=headers
)
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode('utf-8'))

current_code = data.get('code', '')

# Code for llms.txt & dynamic Image Alt optimization
llms_and_alt_block = r'''
// =========================================================================
// 5. LLMS.TXT (GEO / AGENTIC SEARCH) & DYNAMIC IMAGE ALT ENGINE (Phase 3 & 4)
// =========================================================================
add_action('init', function () {
    if (isset($_SERVER['REQUEST_URI'])) {
        $uri = trim(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH), '/');
        if ($uri === 'llms.txt') {
            header('Content-Type: text/plain; charset=utf-8');
            header('Cache-Control: public, max-age=86400');
            echo "# فروشگاه لوازم خانگی حسینی کالا (Hosseiny Kala)\n\n";
            echo "> مرجع تخصصی بررسی و خرید نقد و اقساطی انواع لوازم خانگی در اهواز با بیش از ۲۶ سال سابقه و ارسال به سراسر کشور.\n\n";
            echo "## مشخصات و اطلاعات تماس\n";
            echo "- وب‌سایت رسمی: https://hosseinykala.ir\n";
            echo "- استقرار شعب حضوری: خوزستان، اهواز، مرکز شهر، خیابان کیوان، بین موسوی و علم الهدی\n";
            echo "- تلفن هماهنگی و مشاوره: 09379725440\n\n";
            echo "## دسته‌بندی‌های اصلی کاتالوگ\n";
            echo "- [یخچال فریزر](https://hosseinykala.ir/product-category/%db%8c%d8%ae%da%86%d8%a7%d9%84-%d9%81%d8%b1%db%8c%d8%b2%d8%b1/): انواع یخچال فریزر دوقلو، ساید و کمبی از برندهای کلور، دیپوینت، ایستکول و الکترواستیل.\n";
            echo "- [ماشین لباسشویی](https://hosseinykala.ir/product-category/washing-cleaning/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d9%84%d8%a8%d8%a7%d8%b3%d8%b4%d9%88%db%8c%db%8c/): مدل‌های اتوماتیک اینورتر با گارانتی معتبر.\n";
            echo "- [ماشین ظرفشویی](https://hosseinykala.ir/product-category/washing-cleaning/%d9%85%d8%a7%d8%b4%db%8c%d9%86-%d8%b8%d8%b1%d9%81%d8%b4%d9%88%db%8c%db%8c/): مدل‌های مبله و رومیزی کم‌مصرف.\n";
            echo "- [کولر آبی](https://hosseinykala.ir/product-category/heating-cooling/%da%a9%d9%88%d9%84%d8%b1-%d8%a2%d8%a8%db%8c/): انواع کولر آبی پرقدرت مناسب آب‌وهوای خوزستان.\n";
            echo "- [جاروبرقی](https://hosseinykala.ir/product-category/washing-cleaning/%d8%ac%d8%a7%d8%b1%d9%88%d8%a8%d8%b1%d9%82%db%8c/): مدل‌های کیسه‌ای و مخزنی با مکش بالا.\n\n";
            echo "## راهنماهای خرید اقساطی\n";
            echo "- [راهنمای جامع خرید اقساطی لوازم خانگی](https://hosseinykala.ir/home-appliances-installment-buying-guide/): مقایسه وام بتا رفاه، باجت تجارت، فرابانک ملت و خرید با چک صیادی در اهواز.\n";
            exit;
        }
        if ($uri === 'llms-full.txt') {
            header('Content-Type: text/plain; charset=utf-8');
            header('Cache-Control: public, max-age=86400');
            echo "# Hosseiny Kala Full Catalog & Knowledge Base\n";
            echo "> Comprehensive appliance catalog and purchase terms for https://hosseinykala.ir\n";
            exit;
        }
    }
}, 1);
'''

# Update Snippet 7 with alt replacement inside the output buffer
# Replace existing snippet code to ensure buffer has alt filler
target_str = "return $buffer;\n    });"
alt_code = r'''
        // 3.5. Ensure every <img> tag has a descriptive Persian Alt attribute
        $buffer = preg_replace_callback(
            '/<img\b((?:(?!\balt=)[^>])*)>/i',
            function ($matches) {
                return '<img alt="لوازم خانگی حسینی کالا اهواز"' . $matches[1] . '>';
            },
            $buffer
        );
        $buffer = str_replace('alt=""', 'alt="فروشگاه لوازم خانگی حسینی کالا اهواز"', $buffer);
        $buffer = str_replace("alt=''", 'alt="فروشگاه لوازم خانگی حسینی کالا اهواز"', $buffer);

        return $buffer;
    });'''

if '3.5. Ensure every <img>' not in current_code:
    if target_str in current_code:
        current_code = current_code.replace(target_str, alt_code, 1)

if '5. LLMS.TXT' not in current_code:
    updated_code = current_code + "\n" + llms_and_alt_block
else:
    updated_code = current_code

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
    print("Snippet 7 updated with LLMS.txt & Alt Engine! Active:", res.get('active'))

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

print("Phases 3 & 4 deployment complete.")
