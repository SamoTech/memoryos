# MemoryOS Architecture

## Overview

MemoryOS is a **local-first** AI memory layer. All data stays on your machine.

```
┌─────────────────────────────────────────────────────────┐
│                    Your Machine                          │
│                                                          │
│  ┌──────────────┐    ┌───────────────────────────────┐  │
│  │   Browser    │    │      MemoryOS Backend           │  │
│  │  Extension   │───▶│  FastAPI  :8765                │  │
│  │  (MV3, TS)   │    │  ├── SQLite (memories.db)      │  │
│  └──────────────┘    │  ├── ChromaDB (vectors)        │  │
│                       │  ├── sentence-transformers     │  │
│  ┌──────────────┐    │  └── Ollama / Groq / OpenAI   │  │
│  │  Dashboard   │───▶│                               │  │
│  │  Next.js 14  │    └───────────────────────────────┘  │
│  │  :3000       │                                        │
│  └──────────────┘    ┌───────────────┐                  │
│                       │  ~/.memoryos/ │                  │
│  ┌──────────────┐    │  memories.db  │                  │
│  │  CLI         │───▶│  chroma/      │                  │
│  │  memoryos    │    │  models/      │                  │
│  └──────────────┘    └───────────────┘                  │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

1. **Capture**: Extension MutationObserver detects new AI messages
2. **Batch**: Background SW queues + batches (2s window)
3. **Ingest**: POST /api/v1/memories/bulk → MemoryService.add()
4. **Embed**: sentence-transformers all-MiniLM-L6-v2 (local, 384-dim)
5. **Store**: SQLite (structured) + ChromaDB (vectors)
6. **Index**: FTS5 virtual table for keyword search
7. **Summarize**: Background task → Ollama → Groq → OpenAI
8. **Retrieve**: Hybrid search (70% semantic + 30% keyword) with re-ranking

## Privacy

- Zero external calls by default
- Extension only communicates with `localhost:8765`
- CORS restricted to `chrome-extension://` and `localhost`
- No telemetry, no analytics
