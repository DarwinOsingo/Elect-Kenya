#!/usr/bin/env python3
"""
Seed script to populate the database with initial data.
Run from the backend directory: python -m seeds.seed_data
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from app.database import SessionLocal, init_db
from app.models import Candidate, County, Issue, VoteBuyingFact


def seed_candidates(db):
    """Seed candidate data"""
    candidates = [
        {
            "slug": "william-ruto",
            "name": "William Kipchoge Ruto",
            "party": "Kenya Kwanza Alliance",
            "photo_url": "https://via.placeholder.com/300x400?text=William+Ruto",
            "bio_text": "William Ruto is the incumbent President of Kenya. Previously served as Deputy President and has held various ministerial positions.",
            "wiki_title": "William_Ruto",
            "county_affiliation": "Rift Valley",
            "good_json": [
                "Implemented digital government initiatives",
                "Focus on small business support",
                "Infrastructure projects in regions",
            ],
            "bad_json": [
                "ICC investigation for post-2007 election violence",
                "Allegations of corruption in public contracts",
                "Questions about land deals and acquisition of wealth",
            ],
            "crazy_json": [
                "Claims of promoting witchcraft (dismissed)",
            ],
            "policies_json": [
                {
                    "promise": "Affordable housing program",
                    "details": "Aim to construct 500,000 homes in first 5-year term",
                    "progress": "in_progress",
                    "sources": ["https://www.president.go.ke", "News reports 2023-2024"],
                },
                {
                    "promise": "Bottom-up economic model",
                    "details": "Support micro and small enterprises through credit facilities",
                    "progress": "in_progress",
                    "sources": ["Campaign manifesto 2022"],
                },
                {
                    "promise": "Reduce cost of living",
                    "details": "Tax relief, fuel price stabilization, food security",
                    "progress": "in_progress",
                    "sources": ["Official government statements"],
                },
            ],
        },
        {
            "slug": "fred-matiangi",
            "name": "Fred Koros Matiang'i",
            "party": "Azimio La Umoja",
            "photo_url": "https://via.placeholder.com/300x400?text=Fred+Matiangi",
            "bio_text": "Former Cabinet Secretary for Interior and Coordination. Served under two presidents and was known for security sector reforms.",
            "wiki_title": "Fred_Matiangi",
            "county_affiliation": "Western",
            "good_json": [
                "Reduced crime rates during tenure",
                "Civil service reforms",
                "Border security improvements",
            ],
            "bad_json": [
                "Allegations of political persecution during administration",
                "Questions about disputed security operations",
            ],
            "crazy_json": [],
            "policies_json": [
                {
                    "promise": "Security and governance reforms",
                    "details": "Professionalize security forces, combat corruption",
                    "progress": "not_started",
                    "sources": ["Campaign speeches 2024"],
                },
            ],
        },
        {
            "slug": "kalonzo-musyoka",
            "name": "Wycliffe Koskei Kalonzo Musyoka",
            "party": "Wiper Party",
            "photo_url": "https://via.placeholder.com/300x400?text=Kalonzo+Musyoka",
            "bio_text": "Long-time politician and Vice Presidential candidate in multiple elections. MP for Machakos and former mining minister.",
            "wiki_title": "Kalonzo_Musyoka",
            "county_affiliation": "Eastern",
            "good_json": [
                "Long parliamentary experience",
                "Drought relief initiatives",
                "Regional leadership",
            ],
            "bad_json": [
                "Allegations of election disputes",
                "Questions about personal wealth accumulation",
            ],
            "crazy_json": [],
            "policies_json": [
                {
                    "promise": "Address drought and pastoralism",
                    "details": "Support for pastoral communities, water projects",
                    "progress": "not_started",
                    "sources": ["Party manifesto"],
                },
            ],
        },
        {
            "slug": "rigathi-gachagua",
            "name": "Rigathi Gachagua",
            "party": "Kenya Kwanza Alliance",
            "photo_url": "https://via.placeholder.com/300x400?text=Rigathi+Gachagua",
            "bio_text": "Former Deputy President. Businessman and politician from Central Kenya. Known for his mobilization efforts.",
            "wiki_title": "Rigathi_Gachagua",
            "county_affiliation": "Central",
            "good_json": [
                "Business background in logistics",
                "Regional economic initiatives",
            ],
            "bad_json": [
                "Corruption allegations during tenure",
                "Impeachment from Deputy President position",
            ],
            "crazy_json": [],
            "policies_json": [
                {
                    "promise": "Regional economic development",
                    "details": "Support for traders and SMEs in Central region",
                    "progress": "not_started",
                    "sources": ["Political statements"],
                },
            ],
        },
        {
            "slug": "eliud-owalo",
            "name": "Eliud Owalo",
            "party": "Orange Democratic Movement (ODM)",
            "photo_url": "https://via.placeholder.com/300x400?text=Eliud+Owalo",
            "bio_text": "Cabinet Secretary for Interior. Career in business and government. Represents Kisumu County interests.",
            "wiki_title": "Eliud_Owalo",
            "county_affiliation": "Western",
            "good_json": [
                "Business development background",
                "Community mobilization",
            ],
            "bad_json": [
                "Limited national track record in elected positions",
            ],
            "crazy_json": [],
            "policies_json": [
                {
                    "promise": "Youth employment programs",
                    "details": "Job creation through digital economy",
                    "progress": "not_started",
                    "sources": ["Campaign materials"],
                },
            ],
        },
        {
            "slug": "martha-karua",
            "name": "Martha Wangari Karua",
            "party": "Azimio La Umoja",
            "photo_url": "https://via.placeholder.com/300x400?text=Martha+Karua",
            "bio_text": "Prominent women's rights advocate and former attorney. Long parliamentary career. 2022 running mate candidate.",
            "wiki_title": "Martha_Karua",
            "county_affiliation": "Central",
            "good_json": [
                "Strong human rights advocacy",
                "Anti-corruption stance",
                "Women and youth focus",
            ],
            "bad_json": [
                "Limited executive governance experience",
            ],
            "crazy_json": [],
            "policies_json": [
                {
                    "promise": "Gender equality and women empowerment",
                    "details": "Equal representation, economic participation",
                    "progress": "not_started",
                    "sources": ["Advocacy work, campaign"],
                },
            ],
        },
    ]

    for candidate_data in candidates:
        # Check if candidate already exists
        existing = db.query(Candidate).filter(Candidate.slug == candidate_data["slug"]).first()
        if not existing:
            candidate = Candidate(**candidate_data)
            db.add(candidate)
            print(f"✓ Added candidate: {candidate_data['name']}")
        else:
            print(f"⊘ Candidate already exists: {candidate_data['name']}")

    db.commit()


def seed_counties(db):
    """Seed county data"""
    counties = [
        {
            "name": "Nakuru",
            "governor_name": "Susan Kipchoge Kihika",
            "governor_party": "Kenya Kwanza Alliance",
            "governor_wiki_title": "Susan_Kihika",
            "senators_json": [
                {"name": "Tabitha Karanja Mutinda", "party": "Kenya Kwanza", "wiki_title": "Tabitha_Karanja"},
                {"name": "Ledama Ole Kina", "party": "ODM", "wiki_title": "Ledama_Ole_Kina"},
                {"name": "Irungu Kang'ata", "party": "UDA", "wiki_title": "Irungu_Kangata"},
            ],
            "mps_json": [
                {
                    "name": "Kimani Ngunjiri",
                    "constituency": "Bahati",
                    "party": "UDA",
                    "wiki_title": "Kimani_Ngunjiri",
                },
                {"name": "David Kiplagat", "constituency": "Kuresoi North", "party": "UDA", "wiki_title": "David_Kiplagat"},
                {"name": "Beatrice Kones", "constituency": "Nakuru Town West", "party": "UDA", "wiki_title": "Beatrice_Kones"},
                {
                    "name": "Samuel Arama",
                    "constituency": "Naivasha",
                    "party": "UDA",
                    "wiki_title": "Samuel_Arama",
                },
                {"name": "Alex Kipkosgei", "constituency": "Rongai", "party": "UDA", "wiki_title": "Alex_Kipkosgei"},
                {
                    "name": "David Mwangi",
                    "constituency": "Njoro",
                    "party": "UDA",
                    "wiki_title": "David_Mwangi",
                },
                {"name": "Benjamin Kemboi", "constituency": "Kuresoi South", "party": "KANU", "wiki_title": "Benjamin_Kemboi"},
                {
                    "name": "Charles Kamau",
                    "constituency": "Nakuru East",
                    "party": "UDA",
                    "wiki_title": "Charles_Kamau",
                },
            ],
            "past_election_results_json": [
                {
                    "year": 2022,
                    "type": "gubernatorial",
                    "winner": "Susan Kihika",
                    "votes": 548900,
                    "source": "IEBC",
                },
                {
                    "year": 2017,
                    "type": "gubernatorial",
                    "winner": "Lee Kinyanjui",
                    "votes": 438232,
                    "source": "IEBC",
                },
            ],
            "voted_bills_json": [
                {
                    "bill_title": "Finance Bill 2024",
                    "bill_id": "HB1/2024",
                    "vote": "Yes",
                    "date": "2024-06-25",
                    "source_url": "https://www.parliament.go.ke",
                },
                {
                    "bill_title": "Education Amendment Bill 2023",
                    "bill_id": "HB45/2023",
                    "vote": "Yes",
                    "date": "2023-11-10",
                    "source_url": "https://www.parliament.go.ke",
                },
            ],
        },
        {
            "name": "Kisumu",
            "governor_name": "Anyang Nyong'o",
            "governor_party": "ODM",
            "governor_wiki_title": "Anyang_Nyongo",
            "senators_json": [
                {"name": "Tom Ojienda", "party": "ODM", "wiki_title": "Tom_Ojienda"},
                {"name": "Osotsi Godfrey", "party": "Ford-K", "wiki_title": "Godfrey_Osotsi"},
            ],
            "mps_json": [
                {"name": "John Mbadi", "constituency": "Suba South", "party": "ODM", "wiki_title": "John_Mbadi"},
                {"name": "Jared Okelo", "constituency": "Nyatike", "party": "ODM", "wiki_title": "Jared_Okelo"},
                {"name": "Willybright Oyugi", "constituency": "Kisumu City", "party": "ODM", "wiki_title": "Willybright_Oyugi"},
                {
                    "name": "Rashid Kassim",
                    "constituency": "Seme",
                    "party": "Independent",
                    "wiki_title": "Rashid_Kassim",
                },
                {"name": "Elisha Ochieng", "constituency": "Nyando", "party": "ODM", "wiki_title": "Elisha_Ochieng"},
            ],
            "past_election_results_json": [
                {
                    "year": 2022,
                    "type": "gubernatorial",
                    "winner": "Anyang Nyong'o",
                    "votes": 619023,
                    "source": "IEBC",
                },
            ],
            "voted_bills_json": [],
        },
    ]

    for county_data in counties:
        # Check if county already exists
        existing = db.query(County).filter(County.name == county_data["name"]).first()
        if not existing:
            county = County(**county_data)
            db.add(county)
            print(f"✓ Added county: {county_data['name']}")
        else:
            print(f"⊘ County already exists: {county_data['name']}")

    db.commit()


def seed_issues(db):
    """Seed issue data"""
    issues = [
        {
            "title": "Economy & Poverty Reduction",
            "good_points_json": [
                "Focus on job creation in tech and agriculture",
                "Support for small and medium enterprises (SMEs)",
                "Infrastructure investment to spur growth",
                "Fair taxation that doesn't burden the poor",
            ],
            "bad_points_json": [
                "High cost of living remains unaddressed",
                "Corruption diverts resources meant for development",
                "Unemployment among youth remains high",
                "Rural areas lag in economic opportunities",
            ],
            "sources_json": [
                "World Bank Kenya Economic Report 2023",
                "Kenya National Bureau of Statistics",
                "IMF Article IV Consultation 2024",
            ],
        },
        {
            "title": "Healthcare & Education",
            "good_points_json": [
                "Free primary and secondary education expansion",
                "Universal health coverage initiatives",
                "Teacher and healthcare worker training",
                "Mobile health clinics for rural access",
            ],
            "bad_points_json": [
                "Teacher strikes over pay delays",
                "Healthcare worker shortage in rural areas",
                "Disparities between urban and rural education quality",
                "High dropout rates despite free education",
            ],
            "sources_json": [
                "Ministry of Education Strategic Plan",
                "Ministry of Health Annual Report 2023",
                "UN Education Index Report",
            ],
        },
        {
            "title": "Corruption & Governance",
            "good_points_json": [
                "Anti-corruption commission active investigations",
                "Improved financial transparency reporting",
                "Civil service reforms reducing ghost workers",
                "Whistleblower protection mechanisms",
            ],
            "bad_points_json": [
                "High-level corruption cases lack swift prosecution",
                "Estimated KSh 5T lost to corruption over 10 years",
                "Weak enforcement of asset recovery",
                "Political interference in justice systems",
            ],
            "sources_json": [
                "EACC Annual Report 2023",
                "Transparency International Kenya Index",
                "World Bank Corruption Perception Index",
            ],
        },
        {
            "title": "Infrastructure & Tourism",
            "good_points_json": [
                "Standard Gauge Railway improving connectivity",
                "Highway expansion and rehabilitation",
                "Port of Mombasa modernization",
                "Tourism revenue supporting employment",
            ],
            "bad_points_json": [
                "High project costs with limited accountability",
                "Delayed completion and budget overruns",
                "Environmental degradation from mega-projects",
                "Unequal infrastructure development by region",
            ],
            "sources_json": [
                "Ministry of Transport Reports 2023",
                "Kenya Vision 2030 Progress Report",
            ],
        },
    ]

    for issue_data in issues:
        # Check if issue already exists
        existing = db.query(Issue).filter(Issue.title == issue_data["title"]).first()
        if not existing:
            issue = Issue(**issue_data)
            db.add(issue)
            print(f"✓ Added issue: {issue_data['title']}")
        else:
            print(f"⊘ Issue already exists: {issue_data['title']}")

    db.commit()


def seed_vote_buying(db):
    """Seed vote-buying facts"""
    facts = [
        {
            "section_title": "How Vote-Buying Works",
            "content_text": """Vote-buying typically operates through a chain:

