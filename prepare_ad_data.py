import os
import sys
import re
import json

DIVAR_ADS_DIR = "divar_ads"

def clean_separator_lines(text):
    lines = text.split("\n")
    # Remove any separator line containing only dashes, equals, underscores, etc.
    filtered = []
    for line in lines:
        stripped = line.strip()
        # If line is only dashes/dividers like ───────── or ═════════ or -----------
        if stripped and re.match(r"^[\s─=\-_*~•—]+$", stripped):
            continue
        filtered.append(line)
        
    res = "\n".join(filtered).strip()
    # Strip any leading dashes or punctuation
    res = re.sub(r"^[\s─=\-_*~•—\n]+", "", res).strip()
    return res

def condense_ad_text(text, max_len=920):
    # Extract ad title
    title_match = re.search(r"【 عنوان آگهی دیوار.*?】\s*\n([^\n]+)", text)
    title = title_match.group(1).strip() if title_match else ""
    
    # Extract ad body
    body_part = text
    if "📝 متن کامل آگهی جهت کپی در دیوار:" in text:
        body_part = text.split("📝 متن کامل آگهی جهت کپی در دیوار:")[-1].strip()
    elif "====================" in text:
        body_part = text.split("====================")[-1].strip()

    # Clean separators
    cleaned_body = clean_separator_lines(body_part)

    # Clean redundant empty lines
    lines = [line.strip() for line in cleaned_body.split("\n")]
    clean_lines = []
    prev_empty = False
    for line in lines:
        if not line:
            if not prev_empty:
                clean_lines.append("")
                prev_empty = True
        else:
            clean_lines.append(line)
            prev_empty = False
            
    condensed = "\n".join(clean_lines).strip()
    
    # If still > max_len, trim intelligently while keeping disclaimer and contact
    if len(condensed) > max_len:
        condensed = re.sub(r"🌐 مشاهده کاتالوگ آنلاین.*?\n.*?(?=\n|$)", "", condensed)
        condensed = re.sub(r"https?://\S+", "", condensed)
        condensed = re.sub(r"\n{3,}", "\n\n", condensed).strip()
        
    if len(condensed) > max_len:
        condensed = condensed[:max_len]
        if "\n" in condensed:
            condensed = condensed.rsplit("\n", 1)[0]
            
    # Final check: Ensure no separator is at the top
    condensed = clean_separator_lines(condensed)
            
    return title, condensed

def main():
    folders = sorted([d for d in os.listdir(DIVAR_ADS_DIR) if os.path.isdir(os.path.join(DIVAR_ADS_DIR, d))])
    all_ads = []
    
    for folder in folders:
        folder_path = os.path.join(DIVAR_ADS_DIR, folder)
        txt_path = os.path.join(folder_path, "ad_content.txt")
        img_dir = os.path.join(folder_path, "images")
        
        if not os.path.exists(txt_path):
            continue
            
        with open(txt_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
            
        title, clean_content = condense_ad_text(raw_text)
        
        images = []
        if os.path.exists(img_dir):
            images = [os.path.abspath(os.path.join(img_dir, f)) for f in sorted(os.listdir(img_dir)) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
        ad_obj = {
            "folder": folder,
            "title": title,
            "content": clean_content,
            "content_length": len(clean_content),
            "images": images[:10]  # Divar accepts up to 10 images
        }
        all_ads.append(ad_obj)
        
        with open(os.path.join(folder_path, "clean_ad.txt"), "w", encoding="utf-8") as f:
            f.write(f"TITLE: {title}\nCHARS: {len(clean_content)}\n\n{clean_content}")

    with open("divar_prepared_ads.json", "w", encoding="utf-8") as f:
        json.dump(all_ads, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully processed {len(all_ads)} ads.")

if __name__ == "__main__":
    main()
