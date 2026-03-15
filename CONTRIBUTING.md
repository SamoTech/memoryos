# Contributing to MemoryOS

Thank you for your interest in contributing! 🎉

## Ways to Contribute

- 🐛 **Bug reports** — open an issue with steps to reproduce
- 💡 **Feature requests** — open an issue with your use case
- 🔧 **Code** — open a PR (see dev setup below)
- 📖 **Docs** — improve any `.md` file
- ⭐ **Star** — helps others discover the project

## Dev Setup

```bash
git clone https://github.com/SamoTech/memoryos
cd memoryos

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e '.[dev]'

# Run backend
uvicorn app.main:app --reload --port 8765

# Run tests
pytest tests/ -v --tb=short

# Lint + type check
ruff check app cli
mypy app --ignore-missing-imports

# Frontend
cd ../frontend
npm install
npm run dev          # http://localhost:3000

# Extension
cd ../extension
npm install
npm run build        # outputs to extension/dist/
npm run watch        # watch mode
```

## Code Style

- **Python**: ruff formatter, 88 char line limit, type hints everywhere
- **TypeScript**: strict mode, no `any` (use `unknown`)
- **Commits**: conventional commits (`feat:`, `fix:`, `docs:`, `chore:`)

## PR Checklist

- [ ] Tests pass (`pytest tests/ -v`)
- [ ] Linting passes (`ruff check app cli`)
- [ ] Added/updated tests for new features
- [ ] Updated docs if API changed
- [ ] Added entry to `CHANGELOG.md`

## Project Structure

```
memoryos/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/   # FastAPI route handlers
│   │   ├── core/               # Config, DB, vector store
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── services/           # Business logic
│   │   ├── workers/            # Background tasks
│   │   └── main.py             # FastAPI app entry
│   └── cli/
│       └── main.py             # Click CLI
├── extension/
│   ├── content/                # Per-site content scripts
│   ├── popup/                  # Extension popup UI
│   └── background.ts           # Service worker
├── frontend/
│   └── src/
│       ├── app/                # Next.js pages
│       ├── components/         # React components
│       ├── hooks/              # Custom React hooks
│       └── lib/                # API client
├── docs/                       # Full documentation
└── scripts/                    # Build + install scripts
```

## Questions?

Open a [GitHub Discussion](https://github.com/SamoTech/memoryos/discussions) or tag [@SamoTech](https://github.com/SamoTech) in an issue.
