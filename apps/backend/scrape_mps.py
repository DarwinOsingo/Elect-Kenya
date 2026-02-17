#!/usr/bin/env python3
"""
MP Scraper runner script
Run from backend directory: python scrape_mps.py
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from app.database import SessionLocal, init_db
from app.utils.mp_scraper import scrape_and_seed_mps


def main():
    """Main execution"""
    print("Initializing database...")
    init_db()
    
    print("Starting MP scraper...")
    db = SessionLocal()
    try:
        result = scrape_and_seed_mps(db)
        if result:
            print("\n✓ MP scraping and seeding completed successfully!")
    finally:
        db.close()


if __name__ == "__main__":
    main()
