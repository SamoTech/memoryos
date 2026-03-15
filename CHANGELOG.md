# Changelog

All notable changes to MemoryOS will be documented here.

Format: [Keep a Changelog](https://keepachangelog.com) | Versioning: [Semantic Versioning](https://semver.org)

---

## [Unreleased]

### Planned
- Firefox browser extension
- Cursor IDE LSP plugin
- ChatGPT data export importer
- SQLCipher at-rest encryption
- Obsidian vault bidirectional sync

---

## [1.0.0] — 2026-03-15

### Added
- 🧠 **Core memory engine** — SQLite + ChromaDB hybrid storage
- 🔍 **Hybrid search** — semantic (cosine) + keyword (FTS5) + re-ranking
- 🤖 **Local embeddings** — `all-MiniLM-L6-v2` via sentence-transformers
- ✍️ **Auto-summarization** — Ollama → Groq → OpenAI fallback chain
- 📊 **Entity extraction** — people, projects, tech, decisions, TODOs
- 🏷️ **Importance scoring** — automatic signal detection
- 📌 **Pin/forget** — memory lifecycle management
- 🔁 **Data retention** — configurable auto-forget policy
- 🌐 **Browser Extension** — MV3, ChatGPT + Claude + Gemini support
- 💻 **CLI** — `start`, `stop`, `search`, `add`, `forget`, `stats`, `export`, `ask`
- 📊 **Dashboard** — Next.js 14, dark theme, semantic search, stats, export
- 🔌 **REST API** — full CRUD + search + export + sessions + tags
- 🐳 **Docker** — single `docker-compose up` deployment
- 🚀 **GitHub Actions** — CI (lint + test + build) + PyPI auto-release
- 📖 **Full documentation** — API, Architecture, Privacy, Contributing

---

[Unreleased]: https://github.com/SamoTech/memoryos/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/SamoTech/memoryos/releases/tag/v1.0.0
