# Elect 2027 - Kenyan Voter Information Platform

An independent, non-partisan civic-tech platform providing balanced, sourced information about candidates, policies, and electoral integrity for Kenya's 2027 general elections (August 10, 2027).

## ⚡ Quick Start (5 Minutes)

See **[QUICK_START.md](./QUICK_START.md)** for step-by-step setup.

## ✨ Features

- 🗳️ **Candidate Profiles**: Policies, achievements, controversies, Wikipedia integration
- 📋 **Policy Issues**: Economy, healthcare, education, corruption (balanced perspectives)
- ⚠️ **Vote-Buying Education**: Risks, mechanics, reporting mechanisms
- 🏛️ **County Info**: Governors, MPs, senators, voting records by county
- 💡 **"What Could Have Been"**: Corruption's opportunity cost analysis
- 🌙 **Dark Mode**: User preference with localStorage
- 📱 **Mobile-First**: Responsive design for all devices

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18 + Vite + TypeScript + Tailwind CSS |
| **Backend** | FastAPI + SQLAlchemy + PostgreSQL |
| **Data** | JSONB (flexible, no migrations needed) |
| **Package Mgr** | pnpm (monorepo) + Turborepo (orchestration) |
| **Types** | Zod schemas + TypeScript (shared) |

### Minimal Dependencies

**Frontend:** React, Vite, TanStack (Query/Router), Tailwind, Axios, Lucide Icons
**Backend:** FastAPI, SQLAlchemy, Psycopg, Pydantic, Requests
**Removed:** ESLint, React Hook Form, Radix UI components, Alembic, BeautifulSoup (not used)

## 📚 Database Schema

### Candidates Table
```
id, slug (UNIQUE), name, party, photo_url, bio_text, wiki_title,
good_json [], bad_json [], crazy_json [],
policies_json [{promise, details, progress, sources}],
county_affiliation, updated_at
```

### Counties Table
```
id, name (UNIQUE), governor_name, governor_party, governor_wiki_title,
senators_json [{name, party, wiki_title}],
mps_json [{name, constituency, party, wiki_title}],
past_election_results_json [{year, type, winner, votes, source}],
voted_bills_json [{bill_title, bill_id, vote, date, source_url}],
updated_at
```

### Issues, Vote-Buying Facts
Simple JSONB arrays for flexible content.

## 🚀 Installation

### Prerequisites
- Node.js 18+ & pnpm 8+
- Python 3.11+ & pip
- PostgreSQL 13+

### Setup

```bash
# 1. Install dependencies
pnpm install
cd apps/backend && pip install -r requirements.txt && cd ../..

# 2. Start PostgreSQL (Docker)
docker run --name elect-db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=elect_2027 -p 5432:5432 -d postgres:15

# 3. Seed database
cd apps/backend && python seeds.py && cd ../..

# 4. Run development servers (separate terminals)
# Terminal 1:
cd apps/frontend && pnpm dev          # http://localhost:5173

# Terminal 2:
cd apps/backend && uvicorn app.main:app --reload  # http://localhost:8000
```

## 📡 API Endpoints

All endpoints accept/return JSON with full CORS support.

### Candidates
- `GET /candidates` - List all
- `GET /candidates/{slug}` - Get candidate with Wikipedia summary
- `POST /candidates` - Create (admin: X-API-Key: secret)
- `PATCH /candidates/{slug}` - Update (admin)
- `DELETE /candidates/{slug}` - Delete (admin)

### Counties
- `GET /counties` - List all
- `GET /counties/{name}` - Get county (governors, MPs, senators, bills)
- `POST /counties` - Create (admin)
- `PATCH /counties/{name}` - Update (admin)
- `DELETE /counties/{name}` - Delete (admin)

### Issues, Vote-Buying Facts
Same CRUD pattern as above.

### Admin
- `GET /admin/verify` - Check API key validity (X-API-Key header)

**Interactive Docs:** http://localhost:8000/docs (Swagger UI) or `/redoc`

## 📖 Documentation

| File | Purpose |
|------|---------|
| **QUICK_START.md** | 10-minute setup guide (start here!) |
| **BLOAT_AUDIT.md** | Removed dependencies & rationale |
| **README.md (this)** | Architecture, features, API reference |

## 🎯 How to Extend

### Add a New Candidate (No Code Changes)

