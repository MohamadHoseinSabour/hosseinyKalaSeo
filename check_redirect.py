import urllib.request

req = urllib.request.Request(
    'https://divar.ir/pro/xTlfvkBc',
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
)
try:
    with urllib.request.urlopen(req) as resp:
        print("Final URL:", resp.geturl())
        print("Status code:", resp.getcode())
        print("Headers:", dict(resp.headers))
except Exception as e:
    print("Error:", e)
