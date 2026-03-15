<div align="center">

<img src="https://img.shields.io/badge/-%F0%9F%A7%A0%20MemoryOS-6366f1?style=for-the-badge&logoColor=white" alt="MemoryOS" height="40" />

# 🧠 MemoryOS

### *Your AI finally remembers you.*

> Local-first AI memory layer. 100% private. Zero cloud. Works with every LLM.

---

<!-- Core badges -->
[![License: MIT](https://img.shields.io/badge/License-MIT-6366f1.svg?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776ab.svg?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-000000.svg?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4-3178c6.svg?style=flat-square&logo=typescript&logoColor=white)](https://typescriptlang.org)

<!-- Quality badges -->
[![CI](https://img.shields.io/github/actions/workflow/status/SamoTech/memoryos/ci.yml?branch=main&style=flat-square&label=CI&logo=github)](https://github.com/SamoTech/memoryos/actions)
[![Release](https://img.shields.io/github/v/release/SamoTech/memoryos?style=flat-square&color=22c55e&logo=github)](https://github.com/SamoTech/memoryos/releases)
[![PyPI](https://img.shields.io/pypi/v/memoryos?style=flat-square&logo=pypi&logoColor=white&color=6366f1)](https://pypi.org/project/memoryos)
[![PyPI Downloads](https://img.shields.io/pypi/dm/memoryos?style=flat-square&logo=pypi&logoColor=white&color=4f46e5)](https://pypi.org/project/memoryos)

<!-- Community badges -->
[![Stars](https://img.shields.io/github/stars/SamoTech/memoryos?style=flat-square&logo=github&color=f59e0b)](https://github.com/SamoTech/memoryos/stargazers)
[![Forks](https://img.shields.io/github/forks/SamoTech/memoryos?style=flat-square&logo=github&color=6366f1)](https://github.com/SamoTech/memoryos/network/members)
[![Issues](https://img.shields.io/github/issues/SamoTech/memoryos?style=flat-square&logo=github&color=ef4444)](https://github.com/SamoTech/memoryos/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/SamoTech/memoryos/pulls)
[![Contributors](https://img.shields.io/github/contributors/SamoTech/memoryos?style=flat-square&color=8b5cf6)](https://github.com/SamoTech/memoryos/graphs/contributors)

<!-- Tech badges -->
[![SQLite](https://img.shields.io/badge/SQLite-FTS5-003b57.svg?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-ff6b35.svg?style=flat-square)](https://trychroma.com)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20AI-000000.svg?style=flat-square)](https://ollama.ai)
[![sentence-transformers](https://img.shields.io/badge/sentence--transformers-Embeddings-f97316.svg?style=flat-square)](https://sbert.net)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ed.svg?style=flat-square&logo=docker&logoColor=white)](docker-compose.yml)

<!-- Support badges -->
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-ea4aaa.svg?style=flat-square&logo=github-sponsors)](https://github.com/sponsors/SamoTech)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support-ff5e5b.svg?style=flat-square&logo=ko-fi&logoColor=white)](https://ko-fi.com/samotech)
[![Made in Egypt](https://img.shields.io/badge/Made%20in-%F0%9F%87%AA%F0%9F%87%AC%20Egypt-cc0000.svg?style=flat-square)](https://github.com/SamoTech)

</div>

---

## 📖 Table of Contents

- [The Problem](#-the-problem)
- [How It Works](#-how-it-works)
- [Demo](#-demo)
- [Quick Install](#-quick-install)
- [Browser Extension](#-browser-extension)
- [CLI Reference](#-cli-reference)
- [API Reference](#-api-reference)
- [Configuration](#-configuration)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Docker](#-docker)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Security](#-security)
- [License](#-license)

---

## 😤 The Problem

You use ChatGPT, Claude, Cursor, and Gemini **every single day**.

But every new session starts from **absolute zero**.

The AI has no idea:
- Who you are
- What you're building
- What decisions you made last week
- That you hate Python 2 and love FastAPI
- That you already tried that approach and it failed

**This is the AI amnesia problem. MemoryOS fixes it.**

---

## ✨ How It Works

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║  1. CAPTURE   →   Extension watches your AI chats        ║
║                   (ChatGPT, Claude, Gemini, Cursor)      ║
║                                                           ║
║  2. STORE     →   Local SQLite + ChromaDB                ║
║                   100% on your machine, never uploaded   ║
║                                                           ║
║  3. RETRIEVE  →   Hybrid search: semantic + keyword      ║
║                   Inject context into any AI chat        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 🎬 Demo

```bash
# Install
pip install memoryos && memoryos start

# You chat with ChatGPT: "I'm building a SaaS with Next.js and FastAPI"
# Extension silently captures this.

# Next day, in a new Claude session:
$ memoryos ask "what am I building?"

📋 Relevant context from your memories:

[chatgpt | 2026-03-14] Building a SaaS with Next.js and FastAPI.
Decided to use Zustand for state management.
Using Vercel for frontend deployment.
```

Paste that context into your next AI session. It now knows everything.

---

## ⚡ Quick Install

### One-line install (Linux / macOS)

```bash
curl -fsSL https://raw.githubusercontent.com/SamoTech/memoryos/main/scripts/install.sh | bash
```

### Via pip

```bash
pip install memoryos
memoryos start
# → Opens dashboard at http://localhost:3000
# → API running at http://localhost:8765
```

### Via Docker

```bash
git clone https://github.com/SamoTech/memoryos
cd memoryos
docker-compose up -d
# Dashboard: http://localhost:3000
# API:       http://localhost:8765
```

### Requirements

| Requirement | Version |
|---|---|
| Python | 3.11+ |
| Node.js (dashboard only) | 18+ |
| RAM | 512 MB minimum |
| Disk | 500 MB (model included) |

---

## 🌐 Browser Extension

### Install

1. Clone the repo
2. Run `bash scripts/build-extension.sh`
3. Open Chrome → `chrome://extensions/` → Enable *Developer mode*
4. Click *Load unpacked* → select `extension/dist/`

### Supported Sites (Auto-capture)

| Site | Selector Strategy | Status |
|---|---|---|
| ChatGPT (chat.openai.com) | `data-message-author-role` | ✅ Stable |
| Claude (claude.ai) | `data-testid="human-turn"` | ✅ Stable |
| Gemini (gemini.google.com) | `.query-text` + `model-response` | ✅ Stable |
| Any site | Generic DOM heuristics | ⚙️ Opt-in |

### How capture works

1. `MutationObserver` detects new AI messages
2. Content hash deduplication prevents duplicates
3. Background service worker batches + queues
4. Bulk POST to `localhost:8765/api/v1/memories/bulk` every 2 seconds
5. Green dot flashes on successful capture

---

## 💻 CLI Reference

```bash
# Server lifecycle
memoryos start                          # Start server + open dashboard
memoryos start --no-browser             # Headless start
memoryos stop                           # Stop server

# Memory operations
memoryos add "Decided to use Zustand"   # Add memory manually
memoryos add "Using FastAPI" -t "backend,python"  # With tags
memoryos forget <id>                    # Soft-delete a memory
memoryos pin <id>                       # Pin important memory

# Search & retrieval
memoryos search "react hooks"           # Semantic search
memoryos search "auth" --source claude  # Filter by source
memoryos search "deploy" -n 20          # More results
memoryos ask "what auth approach did I use?"  # Get AI-ready context

# Data management
memoryos stats                          # Show statistics
memoryos export --format markdown       # Export to Markdown
memoryos export --format json -o backup # Export to JSON file
memoryos export --format csv            # Export to CSV
```

---

## 🔌 API Reference

Full docs: [docs/API.md](docs/API.md) | Interactive: `http://localhost:8765/docs`

```
GET    /health                           Server health + config

GET    /api/v1/memories                  List memories
POST   /api/v1/memories                  Add memory
POST   /api/v1/memories/bulk             Bulk add (used by extension)
GET    /api/v1/memories/{id}             Get memory
PUT    /api/v1/memories/{id}             Update memory
DELETE /api/v1/memories/{id}             Forget memory
POST   /api/v1/memories/{id}/pin         Toggle pin

GET    /api/v1/search?q=...              Hybrid semantic+keyword search
POST   /api/v1/search/similar            Find similar to text
GET    /api/v1/search/context?q=...      Get prompt-ready context

GET    /api/v1/sessions                  List sessions
POST   /api/v1/sessions                  Create session
GET    /api/v1/sessions/{id}             Session + memories
GET    /api/v1/sessions/{id}/summary     AI summary

GET    /api/v1/tags                      List tags
GET    /api/v1/tags/{name}/memories      Memories by tag

GET    /api/v1/stats                     Memory statistics
GET    /api/v1/export?format=...         Export (json/markdown/csv/obsidian)
POST   /api/v1/summarize                 Summarize text
POST   /api/v1/summarize/pending         Summarize all unsummarized
```

### Quick API example

```python
import requests

api = "http://localhost:8765"

# Add a memory
requests.post(f"{api}/api/v1/memories", json={
    "content": "Decided to use PostgreSQL instead of MySQL for the main DB",
    "source": "manual",
    "tags": ["database", "architecture"]
})

# Search
results = requests.get(f"{api}/api/v1/search", params={"q": "database choice"}).json()
for r in results:
    print(r["memory"]["content"], "→ score:", r["score"])

# Get context for your AI prompt
ctx = requests.get(f"{api}/api/v1/search/context", params={"q": "backend stack"}).json()
print(ctx["context"])
```

---

## ⚙️ Configuration

Edit `~/.memoryos/.env`:

```env
# ── Server ──────────────────────────────
HOST=127.0.0.1
PORT=8765
DASHBOARD_PORT=3000
DEBUG=false

# ── Storage ─────────────────────────────
DATA_DIR=~/.memoryos
# DB_URL=sqlite+aiosqlite:///~/.memoryos/memories.db

# ── Embeddings ──────────────────────────
EMBEDDING_PROVIDER=local          # local | openai
EMBEDDING_MODEL=all-MiniLM-L6-v2  # any sentence-transformers model

# ── Summarization ────────────────────────
SUMMARIZER_PROVIDER=ollama        # ollama | groq | openai
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# GROQ_API_KEY=gsk_...
# GROQ_MODEL=llama3-70b-8192

# OPENAI_API_KEY=sk-...
# OPENAI_MODEL=gpt-4o-mini

# ── Memory Behaviour ────────────────────
AUTO_SUMMARIZE=true
AUTO_SUMMARIZE_THRESHOLD=500      # chars
IMPORTANCE_SCORING=true
DATA_RETENTION_DAYS=0             # 0 = keep forever
```

### Provider comparison

| Provider | Cost | Speed | Quality | Privacy |
|---|---|---|---|---|
| Ollama (local) | Free | Medium | Good | ✅ 100% local |
| Groq | Free tier | Fast | Great | ☁️ API call |
| OpenAI | Paid | Fast | Best | ☁️ API call |
| No summarizer | Free | Instant | None | ✅ 100% local |

---

## ✨ Features

### 🔒 Privacy First
- **100% local** — data never leaves your machine by default
- No telemetry, no analytics, no accounts, no sign-up
- All data lives in `~/.memoryos/` — fully portable
- Extension communicates **only** with `localhost:8765`
- Open source — audit every line

### 🔍 Hybrid Search Engine
- **Semantic search** via ChromaDB + sentence-transformers (384-dim cosine)
- **Keyword search** via SQLite FTS5 full-text index
- **Re-ranking**: `0.7 × semantic + 0.3 × keyword × importance × recency × pin_boost`
- Filter by source, tags, date range

### 🤖 Flexible AI Providers
- **Embeddings**: Local `all-MiniLM-L6-v2` (no API key needed) or OpenAI
- **Summarization**: Ollama (local) → Groq → OpenAI (auto-fallback chain)
- **Entity extraction**: regex-based (people, projects, tech, decisions, TODOs)
- **Importance scoring**: automatic signal detection (decisions, bugs, deploys)

### 🌐 Browser Extension (MV3)
- Chrome, Edge, Brave support
- Per-site content scripts (ChatGPT, Claude, Gemini)
- Smart deduplication via content hashing
- Batch queue with 2s debounce window
- Popup with live search + server status

### 📊 Dashboard (Next.js 14)
- Real-time memory grid with source color-coding
- Semantic search bar
- Stats widget (total, pinned, storage, sources)
- Session timeline
- Export to JSON / Markdown / CSV / Obsidian
- Dark theme, responsive

### 🔁 Memory Lifecycle
- **Pin** important memories (never auto-forgotten)
- **Forget** (soft delete — vector removed from Chroma)
- **Data retention** — auto-forget old memories after N days
- **Access tracking** — count and timestamp every retrieval
- **Background summarization** — async, non-blocking

---

## 🛠 Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Backend | Python 3.11, FastAPI | Async, fast, auto-docs |
| ORM | SQLAlchemy 2 (async) | Type-safe, async-native |
| Database | SQLite + FTS5 | Zero-config, portable |
| Vector DB | ChromaDB | Local-first, persistent |
| Embeddings | sentence-transformers | Runs offline, 384-dim |
| Summarization | Ollama / Groq / OpenAI | Fallback chain |
| Frontend | Next.js 14, TypeScript | SSR + ISR |
| Styling | Tailwind CSS | Utility-first |
| State | TanStack React Query | Cache + revalidation |
| Animation | Framer Motion | Smooth UX |
| Extension | TypeScript, MV3 | Modern, secure |
| CLI | Click | Pythonic, composable |
| CI/CD | GitHub Actions | Lint + test + publish |

---

## 🏗 Architecture

```
┌────────────────────────────────────────────────────────────┐
│                        Your Machine                        │
│                                                            │
│  ┌──────────────┐    ┌────────────────────────────────┐  │
│  │   Browser    │    │     MemoryOS Backend :8765     │  │
│  │  Extension   │───▶│  FastAPI + SQLAlchemy (async)  │  │
│  │  (MV3, TS)   │    │  ├── SQLite + FTS5             │  │
│  └──────────────┘    │  ├── ChromaDB (cosine vectors) │  │
│                       │  ├── sentence-transformers    │  │
│  ┌──────────────┐    │  └── Ollama / Groq / OpenAI   │  │
│  │  Dashboard   │───▶│                               │  │
│  │  Next.js 14  │    └────────────────────────────────┘  │
│  │  :3000       │                                         │
│  └──────────────┘    ┌────────────────┐                  │
│                       │ ~/.memoryos/   │                  │
│  ┌──────────────┐    │  memories.db   │                  │
│  │  CLI         │───▶│  chroma/       │                  │
│  │  memoryos    │    │  models/       │                  │
│  └──────────────┘    └────────────────┘                  │
└────────────────────────────────────────────────────────────┘
```

Full architecture docs: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 🐳 Docker

```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop
docker-compose down

# With Ollama for local summarization
docker-compose --profile ollama up -d
```

Data persists in `./data/` volume.

---

## 🗺 Roadmap

### v1.1
- [ ] Firefox extension (WebExtensions API)
- [ ] Cursor IDE integration — LSP plugin
- [ ] Import from ChatGPT data export (conversations.json)
- [ ] Memory merge & deduplication

### v1.2
- [ ] Obsidian vault sync (bidirectional)
- [ ] Memory graph visualization (D3.js)
- [ ] SQLCipher at-rest encryption
- [ ] Webhook notifications

### v2.0
- [ ] Mobile companion app (React Native)
- [ ] Memory streaks & gamification
- [ ] Multi-user / team memory sharing
- [ ] MCP server (Model Context Protocol)
- [ ] VS Code extension

---

## 🤝 Contributing

Contributions are what make open source amazing. Every PR, issue, and ⭐ is appreciated.

```bash
# Fork + clone
git clone https://github.com/YOUR_USERNAME/memoryos
cd memoryos

# Backend setup
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'

# Run tests
pytest tests/ -v

# Frontend setup
cd ../frontend
npm install && npm run dev

# Extension setup
cd ../extension
npm install && npm run build
```

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a PR.

---

## 🔐 Security

- The API binds to `127.0.0.1` by default (not `0.0.0.0`)
- CORS is restricted to `localhost` and `chrome-extension://`
- No authentication required locally (single-user design)
- **Do not expose port 8765 to the internet**
- For network access, use an SSH tunnel or VPN

Found a vulnerability? Please email [ossama@samotech.dev](mailto:ossama@samotech.dev) before opening a public issue.

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for full text.

Copyright © 2026 [Ossama Hashim](https://github.com/SamoTech)

---

## 💖 Support

If MemoryOS saves you time, consider supporting:

[![Sponsor on GitHub](https://img.shields.io/badge/Sponsor%20on-GitHub-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/SamoTech)
[![Ko-fi](https://img.shields.io/badge/Buy%20me%20a%20coffee-Ko--fi-ff5e5b?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/samotech)

---

<div align="center">

*"The palest ink is better than the best memory."*

**⭐ Star this repo if MemoryOS helps you!**

[![Star History](https://img.shields.io/github/stars/SamoTech/memoryos?style=social)](https://github.com/SamoTech/memoryos/stargazers)

</div>
