import sys
import os
from PIL import Image, ImageStat

sys.stdout.reconfigure(encoding='utf-8')

def analyze_image_quality(image_path):
    if not os.path.exists(image_path):
        return {'status': 'error', 'message': 'File not found'}
    
    try:
        img = Image.open(image_path).convert('RGB')
        width, height = img.size
        
        # 1. Dimension Check
        is_high_res = width >= 600 and height >= 600
        
        # 2. Check corners and borders for watermarks using ImageStat
        cw, ch = max(20, int(width * 0.08)), max(20, int(height * 0.08))
        
        corner_boxes = {
            'top_left': (0, 0, cw, ch),
            'top_right': (width - cw, 0, width, ch),
            'bottom_left': (0, height - ch, cw, height),
            'bottom_right': (width - cw, height - ch, width, height)
        }
        
        corner_stats = {}
        has_potential_corner_watermark = False
        
        for name, box in corner_boxes.items():
            crop_box = img.crop(box)
            stat = ImageStat.Stat(crop_box)
            mean_brightness = sum(stat.mean) / 3.0
            std_dev = sum(stat.stddev) / 3.0
            
            # Pure white background: mean brightness is near 255, stddev near 0.
            # A logo or watermark causes dark pixels (lower mean) and high variation (higher stddev).
            is_suspicious = (mean_brightness < 240 and std_dev > 20)
            
            corner_stats[name] = {
                'mean_brightness': round(mean_brightness, 2),
                'std_variance': round(std_dev, 2),
                'suspicious': bool(is_suspicious)
            }
            if is_suspicious:
                has_potential_corner_watermark = True
                
        # Bottom bar check (often watermarks/credits are at the bottom center)
        bottom_box = (int(width * 0.2), height - int(height * 0.05), int(width * 0.8), height)
        bottom_crop = img.crop(bottom_box)
        bottom_stat = ImageStat.Stat(bottom_crop)
        bottom_mean = sum(bottom_stat.mean) / 3.0
        bottom_std = sum(bottom_stat.stddev) / 3.0
        bottom_bar_suspicious = (bottom_mean < 240 and bottom_std > 20)
        
        verdict = 'CLEAN'
        if not is_high_res:
            verdict = 'LOW_RESOLUTION'
        elif has_potential_corner_watermark or bottom_bar_suspicious:
            verdict = 'POSSIBLE_WATERMARK'
            
        return {
            'status': 'success',
            'width': width,
            'height': height,
            'is_high_res': is_high_res,
            'corner_stats': corner_stats,
            'bottom_bar_suspicious': bool(bottom_bar_suspicious),
            'verdict': verdict
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    if len(sys.argv) > 1:
        res = analyze_image_quality(sys.argv[1])
        import json
        print(json.dumps(res, indent=2))

