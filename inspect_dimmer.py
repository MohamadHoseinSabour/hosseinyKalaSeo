from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

soup = BeautifulSoup(open('wizard_step2.html', encoding='utf-8'), 'html.parser')
dimmers = soup.find_all('div', class_=lambda c: c and 'dimmer' in c)
print(f"Found {len(dimmers)} dimmers:")
for d in dimmers:
    print("Dimmer class:", d.get('class'))
    print("Dimmer text:", d.get_text(strip=True)[:200])

modals = soup.find_all('div', class_=lambda c: c and ('modal' in c or 'dialog' in c or 'bottom-sheet' in c))
print(f"\nFound {len(modals)} modals:")
for m in modals:
    print("Modal class:", m.get('class'))
    print("Modal text:", m.get_text(strip=True)[:200])
