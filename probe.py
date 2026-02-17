"""
probe.py — Stage 0: Site investigation script.

Run this ONCE before building any stage of the pipeline.
Answers 5 critical unknowns about parliament.go.ke structure:

  1. Exact total MP count and pagination depth
  2. Which Drupal field classes exist on profile pages (and coverage %)
  3. Whether voting records exist per-MP or only in bulk
  4. Whether tables use <table>, <p>, <ul> or mixed formats
  5. Where the real MP photo lives (listing thumbnail vs profile page)

Output: probe_report.json  ← read this before writing any extractor

Usage:
    python probe.py

Requirements:
    pip install playwright beautifulsoup4 lxml
    playwright install chromium
"""

import json
import random
import re
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ─── Inline constants (probe is self-contained, no config import needed) ──────

BASE_URL       = "https://www.parliament.go.ke"
LISTING_URL    = f"{BASE_URL}/the-national-assembly/mps"
PROBE_SAMPLES  = 10     # number of MP profile pages to inspect
DELAY_BETWEEN  = 2.0    # seconds between requests
OUTPUT_FILE    = Path(__file__).parent / "probe_report.json"

VOTING_PROBE_PATHS = [
    "/the-national-assembly/votes-and-proceedings",
    "/the-national-assembly/hansard",
    "/the-national-assembly/bills",
    "/the-national-assembly/committee-business",
]

# ─── Helpers ──────────────────────────────────────────────────────────────────

