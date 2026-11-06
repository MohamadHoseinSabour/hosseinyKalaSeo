import json

full_transcript_path = r'C:/Users/mmhhs/.gemini/antigravity/brain/1f248730-479c-4c28-869b-1c3bac549b81/.system_generated/logs/transcript_full.jsonl'

with open(full_transcript_path, 'r', encoding='utf-8') as f:
    full_lines = f.readlines()

for i in range(len(full_lines)-15, len(full_lines)):
    d = json.loads(full_lines[i])
    s_idx = d.get('step_index')
    t = d.get('type')
    c_len = len(d.get('content', ''))
    print(f"Line {i} | step_index={s_idx} | type={t} | len={c_len}")
    if t == 'USER_INPUT':
        print("  Snippet:", repr(d.get('content', '')[:100]))
