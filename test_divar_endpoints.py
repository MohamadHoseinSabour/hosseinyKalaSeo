import urllib.request
import json

token = "xTlfvkBc"
endpoints = [
    f"https://api.divar.ir/v8/places/{token}",
    f"https://api.divar.ir/v8/pro-user/{token}",
    f"https://api.divar.ir/v8/premium-user/{token}",
    f"https://api.divar.ir/v8/store/{token}",
    f"https://api.divar.ir/v8/marketplace/{token}",
    f"https://api.divar.ir/v8/web-search/{token}",
    f"https://api.divar.ir/v8/posts/{token}",
    f"https://api.divar.ir/v8/users/{token}",
    f"https://api.divar.ir/v8/business/{token}",
    f"https://api.divar.ir/v8/business-card/{token}",
    f"https://api.divar.ir/v8/dealers/{token}",
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
}

for ep in endpoints:
    try:
        req = urllib.request.Request(ep, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode('utf-8')
            print(f"SUCCESS {ep} -> Status {resp.getcode()}, Len: {len(data)}")
            with open("found_endpoint.json", "w", encoding="utf-8") as out:
                out.write(data)
            break
    except urllib.error.HTTPError as e:
        print(f"HTTPError {e.code} for {ep}")
    except Exception as e:
        print(f"Error {e} for {ep}")
