import re

with open("divar_test.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's inspect chunk names or loadable chunks
chunks = re.findall(r'(\w+-[0-9a-f]+\.desktop\.js|\w+\.[0-9a-f]+\.desktop\.js)', html)
print("Chunks:", set(chunks))

# Let's see if there is any mention of pro in the html
pro_matches = re.findall(r'.{0,50}/pro/.{0,50}', html)
print("Pro matches in html:", pro_matches)
