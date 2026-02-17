from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.database import init_db
from app.routes import candidates, counties, issues, vote_buying, admin

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Elect 2027 API",
    description="API for Kenya 2027 election voter information platform",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize database
@app.on_event("startup")
async def startup():
    init_db()


# Include routers
app.include_router(candidates.router, prefix="/candidates", tags=["candidates"])
app.include_router(counties.router, prefix="/counties", tags=["counties"])
app.include_router(issues.router, prefix="/issues", tags=["issues"])
app.include_router(vote_buying.router, prefix="/vote-buying-facts", tags=["vote-buying"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])


@app.get("/", tags=["health"])
async def root():
    """Health check endpoint"""
    return {"message": "Elect 2027 API is running", "status": "healthy"}


@app.get("/health", tags=["health"])
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