1. Politicians or candidates identify supporters they need to win
2. Agents distribute cash, vouchers, or goods (KSh 50–1,000 per person)
3. Voters are promised payments in exchange for:
   - Voting for a specific candidate
   - Attending rallies
   - Influencing family members

Common tactics:
• Direct cash handouts at rallies
• Promises paid after elections (rarely honored)
• Free transportation to campaign events
• Meals and entertainment
• Cell phone airtime or data bundles
• Soap, sugar, or other goods

The money often comes from:
• Unexplained sources (unclear business dealings)
• Public funds (government resources)
• Foreign donations (sometimes illegal)
• Business donors expecting favors
""",
            "sources_json": [
                "EACC Election Integrity Reports 2017–2023",
                "Transparency International Kenya studies",
                "International IDEA Campaign Finance Documentation",
            ],
        },
        {
            "section_title": "The Real Cost of Vote-Buying",
            "content_text": """A voter accepting KSh 500 in bribes participates in a system that costs the nation billions:

IMMEDIATE IMPACT:
• Public coffers are depleted for voter inducements
• Honest candidates are disadvantaged
• Elections become contests of who can distribute the most cash

LONG-TERM IMPACT (10-year cycle):
• Corruption becomes normalized in politics
• Winners feel emboldened to recoup losses through theft
• Services suffer: roads unbuilt, clinics unfunded, schools unpaid
• Investment and foreign confidence decline
• Youth emigrate seeking better opportunities

