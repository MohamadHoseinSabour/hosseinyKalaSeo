import requests

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

# Fetch tags
r = requests.get('https://hosseinykala.ir/wp-json/wp/v2/tags?per_page=100', auth=AUTH, headers=HEADERS)
tags = {t['name'].strip(): t['id'] for t in r.json()}

target_names = ['خرید اقساطی لوازم خانگی', 'فروشگاه لوازم خانگی حسینی', 'خرید اقساطی در اهواز', 'کالا کارت مهر ایران']
tids = []
for name in target_names:
    if name in tags:
        tids.append(tags[name])
    else:
        r_c = requests.post('https://hosseinykala.ir/wp-json/wp/v2/tags', auth=AUTH, headers=HEADERS, json={'name': name})
        if r_c.status_code in [200, 201]:
            tids.append(r_c.json()['id'])

print("Assigning tags to 3861:", tids)
r_up = requests.post('https://hosseinykala.ir/wp-json/wp/v2/posts/3861', auth=AUTH, headers=HEADERS, json={'tags': tids})
print(f"Update status: {r_up.status_code}")
