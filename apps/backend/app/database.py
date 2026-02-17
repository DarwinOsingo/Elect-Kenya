from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os

load_dotenv()

# Database connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:password@localhost:5432/elect_2027"
)

# Create engine with async support
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("SQL_ECHO", "False") == "True",
    poolclass=NullPool,  # Disable pooling for simplicity in development
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base for models
Base = declarative_base()


def get_db() -> Session:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)
