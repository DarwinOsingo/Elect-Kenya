import requests
import json
from datetime import datetime, timedelta
from typing import Optional
from app.schemas import WikipediaSummaryResponse

# Simple in-memory cache
_wiki_cache: dict = {}


def get_wiki_summary(wiki_title: str) -> WikipediaSummaryResponse:
    """
    Fetch Wikipedia summary for a given title.

    Args:
        wiki_title: Wikipedia article title

    Returns:
        WikipediaSummaryResponse with extract, thumbnail, and page URL
    """
    # Check cache first
    cache_key = f"wiki_{wiki_title}"
    if cache_key in _wiki_cache:
        cached = _wiki_cache[cache_key]
        if cached["expires"] > datetime.now():
            return cached["data"]

    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_title}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()

        # Extract relevant fields
        result = WikipediaSummaryResponse(
            extract=data.get("extract", "")[:800],  # Limit to 800 chars
            thumbnail_url=data.get("thumbnail", {}).get("source"),
            page_url=data.get("content_urls", {}).get("mobile", {}).get("page", ""),
            description=data.get("description"),
        )

        # Cache for 24 hours
        _wiki_cache[cache_key] = {
            "data": result,
            "expires": datetime.now() + timedelta(hours=24),
        }

        return result
    except requests.RequestException as e:
        # Fallback response if Wikipedia is unavailable
        return WikipediaSummaryResponse(
            extract=None,
            thumbnail_url=None,
            page_url=f"https://en.wikipedia.org/wiki/{wiki_title.replace(' ', '_')}",
            description=f"Wikipedia article for {wiki_title}",
        )
    except Exception as e:
        # Return minimal response on error
        return WikipediaSummaryResponse(
            extract=None,
            thumbnail_url=None,
            page_url=f"https://en.wikipedia.org/wiki/{wiki_title.replace(' ', '_')}",
            description=None,
        )


def clear_wiki_cache():
    """Clear Wikipedia cache (useful for testing)"""
    _wiki_cache.clear()