def log(msg: str) -> None:
    """Simple timestamped print."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def get_page_html(page, url: str, retries: int = 3) -> str | None:
    """
    Navigate to URL with Playwright and return full page HTML.
    Returns None if all retries fail.
    """
    for attempt in range(1, retries + 1):
        try:
            page.goto(url, timeout=30_000, wait_until="domcontentloaded")
            time.sleep(0.5)  # let any late JS settle
            return page.content()
        except PlaywrightTimeout:
            log(f"  Timeout on {url} (attempt {attempt}/{retries})")
            time.sleep(2)
        except Exception as exc:
            log(f"  Error on {url}: {exc} (attempt {attempt}/{retries})")
            time.sleep(2)
    return None


def extract_mp_links_from_html(html: str) -> list[dict]:
    """
    Parse listing page HTML and extract all MP links + thumbnail photo URLs.
    Returns list of {name, url, photo_url} dicts.
    """
    soup = BeautifulSoup(html, "lxml")
    results = []

    # MP links follow the pattern /the-national-assembly/hon-*
    for a_tag in soup.find_all("a", href=re.compile(r"/the-national-assembly/hon-")):
        href = a_tag.get("href", "")
        url  = BASE_URL + href if href.startswith("/") else href

        # Extract name — either from img alt or link text
        img = a_tag.find("img")
        if img:
            name      = img.get("alt", "").strip()
            photo_url = img.get("src", "")
            if photo_url.startswith("/"):
                photo_url = BASE_URL + photo_url
        else:
            name      = a_tag.get_text(strip=True)
            photo_url = None

        # Derive slug from URL path
        slug = href.rstrip("/").split("/")[-1]

        if slug and slug not in [r["slug"] for r in results]:
            results.append({
                "slug":      slug,
                "name":      name,
                "url":       url,
                "photo_url": photo_url,
            })

    return results


def find_last_page(page) -> int:
    """
    Navigate listing pages until no new MPs appear.
    Returns the last valid page number (0-indexed).
    """
    log("Probing pagination depth...")
    last_valid = 0

    for page_num in range(0, 30):  # safety cap at 30 pages
        url  = f"{LISTING_URL}?page={page_num}"
        html = get_page_html(page, url)

        if not html:
            log(f"  Page {page_num}: failed to load — stopping")
            break

        links = extract_mp_links_from_html(html)
        log(f"  Page {page_num}: found {len(links)} MP links")

        if len(links) == 0:
            log(f"  Page {page_num}: empty — last valid page was {last_valid}")
            break

        last_valid = page_num
        time.sleep(DELAY_BETWEEN)

    return last_valid


def inventory_profile_fields(html: str, slug: str) -> dict:
    """
    For one MP profile page, record every Drupal field class present.
    Returns dict: {field_class: {present: bool, html_preview: str, structure_type: str}}
    """
    soup   = BeautifulSoup(html, "lxml")
    fields = {}

    # Find all elements whose class contains "field--name-"
    for el in soup.find_all(class_=re.compile(r"field--name-")):
        classes = el.get("class", [])
        # Extract the field--name-* class specifically
        field_class = next(
            (c for c in classes if c.startswith("field--name-")), None
        )
        if not field_class or field_class in fields:
            continue

        # Get a short preview of inner HTML (first 300 chars, stripped)
        inner   = str(el)[:500].replace("\n", " ").strip()
        content = el.get_text(separator=" ", strip=True)[:200]

        # Detect structure type inside this field
        has_table = bool(el.find("table"))
        has_ul    = bool(el.find("ul"))
        has_ol    = bool(el.find("ol"))
        has_p     = bool(el.find("p"))
        has_base64 = "data:image" in str(el)

        if has_table:
            structure = "table"
        elif has_ul:
            structure = "unordered_list"
        elif has_ol:
            structure = "ordered_list"
        elif has_p:
            structure = "paragraphs"
        else:
            structure = "text_only"

        # Detect Word-generated HTML patterns
        is_word_html = bool(
            re.search(r'font-family.*Times|margin-left:\d+\.\d+pt|0in \d', str(el))
        )

        fields[field_class] = {
            "present":        True,
            "structure_type": structure,
            "is_word_html":   is_word_html,
            "has_base64":     has_base64,
            "content_chars":  len(content),
            "html_preview":   inner[:300],
            "text_preview":   content[:200],
        }

    # Also capture page title / h1 (where name lives)
    h1 = soup.find("h1")
    fields["_page_title"] = {
        "present":  bool(h1),
        "text":     h1.get_text(strip=True) if h1 else None,
    }

    # Check for any photo in the profile (not just field--name-field-image)
    profile_photos = []
    for img in soup.find_all("img"):
        src = img.get("src", "")
        alt = img.get("alt", "")
        # Skip base64, banners, logos
        if "base64" in src or "logo" in src.lower() or "banner" in src.lower():
            continue
        if "mp_photo" in src or "styles/medium" in src or "styles/large" in src:
            profile_photos.append({"src": src, "alt": alt,
                                    "width":  img.get("width"),
                                    "height": img.get("height")})

    fields["_profile_photos"] = profile_photos

    return fields


def analyse_table_structure(html: str) -> dict:
    """
    Deep-dive into education/employment tables for one MP.
    Returns info about column count, header detection, Word markup severity.
    """
    soup    = BeautifulSoup(html, "lxml")
    results = {}

    for field_name in ["field--name-field-education-background",
                       "field--name-field-employment-history"]:
        field_el = soup.find(class_=re.compile(field_name))
        if not field_el:
            results[field_name] = {"present": False}
            continue

        table = field_el.find("table")
        if not table:
            # Not a table — what is it?
            text = field_el.get_text(separator="\n", strip=True)
            results[field_name] = {
                "present":        True,
                "is_table":       False,
                "structure":      "non_table",
                "raw_text_lines": text.split("\n")[:10],
            }
            continue

        # Analyse table structure
        rows       = table.find_all("tr")
        all_cells  = [td.get_text(strip=True) for td in table.find_all(["td", "th"])]
        header_row = rows[0] if rows else None
        header_cells = []
        if header_row:
            header_cells = [
                cell.get_text(strip=True)
                for cell in header_row.find_all(["th", "td"])
            ]

        # Detect Word HTML severity
        word_patterns = re.findall(
            r'margin-left|font-family.*Times|0in \d|border:solid', str(table)
        )

        results[field_name] = {
            "present":          True,
            "is_table":         True,
            "row_count":        len(rows),
            "col_count":        len(rows[0].find_all(["td", "th"])) if rows else 0,
            "header_cells":     header_cells,
            "sample_cells":     all_cells[:15],
            "word_html_hits":   len(word_patterns),
            "word_patterns":    word_patterns[:5],
            "has_nested_spans": bool(table.find("span", style=True)),
        }

    return results


def probe_voting_records(page) -> dict:
    """
    Check several URLs that might contain voting record data.
    Returns findings per URL.
    """
    log("Probing voting record locations...")
    findings = {}

    for path in VOTING_PROBE_PATHS:
        url  = BASE_URL + path
        html = get_page_html(page, url)
        log(f"  Checking {url}")

        if not html:
            findings[path] = {"accessible": False, "reason": "failed_to_load"}
            time.sleep(DELAY_BETWEEN)
            continue

        soup  = BeautifulSoup(html, "lxml")
        text  = soup.get_text(separator=" ", strip=True)

        # Look for signals of voting data
        has_bill_numbers   = bool(re.search(r'Bill No\.|No\. \d{1,3} of 20\d{2}', text))
        has_vote_counts    = bool(re.search(r'\bAyes?\b|\bNoes?\b|\babstain', text, re.I))
        has_mp_names       = bool(re.search(r'Hon\.|Member for', text))
        has_pdf_links      = bool(soup.find("a", href=re.compile(r'\.pdf', re.I)))
        has_download_links = bool(soup.find("a", href=re.compile(r'download|votes', re.I)))

        # Count links that might be individual vote records
        vote_links = soup.find_all("a", href=re.compile(r'vote|bill|hansard', re.I))

        findings[path] = {
            "accessible":       True,
            "has_bill_numbers": has_bill_numbers,
            "has_vote_counts":  has_vote_counts,
            "has_mp_names":     has_mp_names,
            "has_pdf_links":    has_pdf_links,
            "has_download_links": has_download_links,
            "vote_link_count":  len(vote_links),
            "page_title":       (soup.find("h1") or soup.find("title") or "").get_text(strip=True)
                                if not isinstance((soup.find("h1") or soup.find("title") or ""), str)
                                else "",
            "recommendation":   "check_manually" if (has_bill_numbers or has_vote_counts)
                                else "probably_not_per_mp_data",
        }
        time.sleep(DELAY_BETWEEN)

    return findings


# ─── Main Probe Logic ─────────────────────────────────────────────────────────

def run_probe() -> dict:
    """
    Run all 5 probe tasks and return a comprehensive report dict.
    """
    report = {
        "probe_timestamp":   datetime.now().isoformat(),
        "probe_version":     "1.0",
        "base_url":          BASE_URL,
        "unknowns_resolved": {},
        "pagination":        {},
        "field_coverage":    {},
        "table_analysis":    {},
        "voting_records":    {},
        "photo_source":      {},
        "raw_mp_sample":     [],
        "recommendations":   [],
    }

    all_mp_links = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )
        page = context.new_page()

        # ── Task 1: Pagination Audit ──────────────────────────────────────────
        log("=" * 60)
        log("TASK 1: Pagination Audit")
        log("=" * 60)

        # Collect links from first page first
        html_page0 = get_page_html(page, LISTING_URL)
        if not html_page0:
            log("ERROR: Cannot load listing page — is the site accessible?")
            browser.close()
            return report

        page0_links = extract_mp_links_from_html(html_page0)
        log(f"Page 0: {len(page0_links)} MPs found")
        log(f"First MP: {page0_links[0] if page0_links else 'none'}")

        # Find last page
        last_page   = find_last_page(page)
        per_page    = len(page0_links)

        # Estimate total (collect all links from all pages)
        log(f"Collecting all MP links across {last_page + 1} pages...")
        all_mp_links = list(page0_links)  # already have page 0

        for p_num in range(1, last_page + 1):
            url  = f"{LISTING_URL}?page={p_num}"
            html = get_page_html(page, url)
            if html:
                links = extract_mp_links_from_html(html)
                all_mp_links.extend(links)
                log(f"  Page {p_num}: +{len(links)} MPs (running total: {len(all_mp_links)})")
            time.sleep(DELAY_BETWEEN)

        # Deduplicate by slug
        seen_slugs  = set()
        unique_links = []
        for link in all_mp_links:
            if link["slug"] not in seen_slugs:
                seen_slugs.add(link["slug"])
                unique_links.append(link)
        all_mp_links = unique_links

        report["pagination"] = {
            "last_page_index": last_page,
            "total_pages":     last_page + 1,
            "per_page":        per_page,
            "total_mp_links":  len(all_mp_links),
            "first_mp":        all_mp_links[0] if all_mp_links else None,
            "last_mp":         all_mp_links[-1] if all_mp_links else None,
        }
        report["unknowns_resolved"]["total_mps"] = len(all_mp_links)

        log(f"✓ Total unique MPs found: {len(all_mp_links)}")

        # ── Task 2 & 4 & 5: Profile Field Inventory + Table Analysis + Photos ─
        log("")
        log("=" * 60)
        log("TASKS 2, 4, 5: Field Inventory + Table Analysis + Photo Source")
        log("=" * 60)

        # Sample PROBE_SAMPLES random MPs
        sample_links = random.sample(all_mp_links, min(PROBE_SAMPLES, len(all_mp_links)))
        log(f"Sampling {len(sample_links)} random MP profiles...")

        field_presence = defaultdict(lambda: {"present": 0, "absent": 0, "structures": []})
        table_samples  = []
        photo_findings = []

        for i, mp in enumerate(sample_links):
            log(f"  [{i+1}/{len(sample_links)}] {mp['name']} — {mp['url']}")
            html = get_page_html(page, mp["url"])

            if not html:
                log(f"    SKIP: failed to load")
                time.sleep(DELAY_BETWEEN)
                continue

            # Field inventory
            fields = inventory_profile_fields(html, mp["slug"])

            for field_class, info in fields.items():
                if field_class.startswith("_"):
                    continue  # skip metadata keys
                if info.get("present"):
                    field_presence[field_class]["present"] += 1
                    field_presence[field_class]["structures"].append(
                        info.get("structure_type", "unknown")
                    )
                else:
                    field_presence[field_class]["absent"] += 1

            # Profile photo findings
            profile_photos = fields.get("_profile_photos", [])
            listing_photo  = mp.get("photo_url")
            photo_findings.append({
                "slug":            mp["slug"],
                "listing_photo":   listing_photo,
                "profile_photos":  profile_photos,
                "has_listing_photo": bool(listing_photo),
                "has_profile_photo": len(profile_photos) > 0,
            })

            # Table structure analysis (save for first PROBE_TABLE_SAMPLES MPs)
            if len(table_samples) < 5:
                table_info = analyse_table_structure(html)
                any_table  = any(v.get("is_table") for v in table_info.values()
                                 if isinstance(v, dict))
                table_samples.append({
                    "slug":       mp["slug"],
                    "name":       mp["name"],
                    "has_tables": any_table,
                    "fields":     table_info,
                })

            report["raw_mp_sample"].append({
                "slug":           mp["slug"],
                "name":           mp["name"],
                "h1_text":        fields.get("_page_title", {}).get("text"),
                "fields_present": [
                    k for k, v in fields.items()
                    if not k.startswith("_") and v.get("present")
                ],
            })

            time.sleep(DELAY_BETWEEN + random.uniform(0, 0.5))

        # Summarise field coverage
        total_sampled = len(sample_links)
        coverage = {}
        for field_class, counts in field_presence.items():
            present    = counts["present"]
            structures = counts["structures"]
            structure_counts = defaultdict(int)
            for s in structures:
                structure_counts[s] += 1

            coverage[field_class] = {
                "present_count":   present,
                "absent_count":    total_sampled - present,
                "coverage_pct":    round(present / total_sampled * 100, 1),
                "structure_types": dict(structure_counts),
                "most_common_structure": (
                    max(structure_counts, key=structure_counts.get)
                    if structure_counts else "unknown"
                ),
            }

        report["field_coverage"]  = dict(sorted(
            coverage.items(), key=lambda x: x[1]["coverage_pct"], reverse=True
        ))
        report["table_analysis"]  = table_samples

        # Photo source conclusion
        has_listing = sum(1 for f in photo_findings if f["has_listing_photo"])
        has_profile = sum(1 for f in photo_findings if f["has_profile_photo"])
        report["photo_source"] = {
            "findings":          photo_findings,
            "listing_photo_count": has_listing,
            "profile_photo_count": has_profile,
            "recommendation":    (
                "listing_thumbnail" if has_listing > has_profile
                else "profile_page" if has_profile > has_listing
                else "both_available"
            ),
        }
        report["unknowns_resolved"]["photo_source"] = report["photo_source"]["recommendation"]

        log(f"✓ Field coverage analysed across {total_sampled} profiles")

        # ── Task 3: Voting Record Hunt ────────────────────────────────────────
        log("")
        log("=" * 60)
        log("TASK 3: Voting Record Investigation")
        log("=" * 60)

        # Also check a sample MP profile for voting fields
        if all_mp_links:
            sample_mp_url  = all_mp_links[0]["url"]
            sample_html    = get_page_html(page, sample_mp_url)
            if sample_html:
                soup           = BeautifulSoup(sample_html, "lxml")
                full_text      = soup.get_text(separator=" ", strip=True)
                vote_in_profile = {
                    "url":            sample_mp_url,
                    "has_vote_field": bool(re.search(
                        r'vote|bill.*read|division|ayes|noes', full_text, re.I
                    )),
                    "vote_related_text_snippet": re.findall(
                        r'.{40}(?:vote|bill.*read|division).{40}', full_text, re.I
                    )[:3],
                }
            else:
                vote_in_profile = {"url": sample_mp_url, "error": "failed_to_load"}
        else:
            vote_in_profile = {"error": "no_mp_links_found"}

        voting_findings          = probe_voting_records(page)
        voting_findings["_sample_mp_profile"] = vote_in_profile
        report["voting_records"] = voting_findings

        # Determine voting recommendation
        any_accessible = any(
            v.get("accessible") and (v.get("has_bill_numbers") or v.get("has_vote_counts"))
            for v in voting_findings.values()
            if isinstance(v, dict)
        )
        report["unknowns_resolved"]["voting_records_location"] = (
            "found_on_separate_page" if any_accessible
            else "not_found_on_profile" if not vote_in_profile.get("has_vote_field")
            else "potentially_on_profile"
        )

        browser.close()

    # ── Generate Recommendations ──────────────────────────────────────────────
    recs = []

    # Constituency/party fields
    party_field = next(
        (f for f in report["field_coverage"] if "party" in f.lower()), None
    )
    constituency_field = next(
        (f for f in report["field_coverage"] if "constituency" in f.lower()), None
    )

    if party_field:
        recs.append(f"Party field confirmed: '{party_field}' — use in FIELD_MAP")
    else:
        recs.append("WARNING: No explicit party field found — may be in bio or page header. Check raw_mp_sample.")

    if constituency_field:
        recs.append(f"Constituency field confirmed: '{constituency_field}' — use in FIELD_MAP")
    else:
        recs.append("WARNING: No explicit constituency field — may need to extract from breadcrumb or h1.")

    # Photo
    photo_rec = report["photo_source"]["recommendation"]
    if photo_rec == "listing_thumbnail":
        recs.append("Photo: Use listing page thumbnail URL — captured during Stage 1 crawl.")
    elif photo_rec == "profile_page":
        recs.append("Photo: Use profile page photo — add specific CSS selector to Stage 2 extractor.")
    else:
        recs.append("Photo: Both listing and profile photos available — prefer profile for higher resolution.")

    # Voting
    voting_rec = report["unknowns_resolved"].get("voting_records_location")
    if voting_rec == "not_found_on_profile":
        recs.append("Voting: No per-MP voting data found. Set voting_json=[] in schema; populate manually later.")
    elif voting_rec == "found_on_separate_page":
        recs.append("Voting: Data found on separate section. Build a separate voting scraper (Stage 1b).")
    else:
        recs.append("Voting: Inconclusive — check manually via probe_report.json > voting_records.")

    # Table format
    word_html_count = sum(
        1 for s in report["table_analysis"]
        for field_data in s.get("fields", {}).values()
        if isinstance(field_data, dict) and field_data.get("word_html_hits", 0) > 0
    )
    if word_html_count > 0:
        recs.append(
            f"Tables: {word_html_count} samples have Word-generated HTML. "
            "table_parser.py must strip Word styles before column detection."
        )

    report["recommendations"] = recs

    return report


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log("Parliament.go.ke Site Probe — Starting")
    log(f"Output will be saved to: {OUTPUT_FILE}")
    log("")

    try:
        report = run_probe()
    except KeyboardInterrupt:
        log("\nProbe interrupted by user.")
        sys.exit(1)

    # Save report
    OUTPUT_FILE.write_text(json.dumps(report, indent=2, ensure_ascii=False))

    # Print summary to console
    print("\n" + "=" * 60)
    print("PROBE COMPLETE — SUMMARY")
    print("=" * 60)

    p = report.get("pagination", {})
    print(f"\n1. PAGINATION")
    print(f"   Total MP links found:  {p.get('total_mp_links', '?')}")
    print(f"   Pages (0-indexed):     0 to {p.get('last_page_index', '?')}")
    print(f"   MPs per page:          {p.get('per_page', '?')}")

    print(f"\n2. FIELD COVERAGE (top fields by presence %)")
    for field, info in list(report.get("field_coverage", {}).items())[:10]:
        bar = "█" * int(info["coverage_pct"] / 10)
        print(f"   {info['coverage_pct']:5.1f}%  {bar:<10}  {field}")

    print(f"\n3. VOTING RECORDS")
    print(f"   Location: {report['unknowns_resolved'].get('voting_records_location', '?')}")

    print(f"\n4. TABLE STRUCTURES")
    for sample in report.get("table_analysis", [])[:3]:
        print(f"   {sample['name']}:")
        for field_name, info in sample.get("fields", {}).items():
            if isinstance(info, dict) and info.get("present"):
                tag    = "TABLE" if info.get("is_table") else "NON-TABLE"
                word   = f" [Word HTML: {info.get('word_html_hits',0)} patterns]" if info.get("is_table") else ""
                print(f"     {field_name}: {tag}{word}")
                if info.get("header_cells"):
                    print(f"       Headers: {info['header_cells']}")

    print(f"\n5. PHOTO SOURCE")
    print(f"   Recommendation: {report['photo_source'].get('recommendation', '?')}")
    listing_count = report['photo_source'].get('listing_photo_count', 0)
    profile_count = report['photo_source'].get('profile_photo_count', 0)
    print(f"   MPs with listing thumbnail: {listing_count}/{PROBE_SAMPLES}")
    print(f"   MPs with profile photo:     {profile_count}/{PROBE_SAMPLES}")

    print(f"\n6. RECOMMENDATIONS")
    for rec in report.get("recommendations", []):
        prefix = "⚠️ " if rec.startswith("WARNING") else "✓  "
        print(f"   {prefix}{rec}")

    print(f"\n✓ Full report saved to: {OUTPUT_FILE}")
    print("  Read probe_report.json before writing any extractor code.\n")