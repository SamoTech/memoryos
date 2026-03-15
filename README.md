# 🧠 MemoryOS

> **Your AI finally remembers you.**

[![License: MIT](https://img.shields.io/badge/License-MIT-6366f1.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green.svg)](https://fastapi.tiangolo.com)
[![Next.js 14](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org)
[![Powered by MemoryOS](https://img.shields.io/badge/Powered%20by-MemoryOS-4F46E5)](https://github.com/SamoTech/memoryos)

MemoryOS is a **local-first AI memory layer** that gives any AI assistant persistent, searchable memory across all sessions. 100% private, zero cloud, works with every LLM.

---

## The Problem

You use ChatGPT, Claude, Cursor, and Gemini every day.
But every session starts from zero.
The AI forgets your name, your projects, your preferences, your decisions.

**MemoryOS fixes that.**

---

## How It Works

```
1. CAPTURE  →  Browser extension silently captures AI conversations
2. STORE    →  Local SQLite + ChromaDB vector store (100% on your machine)
3. RETRIEVE →  Hybrid semantic+keyword search injects context into any AI
```

---

## Quick Install

```bash
curl -fsSL https://raw.githubusercontent.com/SamoTech/memoryos/main/scripts/install.sh | bash
```

Or via pip:

```bash
pip install memoryos
memoryos start
```

---

## Supported AI Tools

| Tool | Capture Method |
|------|---------------|
| ChatGPT | Browser extension |
| Claude | Browser extension |
| Gemini | Browser extension |
| Cursor | CLI file watcher (`memoryos watch`) |
| Any site | Generic DOM scraper (opt-in) |

---

## CLI Reference

```bash
memoryos start                          # Start server + open dashboard
memoryos stop                           # Stop server
memoryos search "react debounce hook"   # Semantic search
memoryos add "Decided to use Zustand"   # Add memory manually
memoryos forget <id>                    # Forget a memory
memoryos stats                          # Show statistics
memoryos export --format markdown       # Export memories
memoryos ask "what auth approach?"      # Get AI-ready context
```

---

## Features

### 🔒 Privacy First
- 100% local — data never leaves your machine
- No telemetry, no analytics, no accounts
- All data in `~/.memoryos/`

### 🔍 Hybrid Search
- Semantic search via ChromaDB + sentence-transformers
- Keyword search via SQLite FTS5
- Re-ranked by relevance × importance × recency

### 🤖 Local AI
- Embeddings: `all-MiniLM-L6-v2` (runs fully offline)
- Summarization: Ollama (local) → Groq → OpenAI (fallback)

### 🌐 Browser Extension
- Chrome, Edge, Brave (Manifest V3)
- Auto-captures ChatGPT, Claude, Gemini
- Popup with instant search

---

## Tech Stack

- **Backend**: Python 3.11, FastAPI, SQLAlchemy (async), SQLite, ChromaDB
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, React Query, Framer Motion
- **Extension**: TypeScript, Manifest V3
- **Embeddings**: sentence-transformers (local) or OpenAI
- **Summarization**: Ollama → Groq → OpenAI

---

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Privacy

See [docs/PRIVACY.md](docs/PRIVACY.md) — every file MemoryOS writes to disk, documented.

## API

See [docs/API.md](docs/API.md)

---

## Contributing

PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
git clone https://github.com/SamoTech/memoryos
cd memoryos/backend
pip install -e '.[dev]'
memoryos start
```

---

## Roadmap

- [ ] Firefox extension
- [ ] Cursor IDE integration (LSP plugin)
- [ ] Import from ChatGPT data export
- [ ] Obsidian vault sync
- [ ] Memory streaks & gamification
- [ ] SQLCipher encryption
- [ ] Mobile companion app

---

## License

MIT © [Ossama Hashim](https://github.com/SamoTech)

---

> *"The palest ink is better than the best memory."*