FINANCIAL IMPACT:
• Estimated KSh 5 trillion lost over 10 years through corruption-related activities
• This could have built: 1,400 hospitals, 50 million schoolrooms, 8 million km of roads
• Or reduced national debt interest costs significantly

THE CALCULATION:
• Your KSh 500 bribe
• × 20 million voters
• × Multiple elections
• = KSh 10+ billion diverted from schools, hospitals, and roads

Each bribe you take makes corruption easier and the country poorer.
""",
            "sources_json": [
                "Transparency International Kenya Corruption Index",
                "EACC Public Reports",
                "World Bank Kenya Country Report",
                "KNBS Economic Survey 2024",
            ],
        },
        {
            "section_title": "Legal Consequences",
            "content_text": """Vote-buying is ILLEGAL under Kenya's election laws:

For Voters:
• Fine: Up to KSh 10,000
• Imprisonment: Up to 5 years
• Loss of voting rights for a period

For Candidates/Agents:
• Fine: KSh 100,000–1,000,000
• Imprisonment: Up to 10 years
• Disqualification from contesting elections
• Asset forfeiture

ENFORCEMENT:
• IEBC monitors for vote-buying
• EACC investigates financing violations
• Independent observers report suspicious activities
• Citizens can report violations to hotlines

RECENT CASES:
• Multiple cases filed during 2022 elections
• Investigations ongoing for campaign finance violations
• Asset recovery proceedings for some officials
""",
            "sources_json": [
                "Elections Act 2011, Kenya",
                "IEBC Code of Conduct for Candidates",
                "Public Prosecution Office Decisions",
            ],
        },
        {
            "section_title": "How to Report Vote-Buying",
            "content_text": """If you witness vote-buying or electoral malpractice:

