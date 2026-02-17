# Quick Start Guide

Get **Elect 2027** running locally in 10 minutes.

## Prerequisites Checklist

- [ ] Node.js 18+ (`node --version`)
- [ ] pnpm 8+ (`pnpm --version`)
- [ ] Python 3.11+ (`python --version`)
- [ ] PostgreSQL 13+ (local or Docker)
- [ ] Git

## Step-by-Step

### 1. Clone & Navigate (1 min)

```bash
cd /home/darwin/2027/elect
```

### 2. Install Dependencies (3 min)

```bash
# Install Node dependencies
pnpm install

# Install Python dependencies
cd apps/backend
pip install -r requirements.txt
cd ../..
```

### 3. Start Database (2 min)

**Option A: Docker** (easiest)
```bash
docker run --name elect-db \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=elect_2027 \
  -p 5432:5432 \
  -d postgres:15
```

**Option B: Docker Compose**
```bash
docker-compose up postgres
```

**Option C: Local PostgreSQL**
```bash
createdb elect_2027  # Requires local PostgreSQL
```

### 4. Seed Database (2 min)

```bash
cd apps/backend
python seeds.py
cd ../..
```

Expected output:
```
🌱 Starting database seeding...
✓ Database initialized
✓ Added candidate: William Kipchoge Ruto
✓ Added candidate: Fred Koros Matiang'i
... (more candidates, counties, issues)
✅ Database seeding completed successfully!
```

### 5. Start Development Servers (2 min)

**Terminal 1: Frontend**
```bash
cd apps/frontend
pnpm dev
# Opens http://localhost:5173
```

**Terminal 2: Backend**
```bash
cd apps/backend
uvicorn app.main:app --reload
# Runs on http://localhost:8000
# Docs: http://localhost:8000/docs
```

### 6. Browse & Test (1 min)

- **Homepage**: http://localhost:5173
- **Candidates**: http://localhost:5173/candidates
- **API Docs**: http://localhost:8000/docs
- **Admin**: http://localhost:5173/admin (key: "secret")

## Using Docker Compose (Alternative)

If you prefer everything in containers:

```bash
# Start database and backend
docker-compose up

# In another terminal, start frontend
cd apps/frontend
pnpm dev
```

## Testing API Endpoints

```bash
# Get all candidates
curl http://localhost:8000/candidates

# Get specific candidate
curl http://localhost:8000/candidates/william-ruto

# Get all counties
curl http://localhost:8000/counties

# Create a new issue (admin)
curl -X POST http://localhost:8000/issues \
  -H "X-API-Key: secret" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Issue",
    "good_points_json": ["Point 1"],
    "bad_points_json": ["Point 2"],
    "sources_json": ["source"]
  }'
```

## Common Issues

### "Cannot connect to database"
- Check PostgreSQL is running: `psql -h localhost -U postgres`
- Verify DATABASE_URL in `.env` (should be `postgresql://postgres:password@localhost:5432/elect_2027`)
- Reset: `docker-compose down postgres && docker-compose up postgres`

### "Port 5173 already in use"
```bash
# Kill process on port 5173
lsof -i :5173 | grep -v PID | awk '{print $2}' | xargs kill -9
```

### "Port 8000 already in use"
```bash
# Kill process on port 8000
lsof -i :8000 | grep -v PID | awk '{print $2}' | xargs kill -9
```

### "ModuleNotFoundError: No module named 'app'"
- Ensure you're in `apps/backend` when running Python commands
- Or ensure `PYTHONPATH=.` is set: `PYTHONPATH=. python seeds.py`

## Next Steps

1. **Explore the admin dashboard**: http://localhost:5173/admin (key: "secret")
2. **Add more candidates**: POST to `/candidates` with API key
3. **Add more data**: Modify `seeds.py` and reseed
4. **Customize styling**: Edit Tailwind config in `apps/frontend/tailwind.config.ts`
5. **Deploy**: Follow deployment guide in main README

## Need Help?

- Backend errors? Check `apps/backend` terminal for logs
- Frontend errors? Check browser console (F12)
- Database issues? Check PostgreSQL logs: `docker logs elect-db`
- API issues? Visit http://localhost:8000/docs for interactive docs

---

**You're all set! Start building.** 🚀
