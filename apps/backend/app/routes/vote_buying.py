from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import VoteBuyingFact
from app.schemas import VoteBuyingFactCreate, VoteBuyingFactResponse, VoteBuyingFactUpdate
from typing import List

router = APIRouter()


@router.get("", response_model=List[VoteBuyingFactResponse])
async def get_vote_buying_facts(db: Session = Depends(get_db)):
    """Get all vote-buying facts"""
    facts = db.query(VoteBuyingFact).all()
    return facts


@router.get("/{fact_id}", response_model=VoteBuyingFactResponse)
async def get_vote_buying_fact(fact_id: int, db: Session = Depends(get_db)):
    """Get a vote-buying fact by ID"""
    fact = db.query(VoteBuyingFact).filter(VoteBuyingFact.id == fact_id).first()
    if not fact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vote-buying fact with ID {fact_id} not found",
        )
    return fact


@router.post("", response_model=VoteBuyingFactResponse, status_code=status.HTTP_201_CREATED)
async def create_vote_buying_fact(
    fact: VoteBuyingFactCreate,
    db: Session = Depends(get_db),
    x_api_key: str = None,
):
    """Create a new vote-buying fact (admin only)"""
    # Simple admin check
    if x_api_key != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    db_fact = VoteBuyingFact(**fact.model_dump())
    db.add(db_fact)
    db.commit()
    db.refresh(db_fact)
    return db_fact


@router.patch("/{fact_id}", response_model=VoteBuyingFactResponse)
async def update_vote_buying_fact(
    fact_id: int,
    fact: VoteBuyingFactUpdate,
    db: Session = Depends(get_db),
    x_api_key: str = None,
):
    """Update a vote-buying fact (admin only)"""
    # Simple admin check
    if x_api_key != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    db_fact = db.query(VoteBuyingFact).filter(VoteBuyingFact.id == fact_id).first()
    if not db_fact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vote-buying fact with ID {fact_id} not found",
        )

    # Update only provided fields
    update_data = fact.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_fact, field, value)

    db.commit()
    db.refresh(db_fact)
    return db_fact


@router.delete("/{fact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vote_buying_fact(
    fact_id: int,
    db: Session = Depends(get_db),
    x_api_key: str = None,
):
    """Delete a vote-buying fact (admin only)"""
    # Simple admin check
    if x_api_key != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    db_fact = db.query(VoteBuyingFact).filter(VoteBuyingFact.id == fact_id).first()
    if not db_fact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vote-buying fact with ID {fact_id} not found",
        )

    db.delete(db_fact)
    db.commit()
