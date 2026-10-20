import os
import io
import requests
from PIL import Image

AUTH = ('agent', 'Mlwg pHHX NQ64 drrz 7ca2 IVto')
BRAIN_DIR = r'C:\Users\mmhhs\.gemini\antigravity\brain\a254ee85-ba68-4053-b5cb-81ee7084ef3f'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

src_path = os.path.join(BRAIN_DIR, 'mehr_bnpl_cover_1789795433300.jpg')
img = Image.open(src_path).convert('RGB')
img = img.resize((1599, 900), Image.Resampling.LANCZOS)

buf = io.BytesIO()
img.save(buf, format='JPEG', quality=82, optimize=True)
size_kb = len(buf.getvalue()) / 1024
if size_kb > 120:
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=74, optimize=True)
    size_kb = len(buf.getvalue()) / 1024

print(f"Uploading mehr-iran-kalacard-bnpl-appliances-guide.jpg ({size_kb:.1f} KB)...")
upload_headers = {
    'User-Agent': HEADERS['User-Agent'],
    'Content-Type': 'image/jpeg',
    'Content-Disposition': 'attachment; filename="mehr-iran-kalacard-bnpl-appliances-guide.jpg"'
}
r = requests.post('https://hosseinykala.ir/wp-json/wp/v2/media', auth=AUTH, headers=upload_headers, data=buf.getvalue(), timeout=35)
if r.status_code in [200, 201]:
    data = r.json()
    mid = data['id']
    print(f"SUCCESS! Media ID: {mid}")
    requests.post(
        f'https://hosseinykala.ir/wp-json/wp/v2/media/{mid}',
        auth=AUTH,
        headers=HEADERS,
        json={
            'alt_text': 'مقایسه کالا کارت قرض الحسنه مهر ایران و روش های قسطی اسنپ پی و دیجی پی',
            'title': 'کالا کارت مهر ایران و روش های خرید اقساطی BNPL'
        }
    )
else:
    print(f"FAILED: {r.status_code} - {r.text[:200]}")
