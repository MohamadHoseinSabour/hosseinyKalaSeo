import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

RAW_DIR = 'scratch/new_tvs_raw'
OUT_DIR = 'scratch/new_tvs_processed'
os.makedirs(OUT_DIR, exist_ok=True)

files = {
    'xvision_43.jpg': 'xvision-43-inch-43xt515-smart-tv.webp',
    'toshiba_50.jpg': 'toshiba-50-inch-50l2300ee-led-tv.webp',
    'toshiba_55.jpg': 'toshiba-55-inch-4k-smart-led-tv.webp',
    'toshiba_43.jpg': 'toshiba-43-inch-fhd-led-tv.webp',
    'hisense_43.jpg': 'hisense-43-inch-4k-smart-tv.webp'
}

for in_name, out_name in files.items():
    in_path = os.path.join(RAW_DIR, in_name)
    out_path = os.path.join(OUT_DIR, out_name)
    im = Image.open(in_path)
    
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        im_rgba = im.convert('RGBA')
        bg = Image.new('RGB', im_rgba.size, (255, 255, 255))
        bg.paste(im_rgba, mask=im_rgba.split()[3])
        im_rgb = bg
    else:
        im_rgb = im.convert('RGB')
    
    w, h = im_rgb.size
    max_dim = max(w, h)
    pad_dim = int(max_dim * 1.08) # 8% padding
    canvas = Image.new('RGB', (pad_dim, pad_dim), (255, 255, 255))
    paste_x = (pad_dim - w) // 2
    paste_y = (pad_dim - h) // 2
    canvas.paste(im_rgb, (paste_x, paste_y))
    
    canvas_resized = canvas.resize((1000, 1000), Image.Resampling.LANCZOS)
    canvas_resized.save(out_path, 'WEBP', quality=88)
    
    sz_kb = os.path.getsize(out_path) / 1024
    print(f"✓ {out_name}: (1000, 1000), {sz_kb:.1f} KB")
