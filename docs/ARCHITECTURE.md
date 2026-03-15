# MemoryOS Architecture

## Overview

MemoryOS is a **local-first** AI memory layer. All data stays on your machine.

```
┌──────────────────────────────────────────────────────────────┐
│                        Your Machine                          │
│                                                              │
│  ┌──────────────┐    ┌──────────────────────────────────┐  │
│  │   Browser    │    │     MemoryOS Backend :8765       │  │
│  │  Extension   │───▶│  FastAPI + SQLAlchemy (async)    │  │
│  │  (MV3, TS)   │    │  ├── SQLite + FTS5               │  │
│  └──────────────┘    │  ├── ChromaDB (cosine vectors)   │  │
│                       │  ├── sentence-transformers      │  │
│  ┌──────────────┐    │  └── Ollama / Groq / OpenAI     │  │
│  │  Dashboard   │───▶│                                  │  │
│  │  Next.js 14  │    └──────────────────────────────────┘  │
│  │  :3000       │                                           │
│  └──────────────┘    ┌────────────────────┐               │
│                       │  ~/.memoryos/      │               │
│  ┌──────────────┐    │  memories.db       │               │
│  │  CLI         │───▶│  chroma/           │               │
│  │  memoryos    │    │  models/           │               │
│  └──────────────┘    └────────────────────┘               │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow

### Ingestion Pipeline

```
Extension detects new AI message
        │
        ▼
Content hash deduplication
        │
        ▼
Background SW batches (2s window)
        │
        ▼
POST /api/v1/memories/bulk
        │
        ▼
MemoryService.add()
   ├── Generate UUID
   ├── EmbeddingService.embed(content)        → all-MiniLM-L6-v2
   ├── ChromaDB.add(id, embedding, metadata)
   ├── Summarizer.score_importance(content)
   ├── Summarizer.extract_entities(content)
   ├── SQLite INSERT (memories table)
   ├── SQLite INSERT (memories_fts FTS5)
   └── asyncio.create_task(background_summarize)   [if len > 500]
```

### Retrieval Pipeline

```
Query: "what auth approach did I use?"
        │
        ▼
┌───────────────────────────────────┐
│         Hybrid Search             │
│                                   │
│  Semantic branch:                 │
│  query → embed → ChromaDB.query() │
│  → top 20 by cosine similarity    │
│                                   │
│  Keyword branch:                  │
│  query → FTS5 MATCH → top 20     │
│                                   │
│  Merge + re-rank:                 │
│  score = 0.7×semantic             │
│        + 0.3×keyword              │
│        × importance_score         │
│        × recency_factor           │
│        × pin_boost (1.5× pinned)  │
└───────────────────────────────────┘
        │
        ▼
Top 10 results returned
        │
        ▼
get_context() → formatted string → paste into AI
```

## Database Schema

### `memories` table

| Column | Type | Description |
|---|---|---|
| id | TEXT (UUID) | Primary key |
| content | TEXT | Full conversation text |
| summary | TEXT | AI-generated 1-2 sentence summary |
| embedding_id | TEXT | ChromaDB vector ID |
| source | ENUM | chatgpt / claude / gemini / cursor / manual / api / cli |
| session_id | TEXT (FK) | Parent session |
| entities | JSON | Extracted entities |
| importance_score | FLOAT | 0.0 – 1.0 |
| is_pinned | BOOL | Never auto-forgotten if true |
| is_forgotten | BOOL | Soft delete |
| created_at | DATETIME | Creation timestamp |
| accessed_at | DATETIME | Last access timestamp |
| access_count | INT | Number of retrievals |

### `memories_fts` (virtual FTS5)

| Column | Description |
|---|---|
| content | Indexed full text |
| summary | Indexed summary |
| id | Unindexed reference |

### `sessions` table

| Column | Type | Description |
|---|---|---|
| id | TEXT (UUID) | Primary key |
| source | TEXT | AI tool name |
| title | TEXT | Auto or manual title |
| summary | TEXT | Session summary |
| memory_count | INT | Number of memories |
| started_at | DATETIME | Session start |
| ended_at | DATETIME | Session end |
| url | TEXT | Source page URL |

## Vector Store

- **Engine**: ChromaDB `PersistentClient`
- **Collection**: `memories` (cosine similarity space)
- **Dimensions**: 384 (all-MiniLM-L6-v2)
- **Metadata filters**: `source`, `is_forgotten`
- **Storage**: `~/.memoryos/chroma/`

## Embedding Model

| Property | Value |
|---|---|
| Model | `all-MiniLM-L6-v2` |
| Dimensions | 384 |
| Max sequence | 256 tokens |
| Size on disk | ~90 MB |
| Speed | ~50ms/query (CPU) |
| Requires internet | First download only |

## Privacy

- Zero external calls by default
- Extension only communicates with `localhost:8765`
- CORS restricted to `chrome-extension://` and `localhost`
- No telemetry, no analytics
- See [PRIVACY.md](PRIVACY.md)
