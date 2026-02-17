#!/usr/bin/env python3
"""
Complete Kenya Parliament MP Scraper
Two-step process:
1. Scrape listing pages (1-35) to get all MP profile URLs
2. Visit each profile page to get complete MP details
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin
from sqlalchemy.orm import Session

from app.models import MP, County



class CompleteMPScraper:
    """Complete MP scraper with pagination and detail page scraping"""
    
    def __init__(self, delay: float = 1.0):
        self.base_url = "https://www.parliament.go.ke"
        self.listing_url = f"{self.base_url}/the-national-assembly/mps"
        self.delay = delay  # Delay between requests (be respectful!)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def scrape_all_mps(self, max_pages: int = 35) -> List[Dict]:
        """Main method: scrape all MPs with complete details"""
        print("=" * 70)
        print("KENYA PARLIAMENT COMPLETE MP SCRAPER")
        print("=" * 70)
        print()
        
        # Step 1: Get all MP profile URLs from listing pages
        print("STEP 1: Collecting MP profile URLs from listing pages...")
        print("-" * 70)
        profile_urls = self.scrape_listing_pages(max_pages)
        
        print(f"\n✓ Found {len(profile_urls)} MP profiles")
        print()
        
        # Step 2: Visit each profile to get complete details
        print("STEP 2: Scraping detailed information from each MP page...")
        print("-" * 70)
        all_mps = self.scrape_mp_details(profile_urls)
        
        print(f"\n✓ Successfully scraped {len(all_mps)} complete MP profiles")
        return all_mps
    
    def scrape_listing_pages(self, max_pages: int = 35) -> List[str]:
        """Scrape all listing pages to collect MP profile URLs"""
        all_profile_urls = set()  # Use set to avoid duplicates
        
        for page_num in range(max_pages):
            # Drupal pagination: page=0 is page 2, page=1 is page 3, etc.
            if page_num == 0:
                url = self.listing_url
            else:
                url = f"{self.listing_url}?page={page_num - 1}"
            
            try:
                print(f"  Scraping page {page_num + 1}/{max_pages}: {url}")
                soup = self.fetch_page(url)
                
                # Find all MP profile links
                profile_links = self.extract_profile_links(soup)
                
                if not profile_links:
                    print(f"    ⚠ No profiles found on page {page_num + 1}, stopping...")
                    break
                
                print(f"    ✓ Found {len(profile_links)} profiles")
                all_profile_urls.update(profile_links)
                
                # Be respectful - delay between requests
                time.sleep(self.delay)
                
            except Exception as e:
                print(f"    ✗ Error on page {page_num + 1}: {e}")
                continue
        
        return list(all_profile_urls)
    
    def extract_profile_links(self, soup: BeautifulSoup) -> List[str]:
        """Extract MP profile links from a listing page"""
        profile_links = []
        
        # Method 1: Look for links with pattern /the-national-assembly/hon-
        links = soup.find_all('a', href=re.compile(r'/the-national-assembly/hon-'))
        for link in links:
            href = link.get('href', '')
            if href:
                full_url = urljoin(self.base_url, href)
                profile_links.append(full_url)
        
        # Method 2: Look for member profile links (alternative structure)
        if not profile_links:
            member_links = soup.find_all('a', class_=re.compile(r'member|mp-profile'))
            for link in member_links:
                href = link.get('href', '')
                if href and 'hon-' in href:
                    full_url = urljoin(self.base_url, href)
                    profile_links.append(full_url)
        
        # Remove duplicates
        return list(set(profile_links))
    
    def scrape_mp_details(self, profile_urls: List[str]) -> List[Dict]:
        """Scrape detailed information from each MP profile page"""
        all_mps = []
        total = len(profile_urls)
        
        for idx, url in enumerate(profile_urls, 1):
            try:
                print(f"  [{idx}/{total}] Scraping: {url}")
                
                soup = self.fetch_page(url)
                mp_data = self.parse_mp_profile(soup, url)
                
                if mp_data:
                    all_mps.append(mp_data)
                    print(f"    ✓ {mp_data['name']} - {mp_data['constituency']}, {mp_data['county']}")
                else:
                    print(f"    ✗ Could not parse profile")
                
                # Be respectful - delay between requests
                time.sleep(self.delay)
                
            except Exception as e:
                print(f"    ✗ Error: {e}")
                continue
        
        return all_mps
    
    def parse_mp_profile(self, soup: BeautifulSoup, url: str) -> Optional[Dict]:
        """Parse complete MP details from their profile page"""
        try:
            mp_data = {
                "profile_url": url,
                "name": "",
                "county": "",
                "constituency": "",
                "party": "",
                "email": "",
                "phone": "",
                "bio": "",
                "photo_url": "",
                "committees": [],
                "wiki_title": ""
            }
            
            # Extract name (usually in h1 or page title)
            name_elem = soup.find('h1', class_=re.compile(r'page-title|title'))
            if not name_elem:
                name_elem = soup.find('h1')
            if name_elem:
                mp_data['name'] = self.clean_text(name_elem.get_text())
            
            # Extract main content area
            content = soup.find('div', class_=re.compile(r'content|main|body'))
            if not content:
                content = soup
            
            # Extract county
            county_elem = content.find(text=re.compile(r'County', re.I))
            if county_elem:
                # Get the next element which usually contains the value
                parent = county_elem.find_parent()
                if parent:
                    county_value = parent.find_next_sibling()
                    if county_value:
                        mp_data['county'] = self.clean_text(county_value.get_text())
            
            # Try alternative: look for field-label
            if not mp_data['county']:
                county_field = content.find('div', class_='field-label', text=re.compile(r'County', re.I))
                if county_field:
                    county_value = county_field.find_next_sibling('div', class_='field-items')
                    if county_value:
                        mp_data['county'] = self.clean_text(county_value.get_text())
            
            # Extract constituency
            constituency_elem = content.find(text=re.compile(r'Constituency', re.I))
            if constituency_elem:
                parent = constituency_elem.find_parent()
                if parent:
                    constituency_value = parent.find_next_sibling()
                    if constituency_value:
                        mp_data['constituency'] = self.clean_text(constituency_value.get_text())
            
            # Alternative constituency
            if not mp_data['constituency']:
                const_field = content.find('div', class_='field-label', text=re.compile(r'Constituency', re.I))
                if const_field:
                    const_value = const_field.find_next_sibling('div', class_='field-items')
                    if const_value:
                        mp_data['constituency'] = self.clean_text(const_value.get_text())
            
            # Extract party
            party_elem = content.find(text=re.compile(r'Party', re.I))
            if party_elem:
                parent = party_elem.find_parent()
                if parent:
                    party_value = parent.find_next_sibling()
                    if party_value:
                        mp_data['party'] = self.clean_text(party_value.get_text())
            
            # Alternative party
            if not mp_data['party']:
                party_field = content.find('div', class_='field-label', text=re.compile(r'Party', re.I))
                if party_field:
                    party_value = party_field.find_next_sibling('div', class_='field-items')
                    if party_value:
                        mp_data['party'] = self.clean_text(party_value.get_text())
            
            # Extract email
            email_link = content.find('a', href=re.compile(r'mailto:'))
            if email_link:
                mp_data['email'] = email_link['href'].replace('mailto:', '').strip()
            
            # Extract phone
            phone_text = content.find(text=re.compile(r'\+254|0\d{9}'))
            if phone_text:
                phone_match = re.search(r'(\+254\d{9}|0\d{9})', phone_text)
                if phone_match:
                    mp_data['phone'] = phone_match.group(1)
            
            # Extract bio
            bio_elem = content.find('div', class_=re.compile(r'field-name-body|body|biography'))
            if bio_elem:
                mp_data['bio'] = self.clean_text(bio_elem.get_text())[:500]  # First 500 chars
            
            # Extract photo
            photo_elem = content.find('img', class_=re.compile(r'photo|image|portrait'))
            if not photo_elem:
                photo_elem = content.find('img')
            if photo_elem and photo_elem.get('src'):
                mp_data['photo_url'] = urljoin(self.base_url, photo_elem['src'])
            
            # Extract committees
            committees_section = content.find('div', class_=re.compile(r'committee'))
            if committees_section:
                committee_items = committees_section.find_all('li')
                mp_data['committees'] = [self.clean_text(c.get_text()) for c in committee_items]
            
            # Generate Wikipedia title
            if mp_data['name']:
                mp_data['wiki_title'] = self.generate_wiki_title(mp_data['name'])
            
            return mp_data
            
        except Exception as e:
            print(f"      Error parsing profile: {e}")
            return None
    
    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a page"""
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    
    def clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove HTML entities
        text = text.replace('&nbsp;', ' ')
        return text.strip()
    
    def generate_wiki_title(self, name: str) -> str:
        """Generate Wikipedia article title from MP name"""
        clean_name = re.sub(r'\(.*?\)', '', name)
        clean_name = re.sub(r'(Hon\.|Dr\.|Prof\.|Mr\.|Mrs\.|Ms\.|Amb\.)\s*', '', clean_name, flags=re.I)
        clean_name = clean_name.strip()
        wiki_title = clean_name.replace(' ', '_')
        
        if not wiki_title.endswith('_(Kenyan_politician)'):
            wiki_title += "_(Kenyan_politician)"
        
        return wiki_title



