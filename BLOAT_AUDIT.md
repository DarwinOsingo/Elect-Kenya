# 🚨 BLOAT AUDIT & CLEANUP REPORT

## Redundant Files to Remove

### Documentation (3 files are redundant)
- ❌ `BUILD_SUMMARY.md` - Duplicate of README + QUICK_START
- ❌ `DATA_MODEL.md` - Too long, merge into README
- ❌ Keep BOTH `README.md` and `QUICK_START.md` only

### Files That Don't Exist Yet (safe to ignore)
- ✓ `MP_SCRAPER.md` - Mentioned but not in our file list

---

## Unused Dependencies (Remove)

### Frontend - Remove from package.json
```json
// ❌ REMOVE THESE (not used in any component):
"@hookform/resolvers": "^3.3.0",        // Admin forms are stubs
"@radix-ui/react-accordion": "^1.0.1",  // Not implemented
"@radix-ui/react-dropdown-menu": "^2.0.5", // Not implemented
"class-variance-authority": "^0.7.0",   // Not used (CVA not in code)
"react-hook-form": "^7.48.0",           // Admin forms are stubs
"@typescript-eslint/eslint-plugin": "^6.0.0", // Optional for MVP
"@typescript-eslint/parser": "^6.0.0",  // Optional for MVP
"eslint": "^8.50.0",                    // Optional for MVP
"eslint-plugin-react-hooks": "^4.6.0",  // Optional for MVP
```

### Backend - Remove from requirements.txt
```
❌ alembic==1.13.1                      // Not used (no migrations)
❌ beautifulsoup4==4.12.2               // Not used in backend
❌ pydantic-settings==2.1.0             // Not used (using dotenv)
```

---

## Code Bloat to Clean

### Frontend Pages (All Good - No Bloat)
✓ All 11 pages are lean and used

### Backend Routes (All Good - No Bloat)
✓ All 5 route files are minimal

### Unnecessary Files in Frontend
- ❌ `apps/frontend/src/pages/Resources.tsx` - Could be merged with About
- ❌ `.eslintrc` - Not present, but if added, make optional

---

## What to Keep ✓

### Core Dependencies (MUST KEEP)
- react, react-dom
- vite, typescript
- @tanstack/react-query, @tanstack/react-router
- axios, lucide-react, clsx, tailwind-merge
- tailwindcss, postcss, autoprefixer
- fastapi, uvicorn, sqlalchemy, psycopg
- pydantic, python-dotenv, requests

### Core Documentation (MUST KEEP)
- `README.md` - Main guide
- `QUICK_START.md` - Quick setup
- `.env.example` - Config template

---

## Summary

| Category | Count | Action |
|----------|-------|--------|
| Redundant Docs | 1 | Remove DATA_MODEL.md |
| Unused Frontend Deps | 8 | Remove from package.json |
| Unused Backend Deps | 3 | Remove from requirements.txt |
| Unused Pages | 1 | Consider merging Resources → About |
| Code Bloat | 0 | All code is lean ✓ |

**Total Bloat: 13 items to remove**
**Space Saved: ~50 MB (node_modules cleanup)**

