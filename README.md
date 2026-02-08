# Elect 2027 - Kenyan Voter Information Platform

An independent, non-partisan civic-tech platform providing balanced, sourced information about candidates, policies, and electoral integrity for Kenya's 2027 general elections (August 10, 2027).

## Features

- **Candidate Information**: Comprehensive profiles with policies, achievements, and controversies
- **Issues & Perspectives**: Balanced coverage of key policy areas
- **Vote-Buying Education**: Understanding risks and legal consequences
- **County Information**: Gubernatorial, senatorial, and parliamentary representatives
- **"What Could Have Been"**: Analysis of corruption's opportunity cost
- **Dark Mode**: User preference toggle with localStorage persistence
- **Mobile-First Design**: Optimized for all devices
- **Wikipedia Integration**: Live candidate biographies (with verification disclaimers)

## Tech Stack

### Frontend
- **Framework**: React 18 + Vite
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Router**: TanStack Router
- **Data Fetching**: TanStack Query
- **State**: React Context for theme
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with JSONB
- **ORM**: SQLAlchemy
- **Migrations**: Alembic (stub for MVP)
- **External API**: Wikipedia REST API

### Monorepo
- **Package Manager**: pnpm
- **Build Orchestration**: Turborepo
- **Shared Package**: Zod schemas + TypeScript types

## Project Structure

```
elect/
├── apps/
│   ├── frontend/          # React + Vite application
│   │   ├── src/
│   │   │   ├── pages/     # Route components
│   │   │   ├── components/
│   │   │   ├── lib/       # Utilities (API client, theme)
│   │   │   ├── router.tsx # Route definitions
│   │   │   └── main.tsx   # Entry point
│   │   ├── vite.config.ts
│   │   └── package.json
│   └── backend/           # FastAPI application
│       ├── app/
│       │   ├── main.py    # FastAPI app setup
│       │   ├── models.py  # SQLAlchemy models
│       │   ├── schemas.py # Pydantic schemas
│       │   ├── database.py
│       │   ├── routes/    # API endpoint routers
│       │   └── utils/     # Wikipedia integration
│       ├── seeds.py       # Database seeding script
│       ├── requirements.txt
│       └── pyproject.toml
├── packages/
│   └── shared/            # TypeScript types + Zod schemas
│       └── src/index.ts
├── pnpm-workspace.yaml
├── turbo.json
├── package.json
└── README.md
```

## Prerequisites

- **Node.js** 18+ and **pnpm** 8+
- **Python** 3.11+ and **Poetry** (or pip)
- **PostgreSQL** 13+ (local or Docker)
- **Git**

## Quick Start

### 1. Clone & Install Dependencies

```bash
cd /home/darwin/2027/elect

# Install Node dependencies
pnpm install

# Install Python dependencies (backend)
cd apps/backend
pip install -r requirements.txt
# OR with Poetry:
poetry install
cd ../..
```

### 2. Set Up PostgreSQL

```bash
# Option A: Using Docker
docker run --name elect-db \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=elect_2027 \
  -p 5432:5432 \
  -d postgres:15

# Option B: Local PostgreSQL
# Create database and user manually
createdb elect_2027
```

### 3. Configure Environment

```bash
# Backend environment
cd apps/backend
cp .env.example .env
# Edit .env with your database URL if not using defaults

# Frontend uses Vite proxy (see vite.config.ts)
cd ../..
```

### 4. Seed Database

```bash
cd apps/backend
python seeds.py
# This populates candidates, counties, issues, and vote-buying facts
cd ../..
```

### 5. Run Development Servers

```bash
# From project root, run both frontend and backend
pnpm dev

# Or run separately:
# Terminal 1 - Frontend (http://localhost:5173)
cd apps/frontend
pnpm dev

# Terminal 2 - Backend (http://localhost:8000)
cd apps/backend
uvicorn app.main:app --reload
```

### 6. Browse & Test

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)

## API Endpoints

### Candidates
- `GET /candidates` - List all candidates
- `GET /candidates/{slug}` - Get candidate details
- `POST /candidates` - Create (admin, requires X-API-Key: secret)
- `PATCH /candidates/{slug}` - Update (admin only)
- `DELETE /candidates/{slug}` - Delete (admin only)

### Counties
- `GET /counties` - List all counties
- `GET /counties/{name}` - Get county details (with MPs, senators, bills)
- `POST /counties` - Create (admin only)
- `PATCH /counties/{name}` - Update (append to arrays)
- `DELETE /counties/{name}` - Delete (admin only)

### Issues
- `GET /issues` - List all issues
- `GET /issues/{id}` - Get issue details
- `POST /issues` - Create (admin only)
- `PATCH /issues/{id}` - Update (admin only)
- `DELETE /issues/{id}` - Delete (admin only)

### Vote-Buying
- `GET /vote-buying-facts` - List all facts
- `GET /vote-buying-facts/{id}` - Get fact details
- `POST /vote-buying-facts` - Create (admin only)
- `PATCH /vote-buying-facts/{id}` - Update (admin only)
- `DELETE /vote-buying-facts/{id}` - Delete (admin only)

### Admin
- `GET /admin/verify` - Check admin access (requires X-API-Key: secret)

