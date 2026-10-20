import sys
import json
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
BASE_URL = 'https://hosseinykala.ir'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

def check_url(url, allow_redirects=False):
    try:
        r = requests.get(url, headers=HEADERS, allow_redirects=allow_redirects, timeout=15)
        return {
            'url': url,
            'status': r.status_code,
            'redirect_to': r.headers.get('Location') if not allow_redirects else r.url,
            'final_url': r.url if allow_redirects else None,
            'ok': r.status_code == 200 or (not allow_redirects and r.status_code in [301, 302])
        }
    except Exception as e:
        return {'url': url, 'status': f'ERR: {e}', 'ok': False}

def main():
    print("======================================================================")
    print("🚀 STARTING COMPREHENSIVE QA & SEO AUDIT FOR HOSSEINYKALA.IR")
    print("======================================================================\n")

    audit_report = {
        'slugs_and_redirects': [],
        'article_audits': {},
        'meta_and_titles': []
    }

    # ---------------------------------------------------------
    # PART 1: Slugs & 301 Redirects Verification
    # ---------------------------------------------------------
    print("--- [1/3] VERIFYING SLUGS AND 301 REDIRECTS ---")
    slug_pairs = [
        # (Type, ID, Label, Old Persian URL, New English URL)
        ("post", 3000, "کولر آبی سلولزی و پرتابل",
         "https://hosseinykala.ir/راهنمای-خرید-کولر-آبی-سلولزی-و-پرتابل؛/",
         "https://hosseinykala.ir/portable-cellulose-air-cooler-guide/"),
        ("post", 3098, "یخچال کوچک هتلی",
         "https://hosseinykala.ir/راهنمای-خرید-یخچال-کوچک-هتلی/",
         "https://hosseinykala.ir/mini-hotel-refrigerator-buying-guide/"),
        ("post", 3099, "ماشین ظرفشویی ۱۵ نفره",
         "https://hosseinykala.ir/راهنمای-خرید-ماشین-ظرفشویی-۱۵-نفره/",
         "https://hosseinykala.ir/15-place-dishwasher-buying-guide/"),
        ("post", 3100, "یخچال کمبی یا دوقلو",
         "https://hosseinykala.ir/یخچال-کمبی-یا-دوقلو/",
         "https://hosseinykala.ir/combi-vs-twin-refrigerator-guide/"),
        ("post", 3101, "بررسی برند کلور",
         "https://hosseinykala.ir/بررسی-تخصصی-برند-کلور/",
         "https://hosseinykala.ir/clover-brand-review/"),
        ("post", 3102, "چک لیست خرید جهیزیه",
         "https://hosseinykala.ir/چک-لیست-خرید-جهیزیه-اقتصادی/",
         "https://hosseinykala.ir/economical-dowry-checklist-guide/"),
        ("product", 3453, "الکترواستیل فیوچر دوقلو ۲۱ فوت",
         "https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-21-فوت-الکترواستیل-مدل/",
         "https://hosseinykala.ir/product/electrosteel-future-twin-refrigerator-21ft/"),
        ("product", 2972, "کلور گلوری پلاس دوقلو ۵۴ فوت",
         "https://hosseinykala.ir/product/یخچال-فریزر-گلوری-پلاس-دوقلو-کلور54-فوت/",
         "https://hosseinykala.ir/product/clover-glory-plus-54ft-twin-refrigerator/"),
        ("product", 3395, "هیمالیا آلفا دوقلو ۲۸ فوت",
         "https://hosseinykala.ir/product/یخچال-و-فریزر-دوقلو-28-فوت-هیمالیا-مدل-آ/",
         "https://hosseinykala.ir/product/himalia-alpha-twin-refrigerator-28ft/"),
        ("product", 3266, "پاکشوما اسپلیت ۱۸۰۰۰",
         "https://hosseinykala.ir/product/کولر-گازی-اسپلیت-دیواری-18000-دور-ثابت-پا/",
         "https://hosseinykala.ir/product/pakshoma-18000-split-air-conditioner/")
    ]

    for item_type, item_id, label, old_url, new_url in slug_pairs:
        # Check new English URL
        res_new = check_url(new_url, allow_redirects=False)
        # Check old Persian URL redirect
        res_old = check_url(old_url, allow_redirects=False)
        # Follow redirect of old URL to see if it reaches 200 at new_url
        res_old_follow = check_url(old_url, allow_redirects=True)

        is_passed = (res_new['status'] == 200 and res_old['status'] in [301, 302] and res_old_follow['status'] == 200)
        status_text = "PASS ✅" if is_passed else "FAIL ❌"
        print(f"[{status_text}] {item_type.upper()} {item_id} ({label}):")
        print(f"   - New URL: {new_url} -> Status: {res_new['status']}")
        print(f"   - Old URL: {old_url} -> Status: {res_old['status']} -> Redirect To: {res_old.get('redirect_to')}")
        print(f"   - Final Destination: {res_old_follow.get('final_url')} (Status: {res_old_follow['status']})\n")

        audit_report['slugs_and_redirects'].append({
            'type': item_type,
            'id': item_id,
            'label': label,
            'new_url': new_url,
            'new_status': res_new['status'],
            'old_url': old_url,
            'old_status': res_old['status'],
            'redirect_to': res_old.get('redirect_to'),
            'final_status': res_old_follow['status'],
            'passed': is_passed
        })

    # ---------------------------------------------------------
    # PART 2: In-Depth Content & Internal Links Audit for Articles 2932 and 2926
    # ---------------------------------------------------------
    print("--- [2/3] AUDITING CONTENT & INTERNAL LINKS (POSTS 2932 & 2926) ---")
    target_posts = [
        {
            'id': 2926,
            'title': 'راهنمای خرید یخچال فریزر دوقلو',
            'api_endpoint': f'{BASE_URL}/wp-json/wp/v2/posts/2926'
        },
        {
            'id': 2932,
            'title': 'راهنمای خرید ماشین لباسشویی ۸ و ۹ کیلویی',
            'api_endpoint': f'{BASE_URL}/wp-json/wp/v2/posts/2932'
        }
    ]

    for post_info in target_posts:
        pid = post_info['id']
        print(f"\nAuditing Post {pid} ({post_info['title']})...")
        r = requests.get(post_info['api_endpoint'], auth=AUTH, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            print(f"❌ Failed to fetch Post {pid}: HTTP {r.status_code}")
            continue

        pdata = r.json()
        raw_html = pdata.get('content', {}).get('rendered', '')
        soup = BeautifulSoup(raw_html, 'html.parser')

        # Word count & Character count
        plain_text = soup.get_text()
        words = plain_text.split()
        word_count = len(words)
        char_count = len(plain_text)

        # Check tables
        tables = soup.find_all('table')
        table_count = len(tables)

        # Find all anchor tags
        anchors = soup.find_all('a', href=True)
        link_details = []
        forbidden_p_count = 0
        forbidden_cat_count = 0
        canonical_cat_links = []
        homepage_links = []

        for a in anchors:
            href = a['href']
            text = a.get_text().strip()
            
            # Internal links check
            if '?p=' in href:
                forbidden_p_count += 1
            if '?product_cat=' in href:
                forbidden_cat_count += 1

            if '/product-category/' in href:
                canonical_cat_links.append({'url': href, 'text': text})

            if href.rstrip('/') == BASE_URL or href == BASE_URL + '/':
                homepage_links.append({'url': href, 'text': text})

            # Check live status of link
            if href.startswith('http') and 'hosseinykala.ir' in href:
                res = check_url(href, allow_redirects=True)
                link_details.append({
                    'href': href,
                    'text': text,
                    'status': res['status'],
                    'final_url': res.get('final_url')
                })

        # Check Ahvaz mentions
        has_ahvaz = 'اهواز' in plain_text

        print(f"   - Word Count: {word_count} words ({char_count} chars)")
        print(f"   - Tables Count: {table_count} table(s)")
        print(f"   - Total Internal Links: {len(link_details)}")
        print(f"   - Forbidden '?p=' Links: {forbidden_p_count} {'✅ NONE' if forbidden_p_count == 0 else '❌ DETECTED'}")
        print(f"   - Forbidden '?product_cat=' Links: {forbidden_cat_count} {'✅ NONE' if forbidden_cat_count == 0 else '❌ DETECTED'}")
        print(f"   - Canonical Category Links: {len(canonical_cat_links)}")
        for cl in canonical_cat_links:
            print(f"       * {cl['text']} -> {unquote(cl['url'])}")
        print(f"   - Homepage Anchor: {[h['text'] for h in homepage_links]}")
        print(f"   - Mention of Ahvaz: {'✅ YES' if has_ahvaz else '❌ NO'}")

        # Check all link HTTP status
        broken_links = [l for l in link_details if l['status'] != 200]
        if broken_links:
            print(f"   ❌ Broken links detected: {broken_links}")
        else:
            print(f"   ✅ All {len(link_details)} internal links returned HTTP 200 OK!")

        audit_report['article_audits'][pid] = {
            'title': pdata.get('title', {}).get('rendered'),
            'slug': pdata.get('slug'),
            'link': pdata.get('link'),
            'word_count': word_count,
            'char_count': char_count,
            'tables_count': table_count,
            'forbidden_p_count': forbidden_p_count,
            'forbidden_cat_count': forbidden_cat_count,
            'canonical_cat_links': canonical_cat_links,
            'homepage_anchors': [h['text'] for h in homepage_links],
            'has_ahvaz': has_ahvaz,
            'all_links_status_200': len(broken_links) == 0,
            'link_details': link_details
        }

    # ---------------------------------------------------------
    # PART 3: Titles & Rank Math SEO Metadata Verification
    # ---------------------------------------------------------
    print("\n--- [3/3] VERIFYING TITLES AND RANK MATH SEO METADATA ---")
    items_to_audit_meta = [
        # (type, id, label)
        ('post', 3000, 'کولر آبی سلولزی و پرتابل'),
        ('post', 3098, 'یخچال کوچک هتلی'),
        ('post', 3100, 'یخچال کمبی یا دوقلو'),
        ('post', 2926, 'راهنمای خرید یخچال دوقلو'),
        ('post', 2932, 'راهنمای خرید ماشین لباسشویی'),
        ('product', 2885, 'جاروبرقی بست BVC-PC18B'),
        ('product', 2538, 'کولر پرتابل ریتون ۱۶۰۰۰'),
        ('product', 3056, 'ماشین اصلاح پرو امگا T5'),
        ('product', 3453, 'یخچال دوقلو الکترواستیل فیوچر'),
        ('product', 2972, 'یخچال دوقلو کلور گلوری پلاس'),
        ('product', 3395, 'یخچال دوقلو هیمالیا آلفا'),
        ('product', 3266, 'کولر گازی پاکشوما ۱۸۰۰۰')
    ]

    for itype, iid, ilabel in items_to_audit_meta:
        endpoint = f"{BASE_URL}/wp-json/wp/v2/{'posts' if itype == 'post' else 'product'}/{iid}"
        r = requests.get(endpoint, auth=AUTH, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            print(f"❌ Failed to fetch {itype} {iid}: HTTP {r.status_code}")
            continue

        idata = r.json()
        raw_title = idata.get('title', {}).get('rendered', '')
        meta = idata.get('meta', {})
        rm_title = meta.get('rank_math_title', '')
        rm_desc = meta.get('rank_math_description', '')
        rm_keyword = meta.get('rank_math_focus_keyword', '')

        # CTR Triggers check
        triggers = ['قیمت', 'خرید', 'ضمانت', 'گارانتی', 'ابعاد', 'اهواز', 'انتخاب سرویس', 'بهترین', 'بررسی', '۱۴۰۵']
        matched_triggers = [t for t in triggers if t in (rm_title + ' ' + rm_desc + ' ' + raw_title)]

        print(f"\n[{itype.upper()} {iid}] {ilabel}")
        print(f"   - Title: {raw_title}")
        print(f"   - Rank Math Title: {rm_title if rm_title else '⚠️ EMPTY'}")
        print(f"   - Rank Math Focus Keyword: {rm_keyword if rm_keyword else '⚠️ EMPTY'}")
        print(f"   - Rank Math Desc: {rm_desc[:90]}... (Len: {len(rm_desc)})" if rm_desc else "   - Rank Math Desc: ⚠️ EMPTY")
        print(f"   - CTR Triggers: {matched_triggers}")

        audit_report['meta_and_titles'].append({
            'type': itype,
            'id': iid,
            'label': ilabel,
            'raw_title': raw_title,
            'rm_title': rm_title,
            'rm_desc': rm_desc,
            'rm_keyword': rm_keyword,
            'matched_triggers': matched_triggers
        })

    with open('data/comprehensive_qa_seo_audit.json', 'w', encoding='utf-8') as f:
        json.dump(audit_report, f, ensure_ascii=False, indent=2)

    print("\n======================================================================")
    print("✅ AUDIT COMPLETED! Results saved to data/comprehensive_qa_seo_audit.json")
    print("======================================================================")

if __name__ == '__main__':
    main()
