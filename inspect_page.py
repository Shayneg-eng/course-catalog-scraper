import requests
from bs4 import BeautifulSoup

html = requests.get('https://elon.smartcatalogiq.com/en/2025-2026/academic-catalog/courses/ant-anthropology/400/ant-4986', timeout=30).text

# Save to file for inspection
with open('sample_page.html', 'w', encoding='utf-8') as f:
    f.write(html)

soup = BeautifulSoup(html, 'html.parser')

# Find all divs with specific classes or any structure
divs = soup.find_all('div', class_=True)
print(f"Found {len(divs)} divs with classes")
print("\nFirst 10 div classes:")
for i, div in enumerate(divs[:10]):
    print(f"{i}: {div.get('class')}")

print("\n\nAll text content:")
print(soup.get_text()[:3000])