## Database Design

All data is stored in PostgreSQL with JSONB fields for flexible arrays:

### candidates
```sql
id: INTEGER PRIMARY KEY
slug: STRING UNIQUE
name: STRING
party: STRING
photo_url: STRING
bio_text: STRING
wiki_title: STRING (required for Wikipedia fetch)
good_json: JSONB (array of strings)
bad_json: JSONB (array of strings)
crazy_json: JSONB (array of strings)
policies_json: JSONB (array of {promise, details, progress, sources})
county_affiliation: STRING
updated_at: DATETIME
```

### counties
```sql
id: INTEGER PRIMARY KEY
name: STRING UNIQUE
governor_name: STRING
governor_party: STRING
governor_wiki_title: STRING
senators_json: JSONB (array of {name, party, wiki_title})
mps_json: JSONB (array of {name, constituency, party, wiki_title})
past_election_results_json: JSONB (array of {year, type, winner, votes, source})
voted_bills_json: JSONB (array of {bill_title, bill_id, vote, date, source_url})
updated_at: DATETIME
```

### issues
```sql
id: INTEGER PRIMARY KEY
title: STRING
good_points_json: JSONB (array of strings)
bad_points_json: JSONB (array of strings)
sources_json: JSONB (array of strings)
updated_at: DATETIME
```

### vote_buying_facts
```sql
id: INTEGER PRIMARY KEY
section_title: STRING
content_text: STRING
sources_json: JSONB (array of strings)
updated_at: DATETIME
```

## Adding Data

### Add a New Candidate

Make a POST request to `/candidates`:

```bash
curl -X POST http://localhost:8000/candidates \
  -H "X-API-Key: secret" \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "candidate-name",
    "name": "Full Name",
    "party": "Party Name",
    "photo_url": "https://...",
    "bio_text": "Biography...",
    "wiki_title": "Wikipedia_Title",
    "good_json": ["Achievement 1", "Achievement 2"],
    "bad_json": ["Controversy 1"],
    "crazy_json": [],
    "policies_json": [{
      "promise": "Promise title",
      "details": "Details",
      "progress": "not_started",
      "sources": ["source URL"]
    }],
    "county_affiliation": "County"
  }'
```

### Add an MP to a County

Update the county via PATCH:

```bash
curl -X PATCH http://localhost:8000/counties/Nakuru \
  -H "X-API-Key: secret" \
  -H "Content-Type: application/json" \
  -d '{
    "mps_json": [
      ... existing MPs ...
      {
        "name": "New MP",
        "constituency": "Constituency",
        "party": "Party",
        "wiki_title": "Wikipedia_Title"
      }
    ]
  }'
```

## Frontend Pages

All responses are TypeScript-typed and validated with Zod on the backend:

- `/` - Homepage with overview
- `/candidates` - List of all candidates
- `/candidates/:slug` - Candidate details with Wikipedia summary
- `/issues` - Key policy areas
- `/vote-buying` - Vote-buying risks and reporting
- `/what-could-have-been` - Corruption opportunity cost analysis
- `/counties` - County listing
- `/counties/:name` - County details (governor, MPs, senators, voted bills)
- `/resources` - Links to official sources
- `/about` - About the platform
- `/admin` - Admin dashboard (API key protected)

## Admin Access

The MVP uses a simple API key system:

```
X-API-Key: secret
```

In production:
- Replace with JWT or OAuth2
- Use environment variables (ADMIN_API_KEY)
- Implement proper role-based access control
- Add audit logging

## Deployment Considerations

### Frontend
- Build: `pnpm build` → outputs to `dist/`
- Deploy to Vercel, Netlify, or any static host
- Environment: Update API proxy in `vite.config.ts`

### Backend
- Use a production WSGI server: `gunicorn`, `uvicorn` with `supervisor`/`systemd`
- Database: Use managed PostgreSQL (AWS RDS, Digital Ocean, etc.)
- Secrets: Use `.env` from environment variables
- Consider containerizing with Docker

### Example Docker Compose (Development)

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: elect_2027
    ports:
      - "5432:5432"
  backend:
    build: ./apps/backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/elect_2027
    depends_on:
      - postgres
  frontend:
    build: ./apps/frontend
    ports:
      - "5173:5173"
```

## Contributing

To extend the platform:

1. **Add candidates/counties**: Modify `seeds.py` or use the admin API
2. **Add new pages**: Create a route in `router.tsx` and a page component
3. **Add new endpoints**: Create route files under `app/routes/`
4. **Add new data types**: Add SQLAlchemy models → Pydantic schemas → Zod types

All changes are database-driven; no frontend code changes are needed for data updates.

## Disclaimer

This is an **independent educational platform** for the 2027 elections. It is:
- ✅ Not affiliated with IEBC, any political party, or government body
- ✅ Not endorsing any candidate or position
- ✅ Encouraging independent fact-checking and verification
- ✅ Providing balanced coverage of multiple perspectives

Users should **always verify information** using official sources.

## License

MIT License - See LICENSE file for details

## Contact & Feedback

For issues, suggestions, or corrections, please open an issue on GitHub or contact the team.

---

**Built for informed voting in Kenya's 2027 elections.**
