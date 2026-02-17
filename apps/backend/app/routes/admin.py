from fastapi import APIRouter, Header, HTTPException, status, Depends
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.mp_scraper import scrape_and_seed_mps

router = APIRouter()


@router.get("/verify")
async def verify_admin(x_api_key: Optional[str] = Header(None)):
    """Verify admin access with API key"""
    # Simple admin check - in production, use proper auth
    if x_api_key != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return {"status": "authorized", "role": "admin"}


@router.post("/scrape-mps")
async def scrape_mps(
    x_api_key: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Scrape MPs from parliament.go.ke and update the database
    Requires admin API key in headers
    """
    # Simple admin check - in production, use proper auth
    if x_api_key != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    
    try:
        result = scrape_and_seed_mps(db)
        if result:
            return {
                "status": "success",
                "message": "MPs scraped and database updated",
                "total_mps": result.get("total_mps", 0),
                "counties": len(result.get("by_county", {})),
                "scraped_at": result.get("scraped_at")
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Scraping failed"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during scraping: {str(e)}"
        )
