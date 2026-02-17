from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import List, Optional


# Candidate Schemas
class PolicyCreate(BaseModel):
    promise: str
    details: str
    progress: str = "not_started"  # not_started, in_progress, completed
    sources: List[str] = []


class PolicyResponse(PolicyCreate):
    pass


class CandidateCreate(BaseModel):
    slug: str
    name: str
    party: str
    photo_url: str
    bio_text: str
    wiki_title: str
    good_json: List[str] = []
    bad_json: List[str] = []
    crazy_json: List[str] = []
    policies_json: List[PolicyCreate] = []
    county_affiliation: Optional[str] = None


class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    party: Optional[str] = None
    photo_url: Optional[str] = None
    bio_text: Optional[str] = None
    wiki_title: Optional[str] = None
    good_json: Optional[List[str]] = None
    bad_json: Optional[List[str]] = None
    crazy_json: Optional[List[str]] = None
    policies_json: Optional[List[PolicyCreate]] = None
    county_affiliation: Optional[str] = None


class CandidateResponse(CandidateCreate):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True


# County Schemas
class SenatorCreate(BaseModel):
    name: str
    party: str
    wiki_title: str


class MPCreate(BaseModel):
    name: str
    constituency: str
    party: str
    wiki_title: str


class ElectionResultCreate(BaseModel):
    year: int
    type: str  # presidential, gubernatorial, mp
    winner: str
    votes: Optional[int] = None
    source: str


class VotedBillCreate(BaseModel):
    bill_title: str
    bill_id: str
    vote: str  # Yes, No, Abstain
    date: str  # YYYY-MM-DD
    source_url: str


class CountyCreate(BaseModel):
    name: str
    governor_name: str
    governor_party: str
    governor_wiki_title: str
    senators_json: List[SenatorCreate] = []
    mps_json: List[MPCreate] = []
    past_election_results_json: List[ElectionResultCreate] = []
    voted_bills_json: List[VotedBillCreate] = []


class CountyUpdate(BaseModel):
    name: Optional[str] = None
    governor_name: Optional[str] = None
    governor_party: Optional[str] = None
    governor_wiki_title: Optional[str] = None
    senators_json: Optional[List[SenatorCreate]] = None
    mps_json: Optional[List[MPCreate]] = None
    past_election_results_json: Optional[List[ElectionResultCreate]] = None
    voted_bills_json: Optional[List[VotedBillCreate]] = None


class CountyResponse(CountyCreate):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True


# Issue Schemas
class IssueCreate(BaseModel):
    title: str
    good_points_json: List[str] = []
    bad_points_json: List[str] = []
    sources_json: List[str] = []


class IssueUpdate(BaseModel):
    title: Optional[str] = None
    good_points_json: Optional[List[str]] = None
    bad_points_json: Optional[List[str]] = None
    sources_json: Optional[List[str]] = None


class IssueResponse(IssueCreate):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True


# Vote Buying Schemas
class VoteBuyingFactCreate(BaseModel):
    section_title: str
    content_text: str
    sources_json: List[str] = []


class VoteBuyingFactUpdate(BaseModel):
    section_title: Optional[str] = None
    content_text: Optional[str] = None
    sources_json: Optional[List[str]] = None


class VoteBuyingFactResponse(VoteBuyingFactCreate):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True


# Wikipedia Schema
class WikipediaSummaryResponse(BaseModel):
    extract: Optional[str] = None
    thumbnail_url: Optional[str] = None
    page_url: str
    description: Optional[str] = None
