import subprocess
import sys

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
cmd = [
    chrome_path,
    '--headless=new',
    '--disable-gpu',
    '--virtual-time-budget=10000',
    '--dump-dom',
    'https://divar.ir/pro/xTlfvkBc'
]

print("Running chrome...")
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')
print("Return code:", res.returncode)
print("Stdout length:", len(res.stdout))
print("Stderr length:", len(res.stderr))

if len(res.stdout) > 0:
    with open("chrome_dump.html", "w", encoding="utf-8") as f:
        f.write(res.stdout)
    print("Saved chrome_dump.html")
if len(res.stderr) > 0:
    print("Stderr preview:", res.stderr[:500])
