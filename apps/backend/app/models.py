from sqlalchemy import Column, Integer, String, DateTime, JSON, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    party = Column(String, nullable=False)
    photo_url = Column(String, nullable=True)
    bio_text = Column(String, nullable=False)
    wiki_title = Column(String, nullable=False)
    good_json = Column(JSON, default=list)  # Array of achievements
    bad_json = Column(JSON, default=list)  # Array of controversies
    crazy_json = Column(JSON, default=list)  # Array of questionable claims
    policies_json = Column(JSON, default=list)  # Array of {promise, details, progress, sources}
    county_affiliation = Column(String, nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class County(Base):
    __tablename__ = "counties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    governor_name = Column(String, nullable=False)
    governor_party = Column(String, nullable=False)
    governor_wiki_title = Column(String, nullable=False)
    senators_json = Column(JSON, default=list)  # Array of {name, party, wiki_title}
    mps_json = Column(JSON, default=list)  # Array of {name, constituency, party, wiki_title}
    past_election_results_json = Column(JSON, default=list)  # Array of {year, type, winner, votes, source}
    voted_bills_json = Column(JSON, default=list)  # Array of {bill_title, bill_id, vote, date, source_url}
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class MP(Base):
    __tablename__ = "mps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    county = Column(String, nullable=True, index=True)
    constituency = Column(String, nullable=True)
    party = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    profile_url = Column(String, nullable=True, unique=True)
    committees_json = Column(JSON, default=list)  # Array of committee names
    wiki_title = Column(String, nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    good_points_json = Column(JSON, default=list)  # Array of positive approaches
    bad_points_json = Column(JSON, default=list)  # Array of concerns
    sources_json = Column(JSON, default=list)  # Array of sources
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class VoteBuyingFact(Base):
    __tablename__ = "vote_buying_facts"

    id = Column(Integer, primary_key=True, index=True)
    section_title = Column(String, nullable=False)
    content_text = Column(String, nullable=False)
    sources_json = Column(JSON, default=list)  # Array of sources
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class NewsUpdate(Base):
    __tablename__ = "news_updates"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    source_url = Column(String, nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
