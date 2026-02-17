from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Candidate
from app.schemas import CandidateCreate, CandidateResponse, CandidateUpdate
from app.utils.wikipedia import get_wiki_summary
from typing import List

router = APIRouter()


@router.get("", response_model=List[CandidateResponse])
async def get_candidates(db: Session = Depends(get_db)):
    """Get all candidates"""
    candidates = db.query(Candidate).all()
    return candidates


@router.get("/{slug}", response_model=CandidateResponse)
async def get_candidate(slug: str, db: Session = Depends(get_db)):
    """Get a candidate by slug"""
    candidate = db.query(Candidate).filter(Candidate.slug == slug).first()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with slug '{slug}' not found",
        )
    return candidate


@router.post("", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
async def create_candidate(
    candidate: CandidateCreate,
    db: Session = Depends(get_db),
    x_api_key: str = None,  # Type hint without validation for now
):
    """Create a new candidate (admin only)"""
    # Simple admin check - in production, use JWT or similar
    if x_api_key != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    # Check if candidate already exists
    existing = db.query(Candidate).filter(Candidate.slug == candidate.slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Candidate with slug '{candidate.slug}' already exists",
        )

    db_candidate = Candidate(**candidate.model_dump())
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate


@router.patch("/{slug}", response_model=CandidateResponse)
async def update_candidate(
    slug: str,
    candidate: CandidateUpdate,
    db: Session = Depends(get_db),
    x_api_key: str = None,
):
    """Update a candidate (admin only)"""
    # Simple admin check
    if x_api_key != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    db_candidate = db.query(Candidate).filter(Candidate.slug == slug).first()
    if not db_candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with slug '{slug}' not found",
        )

    # Update only provided fields
    update_data = candidate.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_candidate, field, value)

    db.commit()
    db.refresh(db_candidate)
    return db_candidate


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(
    slug: str,
    db: Session = Depends(get_db),
    x_api_key: str = None,
):
    """Delete a candidate (admin only)"""
    # Simple admin check
    if x_api_key != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    db_candidate = db.query(Candidate).filter(Candidate.slug == slug).first()
    if not db_candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with slug '{slug}' not found",
        )

    db.delete(db_candidate)
    db.commit()
