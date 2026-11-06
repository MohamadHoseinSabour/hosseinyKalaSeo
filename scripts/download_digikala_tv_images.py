import requests
import re
from PIL import Image

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

sources = {
    'toshiba_55.jpg': 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHH4c4MhVD2Pcc2gIIeCYoyilv13Jm8XoYokxdZs9lFkrLQHM-9cX4UyIu3EbxGv2pqeKptNldVepTy_1SNjOABlNI3JH0CoFQeyoMweRooLmrLcJk3fXRQkodAvkoDAlICMrg6i6hmnplFyg==',
    'toshiba_50.jpg': 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGrwrqk4FplFuPpzyAV4AkAvz1ZneftktDb2PUYI-30htELKTf1QyZhebV_NMxUnM6x2RIn0aWuvrX2k7N3dedrmfDUsaRMKH8lLBg511KzQJoKTMcu9AYqhhAwgXsWGAxYOM5gC2ppCaxpCI9GMQ1f_KgfQYsEgTJdyXRp1LMf9Xw7bDIlWv6Nk243rTXb1pIGH4ZoamdJ6RXK2W0XBoSXv3NR6RMJShNZbqNdmyuPGfeHtL0kS82VOihczqsHgtwFSiGn-J3LqOXrYNT8tbqx8lI765d7CgFEffTDDL45oERjdqg3R0fZPXreYUF-uFpF3do7ZvCq3WuiWWyNz1kQKKHAgcjldjThNy4MisB-iXcQkVLadgHajJ-xgcDYaBXC5fxgW5MygApWtL3Qe5sRgKzBZKPDygT2rEigDJw=',
    'toshiba_43.jpg': 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHcN53rcAJ6-YB13Rad6mZ_L8GFSHGRm82Lx7zChxsc0IR_WGv5s5zQG35ar9tAKI4fNaeDRUOMx7Qx1BT6iQ6louJ9jQ3diqkpncXm73P5RcoP8tWimSTiINeJXGbIhYq-nL-uhAUcu2sYS_Fo_AXjD3rMzqIWH7rPxdNxrnU0B98S_m9BsMIs3qaU-vn8ZsA3so1att0U3X0AJXhOjW8D9my6-UsJDSwIhPtQMJRCS66Fbeq13S2CWoHg_bkgLkf1n7rTxOsSI1eQSCHKub246cHVC5q8-BlVVpuRa19oD6FXC3e-w9dnuQdaJKl2VzHhY8reORbE0Eg1r00U6Z3cJT4YjzxJ4BnEsYFRMlJlupSEAVWNDnt4mU_-OT4f8VzEz1sNZsp16Q6nnOL3WyVPoIc8nOU9Qhv17CP7kg==',
    'hisense_43.jpg': 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHJZzME-QBraAFugHcaIWs48JKtHCIRHllyiOzwyiNDpdEJjx-VIC-rSj7LMl0opGQ0I24n7BorGRhmG1KvNk5MrQV-SVUc1kLxWFgZBFDKeWeKl5wj5p_bvP0xKAgY9_AVIFAHbYqUJbRDPWeQdAnSvJtFUiwpQzn6Wa42exXsgNe6cncYdiZNSSL71mlzPoHQpsr0ODgpfGpsxn6umLcV50qVBCnbckEd8IYDi94YGwwMT9IdSIOZOr3jWdtXgDmBuOxxX3llhAmJDM88AL2rqD0JexgEGtOyVhzfDFjPuQDOiWZYCnyddLdAc9l52QrOmZxHWzHVWgkKW5rM70CYgVGrUacGNZI9oLohljDSPU41-1EZXWh7gg8FNRNHXSXhoHXolLsAZ2dcOQ299YOohvHMWU8S9ZJoQJ8='
}

for fname, red_url in sources.items():
    try:
        r = requests.get(red_url, allow_redirects=True, headers=headers, timeout=12)
        print(f"{fname} resolved to: {r.url}")
        og = re.search(r'property="og:image"\s+content="([^"]+)"', r.text)
        if og:
            img_url = og.group(1)
            print(f"  OG Image: {img_url}")
            r_img = requests.get(img_url, headers=headers, timeout=12)
            if r_img.status_code == 200:
                with open(f'scratch/new_tvs_raw/{fname}', 'wb') as f:
                    f.write(r_img.content)
                im = Image.open(f'scratch/new_tvs_raw/{fname}')
                print(f"  ✓ Saved {fname}: {im.size}")
        else:
            print(f"  No og:image found for {fname}")
    except Exception as e:
        print(f"  Error {fname}: {e}")
