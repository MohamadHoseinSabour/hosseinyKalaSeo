with open('scratch/af_block_0.js', 'r', encoding='utf-8') as f:
    text = f.read()

print("Length:", len(text))
print("First 800 chars:\n", text[:800])

# Search for accessibility or performance
import re
for word in ['Accessibility', 'accessibility', 'Performance', 'performance', 'FCP', 'LCP', 'CLS', 'Best Practices', 'SEO']:
    matches = [m.start() for m in re.finditer(word, text, re.IGNORECASE)]
    print(f"Keyword '{word}': {len(matches)} occurrences")
    if matches:
        first_idx = matches[0]
        print(f"  Context for '{word}':\n", text[max(0, first_idx-50):min(len(text), first_idx+200)])