IMMEDIATE ACTIONS:
1. Note the details: Date, time, location, who is involved, amount offered
2. Take photos/video if safe (do not confront perpetrators)
3. Report to election observers present at the location

FORMAL REPORTING CHANNELS:
1. IEBC Voter Hotline: Call/SMS your local IEBC office
2. EACC: Visit eacc.go.ke or call 0800 722 722
3. Election Observation Centers in your county
4. National Police Service (if violence is involved)

ONLINE REPORTING:
• IEBC portal for electoral violations
• EACC whistleblower online form
• Kenya Human Rights Commission hotline

PROTECTION:
• Whistleblower protection laws apply
• Confidentiality is maintained
• No retaliation is permitted by law

Your report could:
• Prevent a violation
• Lead to prosecution
• Protect electoral integrity
• Strengthen democracy
""",
            "sources_json": [
                "IEBC Official Contact Information",
                "EACC Whistleblower Policy",
                "Whistleblower Protection Act 2011",
            ],
        },
    ]

    for fact_data in facts:
        # Check if fact already exists
        existing = db.query(VoteBuyingFact).filter(VoteBuyingFact.section_title == fact_data["section_title"]).first()
        if not existing:
            fact = VoteBuyingFact(**fact_data)
            db.add(fact)
            print(f"✓ Added vote-buying fact: {fact_data['section_title']}")
        else:
            print(f"⊘ Vote-buying fact already exists: {fact_data['section_title']}")

    db.commit()


def main():
    """Main seed function"""
    print("🌱 Starting database seeding...")

    # Initialize database
    init_db()
    print("✓ Database initialized")

    # Create session
    db = SessionLocal()

    try:
        print("\nSeeding candidates...")
        seed_candidates(db)

        print("\nSeeding counties...")
        seed_counties(db)

        print("\nSeeding issues...")
        seed_issues(db)

        print("\nSeeding vote-buying facts...")
        seed_vote_buying(db)

        print("\n✅ Database seeding completed successfully!")

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
