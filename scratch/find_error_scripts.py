import urllib.request
import base64
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

creds = base64.b64encode(b'agent:Mlwg pHHX NQ64 drrz 7ca2 IVto').decode('utf-8')

# 1. Fetch as logged-in editor
req_auth = urllib.request.Request('https://hosseinykala.ir/', headers={
    'Authorization': 'Basic ' + creds,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})
try:
    with urllib.request.urlopen(req_auth) as resp:
        html_auth = resp.read().decode('utf-8', errors='ignore')
        print(f"Logged-in HTML length: {len(html_auth)}")
        
        # Search for inline scripts referencing jQuery, wp, i18n
        for m in re.finditer(r'<script([^>]*)>(.*?)</script>', html_auth, re.DOTALL):
            attrs = m.group(1)
            code = m.group(2).strip()
            if 'wp.i18n' in code or 'wp-i18n' in attrs or 'elementor-common-js-translations' in attrs or 'elementor-common' in code:
                print("\n[MATCH IN LOGGED IN]")
                print("ATTRS:", attrs)
                print("CODE:", code[:200])
except Exception as e:
    print("Error fetching logged in:", e)

# 2. Check guest HTML as well
req_guest = urllib.request.Request('https://hosseinykala.ir/', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})
try:
    with urllib.request.urlopen(req_guest) as resp:
        html_guest = resp.read().decode('utf-8', errors='ignore')
        print(f"\nGuest HTML length: {len(html_guest)}")
        for m in re.finditer(r'<script([^>]*)>(.*?)</script>', html_guest, re.DOTALL):
            attrs = m.group(1)
            code = m.group(2).strip()
            if 'wp.i18n' in code or 'wp-i18n' in attrs or 'elementor-common-js-translations' in attrs:
                print("\n[MATCH IN GUEST]")
                print("ATTRS:", attrs)
                print("CODE:", code[:200])
except Exception as e:
    print("Error fetching guest:", e)