```bash
curl -X POST http://localhost:8000/candidates \
  -H "X-API-Key: secret" \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "candidate-slug",
    "name": "Full Name",
    "party": "Party",
    "photo_url": "https://...",
    "bio_text": "Biography...",
    "wiki_title": "Wikipedia_Title",
    "good_json": ["Achievement 1", "Achievement 2"],
    "bad_json": ["Controversy"],
    "crazy_json": [],
    "policies_json": [{
      "promise": "Promise",
      "details": "Details",
      "progress": "not_started",
      "sources": ["https://..."]
    }],
    "county_affiliation": "County"
  }'
```

### Add MPs to a County

```bash
curl -X PATCH http://localhost:8000/counties/Nakuru \
  -H "X-API-Key: secret" \
  -H "Content-Type: application/json" \
  -d '{
    "mps_json": [
      ... existing MPs ...,
      {
        "name": "New MP",
        "constituency": "Const",
        "party": "Party",
        "wiki_title": "Wikipedia_Title"
      }
    ]
  }'
```

### Add a New Page

1. Create component: `apps/frontend/src/pages/NewPage.tsx`
2. Add route in `apps/frontend/src/router.tsx`
3. Done! (No backend changes)

## 🗄️ Viewing Database Content

### Via CLI
```bash
psql -U postgres -d elect_2027
SELECT name, party FROM candidates;
SELECT jsonb_pretty(mps_json) FROM counties WHERE name = 'Nakuru';
\q
```

### Via REST API
```bash
curl http://localhost:8000/candidates | jq
curl http://localhost:8000/candidates/william-ruto | jq
curl http://localhost:8000/counties | jq
```

### Via Browser
Visit http://localhost:8000/docs and test endpoints interactively

## 🐳 Docker Compose (Optional)

```bash
docker-compose up  # Runs PostgreSQL + Backend
# Then in another terminal:
cd apps/frontend && pnpm dev  # Frontend
```

## 🚢 Deployment

### Frontend
1. `pnpm build` → outputs `dist/`
2. Deploy to Vercel, Netlify, or any static host
3. Update API proxy in `vite.config.ts` if deployed backend URL differs

### Backend
1. Use production database (AWS RDS, DigitalOcean, etc.)
2. Set env vars: `DATABASE_URL`, `CORS_ORIGINS`, `ADMIN_API_KEY`
3. Use `gunicorn` + `uvicorn` production server
4. Enable HTTPS (automatic with most platforms)

## 🔐 Admin Authentication

**MVP:** API key in header
```
X-API-Key: secret
```

**Production:** Replace with JWT or OAuth2 (see backend code comments)

## 📊 Project Stats

- **11 Frontend Pages** (Home, Candidates, Issues, Vote-Buying, Counties, Admin, About, Resources, etc.)
- **5 API Resources** (25+ endpoints with full CRUD)
- **5 Database Tables** (Candidates, Counties, Issues, Vote-Buying, News stub)
- **Seed Data:** 6 candidates, 2 counties (Nakuru, Kisumu), 4 issues, 4 vote-buying facts
- **Code:** ~50 files, pure TypeScript front-to-back
- **Bundle:** <200 KB JS (gzipped) + ~50 KB CSS

## 🎓 Design Philosophy

**Content in DB, Code in Git:** Update candidates/counties/policies via API or admin forms—no code changes needed. Database evolves; codebase stays stable.

## 🤝 Contributing

To extend the platform:
1. Add data via API (POST/PATCH endpoints)
2. Add pages via `router.tsx` + new component
3. Add backend endpoints in `app/routes/` folder
4. All data types are Zod-validated (FE) and Pydantic-validated (BE)

## ⚠️ Disclaimer

This is an **independent educational platform**:
- ✅ Not affiliated with IEBC, any political party, or government
- ✅ Encouraging independent fact-checking
- ✅ Providing balanced, multi-perspective coverage
- ✅ All sources are cited

**Always verify information** using official sources before forming opinions.

## 📞 Support

- **Setup issues?** See [QUICK_START.md](./QUICK_START.md)
- **Database questions?** Run `psql -U postgres -d elect_2027` and explore
- **API issues?** Visit http://localhost:8000/docs for interactive testing

## 📄 License

MIT License. See LICENSE file.

---

**Built for informed voting in Kenya's 2027 elections.**
