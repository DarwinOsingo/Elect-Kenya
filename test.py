import requests
from bs4 import BeautifulSoup

# 1. Check listing page
print("="*60)
print("LISTING PAGE STRUCTURE")
print("="*60)
listing_url = "https://www.parliament.go.ke/the-national-assembly/mps?page=1"
response = requests.get(listing_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all links to MP profiles
mp_links = soup.find_all('a', href=lambda x: x and '/the-national-assembly/hon-' in x)
print(f"Found {len(mp_links)} MP links")
print("\nFirst MP link example:")
if mp_links:
    print(mp_links[0].prettify())

# 2. Check detail page sections
print("\n" + "="*60)
print("DETAIL PAGE SECTIONS")
print("="*60)
detail_url = "https://www.parliament.go.ke/the-national-assembly/hon-amb-langat-benjamin-kipkirui"
response = requests.get(detail_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find expandable sections
sections = soup.find_all('div', class_='field')
print(f"Found {len(sections)} sections")
for section in sections[:5]:  # Show first 5
    print("\n---")
    print(section.prettify()[:500])