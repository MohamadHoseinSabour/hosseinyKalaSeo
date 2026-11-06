import urllib.request
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

urls = {
    'Shop': 'https://hosseinykala.ir/shop/',
    'Product': 'https://hosseinykala.ir/product/depoint-decent-combi-refrigerator-freezer/',
    'Contact': 'https://hosseinykala.ir/contact/',
    'Blog': 'https://hosseinykala.ir/blog/'
}

for name, url in urls.items():
    print(f"\n==========================================")
    print(f"Inspecting {name} ({url})")
    print(f"==========================================")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
        print(f"HTML Size: {len(html)} bytes")
        
        # Check preloads
        preloads = re.findall(r'<link[^>]*rel=[\"\']preload[\"\'][^>]*>', html, re.I)
        print(f"Preloads count: {len(preloads)}")
        for p in preloads[:5]:
            print(f"  {p}")
            
        # Check stylesheets
        css = re.findall(r'<link[^>]*stylesheet[^>]*>', html, re.I)
        print(f"Stylesheets count: {len(css)}")
        
        # Check images and first image (likely LCP)
        images = re.findall(r'<img[^>]+>', html, re.I)
        print(f"Images count: {len(images)}")
        if images:
            print("  First 2 images:")
            for img in images[:2]:
                print(f"    {img[:150]}...")
                
        # Check scripts
        scripts = re.findall(r'<script[^>]*src=[\"\']([^\"\']+)[\"\'][^>]*>', html, re.I)
        print(f"External scripts: {len(scripts)}")
        
    except Exception as e:
        print(f"Error fetching {name}: {e}")
