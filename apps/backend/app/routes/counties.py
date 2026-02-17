from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import County
from app.schemas import CountyCreate, CountyResponse, CountyUpdate
from typing import List

router = APIRouter()


@router.get("", response_model=List[CountyResponse])
async def get_counties(db: Session = Depends(get_db)):
    """Get all counties"""
    counties = db.query(County).all()
    return counties


@router.get("/{name}", response_model=CountyResponse)
async def get_county(name: str, db: Session = Depends(get_db)):
    """Get a county by name"""
    county = db.query(County).filter(County.name == name).first()
    if not county:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"County '{name}' not found",
        )
    return county


@router.post("", response_model=CountyResponse, status_code=status.HTTP_201_CREATED)
async def create_county(
    county: CountyCreate,
    db: Session = Depends(get_db),
    x_api_key: str = None,
):
    """Create a new county (admin only)"""
    # Simple admin check
    if x_api_key != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    # Check if county already exists
    existing = db.query(County).filter(County.name == county.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"County '{county.name}' already exists",
        )

    db_county = County(**county.model_dump())
    db.add(db_county)
    db.commit()
    db.refresh(db_county)
    return db_county


@router.patch("/{name}", response_model=CountyResponse)
async def update_county(
    name: str,
    county: CountyUpdate,
    db: Session = Depends(get_db),
    x_api_key: str = None,
):
    """Update a county (admin only)"""
    # Simple admin check
    if x_api_key != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    db_county = db.query(County).filter(County.name == name).first()
    if not db_county:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"County '{name}' not found",
        )

    # Update only provided fields
    update_data = county.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_county, field, value)

    db.commit()
    db.refresh(db_county)
    return db_county


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_county(
    name: str,
    db: Session = Depends(get_db),
    x_api_key: str = None,
):
    """Delete a county (admin only)"""
    # Simple admin check
    if x_api_key != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    db_county = db.query(County).filter(County.name == name).first()
    if not db_county:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"County '{name}' not found",
        )

    db.delete(db_county)
    db.commit()
