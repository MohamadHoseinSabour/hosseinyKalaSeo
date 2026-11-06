import urllib.request
import urllib.parse
import ssl
import sys

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

opener = urllib.request.build_opener(NoRedirect)
raw_url = 'https://hosseinykala.ir/product/یخچال-فریزر-دوقلو-40-فوت-کلور-مدل-گلوری-پ/'
parts = urllib.parse.urlsplit(raw_url)
encoded_url = urllib.parse.urlunsplit((parts.scheme, parts.netloc, urllib.parse.quote(parts.path), parts.query, parts.fragment))

req = urllib.request.Request(encoded_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = opener.open(req)
    print(f"Status: {resp.status}")
except urllib.error.HTTPError as e:
    loc = e.headers.get('Location', '')
    print(f"HTTP Status: {e.code} -> Location: {loc}")
