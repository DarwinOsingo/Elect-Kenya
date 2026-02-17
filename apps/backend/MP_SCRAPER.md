# MP Scraper Integration Guide

## Overview

The MP (Member of Parliament) scraper has been integrated into the Elect 2027 backend. It automatically scrapes current MPs from parliament.go.ke and updates the database with their information.

## Installation

The required dependencies have been added to:
- `requirements.txt`
- `Pipfile`

Make sure to install them:

```bash
# Using pip
pip install -r requirements.txt

# Or using pipenv
pipenv install
```

Key dependency added:
- `beautifulsoup4==4.12.2` - For HTML parsing

## Usage

### Option 1: Command Line Script

Run the scraper directly from the backend directory:

```bash
cd apps/backend
python scrape_mps.py
```

This will:
1. Initialize the database
2. Scrape MPs from parliament.go.ke
3. Parse the HTML using multiple fallback methods
4. Group MPs by county
5. Update the County records in the database
6. Save results to `mps_structured.json`

### Option 2: API Endpoint (Admin)

Use the POST endpoint at `/admin/scrape-mps` with your admin API key:

```bash
curl -X POST http://localhost:8000/admin/scrape-mps \
  -H "X-Api-Key: secret"
```

Response example:
```json
{
  "status": "success",
  "message": "MPs scraped and database updated",
  "total_mps": 416,
  "counties": 47,
  "scraped_at": "2024-02-08T10:30:45.123456"
}
```

### Option 3: Programmatic Usage in Python

```python
from app.database import SessionLocal
from app.utils.mp_scraper import scrape_and_seed_mps

db = SessionLocal()
try:
    result = scrape_and_seed_mps(db)
    print(f"Updated {len(result['by_county'])} counties")
finally:
    db.close()
```

## Scraper Architecture

### MPScraper Class

The main scraper that fetches and parses MP data from parliament.go.ke.

**Methods:**
- `fetch_page()` - Downloads the MPs page
- `extract_mp_data(soup)` - Extracts MP data using multiple parsing strategies
  - Method 1: Table-based parsing
  - Method 2: Article/div-based parsing  
  - Method 3: List item parsing
- `scrape()` - Main entry point

### DatabaseSeeder Class

Processes scraped data and updates the database.

**Methods:**
- `group_by_county(mps)` - Organizes MPs by county
- `save_to_json(mps, filename)` - Saves results to JSON file
- `update_database(mps)` - Updates County records in the database

## Data Structure

The scraper extracts the following fields for each MP:

```json
{
  "name": "Name of MP",
  "constituency": "Constituency Name",
  "county": "County Name",
  "party": "Political Party",
  "wiki_title": "Name_(Kenyan_politician)"
}
```

## Database Integration

The scraped MPs are stored in the `County` model's `mps_json` field:

```python
class County(Base):
    __tablename__ = "counties"
    # ... other fields ...
    mps_json = Column(JSON, default=list)  # Array of {name, constituency, party, wiki_title}
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
```

## Robustness

The scraper uses multiple parsing strategies to handle different HTML structures:
1. **Table parsing** - For traditional table layouts
2. **Article parsing** - For Drupal-style article nodes
3. **List parsing** - For list-based layouts

This makes it resilient to changes in the parliament.go.ke website structure.

## Outputs

### Console Output
```
Fetching MPs page...
Extracting MP data...
Found 416 MPs

Saved 416 MPs to mps_structured.json

=== SCRAPING SUMMARY ===
Total MPs: 416
Counties: 47

Sample MP:
{
  "name": "Hon. Abel Rotich",
  "county": "Bomet",
  "constituency": "Bomet Central",
  "party": "Kenya Kwanza",
  "wiki_title": "Abel_Rotich_(Kenyan_politician)"
}
```

### JSON Output (`mps_structured.json`)
```json
{
  "scraped_at": "2024-02-08T10:30:45.123456",
  "total_mps": 416,
  "mps": [...],
  "by_county": {
    "Bomet": [...],
    "Bungoma": [...],
    ...
  }
}
```

## Error Handling

The scraper includes comprehensive error handling:
- Network timeouts and failures are caught and reported
- HTML parsing errors are logged without stopping execution
- Database transaction errors are rolled back
- All exceptions include detailed stack traces for debugging

## Troubleshooting

### BeautifulSoup4 not found
```bash
pip install beautifulsoup4==4.12.2
```

### No MPs found
The parliament.go.ke website structure may have changed:
1. Check if the website is accessible
2. Review the HTML structure manually
3. Update the CSS selectors in `extract_mp_data()`

### Database errors
Ensure:
- Database connection is configured (DATABASE_URL env var)
- County records exist (MPs are matched to existing counties)
- Database session is properly initialized

## Future Enhancements

- Add caching to avoid repeated requests
- Implement differential updates (only update changed MPs)
- Add scheduling to run scraper on a schedule
- Include image URLs for MP photos
- Add validation and sanitization
- Integrate with Wikipedia API for additional data

---

**Files Modified/Created:**
- `app/utils/mp_scraper.py` - Main scraper module
- `scrape_mps.py` - CLI runner script
- `app/routes/admin.py` - Added `/admin/scrape-mps` endpoint
- `requirements.txt` - Added beautifulsoup4 dependency
- `Pipfile` - Added beautifulsoup4 dependency
