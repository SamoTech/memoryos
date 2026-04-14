<div align="center">

<img src="https://img.shields.io/badge/-%F0%9F%A7%A0%20MemoryOS-6366f1?style=for-the-badge&logoColor=white" alt="MemoryOS" height="40" />

# 🧠 MemoryOS

![Banner](docs/assets/banner.svg)

### *Your AI finally remembers you.*

> Local-first AI memory layer. 100% private. Zero cloud. Works with every LLM.

---

[![License: MIT](https://img.shields.io/badge/License-MIT-6366f1.svg?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776ab.svg?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-000000.svg?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4-3178c6.svg?style=flat-square&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![CI](https://img.shields.io/github/actions/workflow/status/SamoTech/memoryos/ci.yml?branch=main&style=flat-square&label=CI&logo=github)](https://github.com/SamoTech/memoryos/actions)
[![Release](https://img.shields.io/github/v/release/SamoTech/memoryos?style=flat-square&color=22c55e&logo=github)](https://github.com/SamoTech/memoryos/releases)
[![Stars](https://img.shields.io/github/stars/SamoTech/memoryos?style=flat-square&logo=github&color=f59e0b)](https://github.com/SamoTech/memoryos/stargazers)
[![Forks](https://img.shields.io/github/forks/SamoTech/memoryos?style=flat-square&logo=github&color=6366f1)](https://github.com/SamoTech/memoryos/network/members)
[![Issues](https://img.shields.io/github/issues/SamoTech/memoryos?style=flat-square&logo=github&color=ef4444)](https://github.com/SamoTech/memoryos/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/SamoTech/memoryos/pulls)
[![SQLite](https://img.shields.io/badge/SQLite-FTS5-003b57.svg?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-ff6b35.svg?style=flat-square)](https://trychroma.com)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20AI-000000.svg?style=flat-square)](https://ollama.ai)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ed.svg?style=flat-square&logo=docker&logoColor=white)](docker-compose.yml)
[![Made in Egypt](https://img.shields.io/badge/Made%20in-%F0%9F%87%AA%F0%9F%87%AC%20Egypt-cc0000.svg?style=flat-square)](https://github.com/SamoTech)

</div>

---

## 😐 The Problem

You use ChatGPT, Claude, Cursor, and Gemini **every single day**. But every new session starts from **absolute zero**.

**This is the AI amnesia problem. MemoryOS fixes it.**

---

## ✨ How It Works

```
1. CAPTURE   →   Extension watches your AI chats (ChatGPT, Claude, Gemini)
2. STORE     →   Local SQLite + ChromaDB — 100% on your machine
3. RETRIEVE  →   Hybrid search: semantic + keyword, injected into any AI chat
```

---

## ⚡ Quick Install

```bash
# One-line (Linux / macOS)
curl -fsSL https://raw.githubusercontent.com/SamoTech/memoryos/main/scripts/install.sh | bash

# Via pip
pip install memoryos && memoryos start

# Via Docker
git clone https://github.com/SamoTech/memoryos && cd memoryos && docker-compose up -d
```

---

## 💻 CLI Reference

```bash
memoryos start                          # Start server + open dashboard
memoryos add "Decided to use Zustand"   # Add memory manually
memoryos search "react hooks"           # Semantic search
memoryos ask "what auth approach did I use?"  # Get AI-ready context
memoryos export --format markdown       # Export to Markdown
```

---

## ⚙️ Configuration

Edit `~/.memoryos/.env`:

```env
EMBEDDING_PROVIDER=local
SUMMARIZER_PROVIDER=ollama
OLLAMA_MODEL=llama3
AUTO_SUMMARIZE=true
```

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI |
| Database | SQLite + FTS5 |
| Vector DB | ChromaDB |
| Embeddings | sentence-transformers |
| Summarization | Ollama / Groq / OpenAI |
| Dashboard | Next.js 14 + TypeScript |
| Extension | Chrome MV3 |

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built with ❤️ by [SamoTech](https://github.com/SamoTech) · *Local-first AI memory*

</div>
