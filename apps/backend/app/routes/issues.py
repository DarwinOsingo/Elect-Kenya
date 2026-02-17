from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Issue
from app.schemas import IssueCreate, IssueResponse, IssueUpdate
from typing import List

router = APIRouter()


@router.get("", response_model=List[IssueResponse])
async def get_issues(db: Session = Depends(get_db)):
    """Get all issues"""
    issues = db.query(Issue).all()
    return issues


@router.get("/{issue_id}", response_model=IssueResponse)
async def get_issue(issue_id: int, db: Session = Depends(get_db)):
    """Get an issue by ID"""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue with ID {issue_id} not found",
        )
    return issue


@router.post("", response_model=IssueResponse, status_code=status.HTTP_201_CREATED)
async def create_issue(
    issue: IssueCreate,
    db: Session = Depends(get_db),
    x_api_key: str = None,
):
    """Create a new issue (admin only)"""
    # Simple admin check
    if x_api_key != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    db_issue = Issue(**issue.model_dump())
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


@router.patch("/{issue_id}", response_model=IssueResponse)
async def update_issue(
    issue_id: int,
    issue: IssueUpdate,
    db: Session = Depends(get_db),
    x_api_key: str = None,
):
    """Update an issue (admin only)"""
    # Simple admin check
    if x_api_key != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not db_issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue with ID {issue_id} not found",
        )

    # Update only provided fields
    update_data = issue.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_issue, field, value)

    db.commit()
    db.refresh(db_issue)
    return db_issue


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    x_api_key: str = None,
):
    """Delete an issue (admin only)"""
    # Simple admin check
    if x_api_key != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not db_issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue with ID {issue_id} not found",
        )

    db.delete(db_issue)
    db.commit()
