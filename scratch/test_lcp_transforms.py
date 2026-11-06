import requests
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://hosseinykala.ir/', headers={'User-Agent': 'Mozilla/5.0'})
html = r.text

print("Original HTML size:", len(html))

# Test transform 1: Un-lazyload the hero banner
pattern_hero = r'(<img\b[^>]*clover-home-appliances-october-sale-banner[^>]*>)'
match = re.search(pattern_hero, html)
if match:
    old_tag = match.group(1)
    print("\nFound Hero img tag:")
    print("  Old tag:", old_tag[:200])
    
    # Extract data-xts-src
    src_match = re.search(r'data-xts-src=[\'"]([^\'"]+)[\'"]', old_tag)
    real_src = src_match.group(1) if src_match else "https://hosseinykala.ir/wp-content/uploads/2026/10/clover-home-appliances-october-sale-banner.webp"
    
    # Extract data-srcset
    srcset_match = re.search(r'data-srcset=[\'"]([^\'"]+)[\'"]', old_tag)
    real_srcset = srcset_match.group(1) if srcset_match else ""
    
    new_tag = old_tag
    # Replace src with real src
    new_tag = re.sub(r'src=[\'"][^\'"]*[\'"]', f'src="{real_src}"', new_tag)
    # Replace srcset with real srcset
    if real_srcset:
        new_tag = re.sub(r'srcset=[\'"][^\'"]*[\'"]', f'srcset="{real_srcset}"', new_tag)
    # Replace loading="lazy" with loading="eager" fetchpriority="high"
    new_tag = re.sub(r'loading=[\'"]lazy[\'"]', 'loading="eager" fetchpriority="high"', new_tag)
    if 'fetchpriority' not in new_tag:
        new_tag = new_tag.replace('<img ', '<img fetchpriority="high" ')
    # Remove lazy classes
    new_tag = new_tag.replace('xts-lazy-load', '').replace('xts-lazy-fade', '')
    
    print("\nTransformed Hero img tag:")
    print(" ", new_tag[:250])
else:
    print("Hero img tag not found!")

# Test transform 2: Un-lazyload logo
pattern_logo = r'(<img\b[^>]*xts-logo-main[^>]*>)'
match_logo = re.search(pattern_logo, html)
if match_logo:
    old_logo = match_logo.group(1)
    print("\nFound Logo img tag:")
    print("  Old tag:", old_logo[:150])
    
    new_logo = old_logo
    new_logo = re.sub(r'src=[\'"][^\'"]*base64[^\'"]*[\'"]', 'src="https://hosseinykala.ir/wp-content/uploads/2026/07/حسینی-کالا-300x62.webp"', new_logo)
    new_logo = re.sub(r'data-lazyloaded=[\'"][^\'"]*[\'"]', '', new_logo)
    if 'width=' not in new_logo:
        new_logo = new_logo.replace('<img ', '<img width="250" height="52" fetchpriority="high" ')
    print("  Transformed Logo tag:")
    print(" ", new_logo[:200])