def group_by_county(mps: List[Dict]) -> Dict[str, List[Dict]]:
    """Group MPs by county"""
    counties = {}
    for mp in mps:
        county_name = mp.get('county', 'Unknown')
        if not county_name:
            county_name = "Unknown"
        
        if county_name not in counties:
            counties[county_name] = []
        
        # Create simplified version for county listing
        counties[county_name].append({
            "name": mp['name'],
            "constituency": mp['constituency'],
            "party": mp['party'],
            "email": mp.get('email', ''),
            "phone": mp.get('phone', ''),
            "wiki_title": mp['wiki_title'],
            "profile_url": mp['profile_url']
        })
    
    return counties


def save_to_json(mps: List[Dict], filename: str = "mps_complete.json"):
    """Save complete MP data to JSON file"""
    output = {
        "scraped_at": datetime.now().isoformat(),
        "total_mps": len(mps),
        "mps": mps,
        "by_county": group_by_county(mps)
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Saved {len(mps)} complete MP profiles to {filename}")
    print(f"✓ Found {len(output['by_county'])} counties")
    return output


class DatabaseSeeder:
    """Seeds the database with MP data"""
    
    def __init__(self, db_session: Optional[Session] = None):
        self.db = db_session
    
    def update_database(self, mps: List[Dict]):
        """Update database with complete MP data"""
        if not self.db:
            print("No database session provided. Skipping database update.")
            return
        
        try:
            # First, clear existing MPs (optional - comment out to update instead)
            # self.db.query(MP).delete()
            
            # Add or update each MP
            for mp_data in mps:
                existing_mp = self.db.query(MP).filter(
                    MP.profile_url == mp_data['profile_url']
                ).first()
                
                if existing_mp:
                    # Update existing MP
                    existing_mp.name = mp_data['name']
                    existing_mp.county = mp_data['county']
                    existing_mp.constituency = mp_data['constituency']
                    existing_mp.party = mp_data['party']
                    existing_mp.email = mp_data['email']
                    existing_mp.phone = mp_data['phone']
                    existing_mp.bio = mp_data['bio']
                    existing_mp.photo_url = mp_data['photo_url']
                    existing_mp.committees_json = mp_data['committees']
                    existing_mp.wiki_title = mp_data['wiki_title']
                    existing_mp.updated_at = datetime.now()
                else:
                    # Create new MP
                    new_mp = MP(
                        name=mp_data['name'],
                        county=mp_data['county'],
                        constituency=mp_data['constituency'],
                        party=mp_data['party'],
                        email=mp_data['email'],
                        phone=mp_data['phone'],
                        bio=mp_data['bio'],
                        photo_url=mp_data['photo_url'],
                        profile_url=mp_data['profile_url'],
                        committees_json=mp_data['committees'],
                        wiki_title=mp_data['wiki_title']
                    )
                    self.db.add(new_mp)
            
            self.db.commit()
            print(f"✓ Successfully updated/created {len(mps)} MPs in database")
            
            # Also update county MPs JSON for compatibility
            self.update_county_mps_json(mps)
            
        except Exception as e:
            print(f"✗ Error updating database: {e}")
            self.db.rollback()
            raise
    
    def update_county_mps_json(self, mps: List[Dict]):
        """Update the County.mps_json field with simplified MP data"""
        if not self.db:
            return
        
        try:
            counties_data = group_by_county(mps)
            
            for county_name, county_mps in counties_data.items():
                county = self.db.query(County).filter(County.name == county_name).first()
                
                if county:
                    county.mps_json = county_mps
                    county.updated_at = datetime.now()
                    print(f"  Updated {county_name} with {len(county_mps)} MPs")
            
            self.db.commit()
            print(f"✓ Updated MPs in {len(counties_data)} counties")
        except Exception as e:
            print(f"⚠ Warning updating county MPs: {e}")
            self.db.rollback()


def scrape_and_seed_mps(db: Optional[Session] = None) -> Dict:
    """
    Main function to scrape MPs and update database
    
    Args:
        db: SQLAlchemy database session (optional)
    
    Returns:
        Dictionary with scraped data and results
    """
    # Create scraper with 1-second delay between requests
    scraper = CompleteMPScraper(delay=1.0)
    
    try:
        # Scrape all MPs (35 pages max)
        all_mps = scraper.scrape_all_mps(max_pages=35)
        
        if not all_mps:
            print("\n✗ No MPs found!")
            return None
        
        # Save to JSON
        output = save_to_json(all_mps)
        
        # Update database if connection provided
        if db:
            seeder = DatabaseSeeder(db)
            seeder.update_database(all_mps)
        
        # Print summary
        print("\n" + "=" * 70)
        print("SCRAPING COMPLETE!")
        print("=" * 70)
        print(f"Total MPs: {len(all_mps)}")
        print(f"Counties: {len(output['by_county'])}")
        
        # Print statistics
        with_email = sum(1 for mp in all_mps if mp.get('email'))
        with_phone = sum(1 for mp in all_mps if mp.get('phone'))
        with_photo = sum(1 for mp in all_mps if mp.get('photo_url'))
        
        print(f"\nData completeness:")
        print(f"  MPs with email: {with_email}/{len(all_mps)} ({with_email/len(all_mps)*100:.1f}%)")
        print(f"  MPs with phone: {with_phone}/{len(all_mps)} ({with_phone/len(all_mps)*100:.1f}%)")
        print(f"  MPs with photo: {with_photo}/{len(all_mps)} ({with_photo/len(all_mps)*100:.1f}%)")
        
        # Print top 5 counties
        county_counts = [(name, len(mps)) for name, mps in output['by_county'].items()]
        county_counts.sort(key=lambda x: x[1], reverse=True)
        
        print("\nTop 5 counties by MP count:")
        for county, count in county_counts[:5]:
            print(f"  {county}: {count} MPs")
        
        # Print sample MP
        if all_mps:
            print("\nSample complete MP profile:")
            sample = all_mps[0]
            print(f"  Name: {sample['name']}")
            print(f"  Constituency: {sample['constituency']}")
            print(f"  County: {sample['county']}")
            print(f"  Party: {sample['party']}")
            print(f"  Email: {sample.get('email', 'N/A')}")
            print(f"  Phone: {sample.get('phone', 'N/A')}")
            print(f"  Committees: {len(sample.get('committees', []))}")
            print(f"  Profile URL: {sample['profile_url']}")
        
        print("\n" + "=" * 70)
        print("Next steps:")
        print("1. Review mps_complete.json")
        print("2. Database has been automatically seeded with MP data")
        print("=" * 70)
        
        return output
    
    except Exception as e:
        print(f"\n✗ Error during scraping: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # Run standalone
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        scrape_and_seed_mps(db)
    finally:
        db.close()
