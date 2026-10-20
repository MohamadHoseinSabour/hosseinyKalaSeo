import os, sys, requests, mimetypes
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
SESSION = requests.Session()
SESSION.mount('https://', TLSAdapter())

def upload_media(file_path, title, alt_text):
    filename = os.path.basename(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = 'image/jpeg'
        
    with open(file_path, 'rb') as f:
        media_data = f.read()
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Content-Disposition': f'attachment; filename="{filename}"',
        'Content-Type': mime_type
    }
    
    url = 'https://hosseinykala.ir/wp-json/wp/v2/media'
    r = SESSION.post(url, auth=AUTH, headers=headers, data=media_data, timeout=30)
    if r.status_code == 201:
        res = r.json()
        media_id = res['id']
        source_url = res['source_url']
        print(f"Uploaded: {filename} -> ID: {media_id} ({source_url})")
        
        # update title & alt_text
        update_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Content-Type': 'application/json'
        }
        update_payload = {
            'title': title,
            'alt_text': alt_text,
            'description': alt_text
        }
        r_up = SESSION.post(f"{url}/{media_id}", auth=AUTH, headers=update_headers, json=update_payload, timeout=15)
        print("Updated meta status:", r_up.status_code)
        return media_id, source_url
    else:
        print(f"Upload failed: {r.status_code} - {r.text[:200]}")
        return None, None

# Test with scratch/ziko_5020_box.jpg
mid, url = upload_media('scratch/ziko_5020_box.jpg', 'سشوار حرفه ای زیکو مدل ZC-5020', 'عکس سشوار حرفه ای ۲۶۰۰ وات زیکو مدل 5020')
print("Result:", mid, url)
