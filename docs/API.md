# MemoryOS API Reference

Base URL: `http://localhost:8765`

Interactive docs: `http://localhost:8765/docs` (Swagger UI)

---

## Authentication

No authentication required. The API binds to `127.0.0.1` and is only accessible locally.

---

## Health

### `GET /health`

Returns server status and configuration.

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "database": "ok",
  "data_dir": "/home/user/.memoryos",
  "embedding_provider": "local",
  "summarizer_provider": "ollama"
}
```

---

## Memories

### `GET /api/v1/memories`

List memories with optional filtering.

**Query params:**
| Param | Type | Default | Description |
|---|---|---|---|
| `skip` | int | 0 | Pagination offset |
| `limit` | int | 50 | Max results (≤200) |
| `source` | string | — | Filter by source |
| `pinned` | bool | false | Pinned only |

**Response:** `Memory[]`

---

### `POST /api/v1/memories`

Add a memory.

**Body:**
```json
{
  "content": "Decided to use PostgreSQL over MySQL",
  "source": "manual",
  "session_id": null,
  "tags": ["database", "architecture"],
  "metadata": {}
}
```

**Response:** `Memory` (201)

---

### `POST /api/v1/memories/bulk`

Bulk add memories (used by browser extension).

**Body:** `Memory[]`

**Response:** `Memory[]` (201)

---

### `GET /api/v1/memories/{id}`

Get a specific memory. Increments `access_count`.

---

### `PUT /api/v1/memories/{id}`

Update a memory.

**Body:**
```json
{
  "content": "Updated content",
  "summary": "Updated summary",
  "tags": ["new-tag"],
  "is_pinned": true,
  "importance_score": 0.9
}
```

---

### `DELETE /api/v1/memories/{id}`

Soft-delete (forget) a memory. Removes from ChromaDB vectors.

**Response:** `{ "ok": true, "id": "..." }`

---

### `POST /api/v1/memories/{id}/pin`

Toggle pin status.

---

## Search

### `GET /api/v1/search`

Hybrid semantic + keyword search.

**Query params:**
| Param | Type | Description |
|---|---|---|
| `q` | string | Search query (required) |
| `limit` | int | Max results (default 10, max 50) |
| `source` | string | Filter by source |
| `tags` | string | Comma-separated tag names |

**Response:**
```json
[
  {
    "memory": { ...Memory },
    "score": 0.87
  }
]
```

---

### `POST /api/v1/search/similar`

Find memories semantically similar to any text.

**Body:**
```json
{
  "text": "PostgreSQL replication strategy",
  "limit": 10,
  "source": "chatgpt"
}
```

---

### `GET /api/v1/search/context`

Get a prompt-ready context string from top memories.

**Query params:**
| Param | Default | Description |
|---|---|---|
| `q` | required | Query |
| `max_tokens` | 2000 | Approximate word limit |

**Response:**
```json
{
  "context": "[chatgpt | 2026-03-14] Decided to use PostgreSQL...\n\n[claude | 2026-03-12] ...",
  "query": "database choice"
}
```

---

## Sessions

### `GET /api/v1/sessions`
List all sessions. Params: `skip`, `limit`.

### `POST /api/v1/sessions`
```json
{ "source": "chatgpt", "title": "FastAPI discussion", "url": "https://chat.openai.com/..." }
```

### `GET /api/v1/sessions/{id}`
Session detail including all memories.

### `GET /api/v1/sessions/{id}/summary`
AI-generated session summary.

---

## Tags

### `GET /api/v1/tags`
List all tags ordered by memory count.

### `GET /api/v1/tags/{name}/memories`
List memories with a specific tag.

---

## Stats

### `GET /api/v1/stats`

**Response:**
```json
{
  "total_memories": 1247,
  "pinned_memories": 43,
  "by_source": {
    "chatgpt": 512,
    "claude": 380,
    "manual": 99
  },
  "storage_bytes": 15728640,
  "storage_mb": 15.0
}
```

---

## Export

### `GET /api/v1/export`

**Query params:**
| Param | Options | Description |
|---|---|---|
| `format` | `json` \| `markdown` \| `csv` \| `obsidian` | Export format |
| `source` | any source name | Optional filter |

Returns a downloadable file.

---

## Summarize

### `POST /api/v1/summarize`
```json
{ "text": "Long text to summarize..." }
```
**Response:** `{ "summary": "..." }`

### `POST /api/v1/summarize/pending`
Trigger background summarization for all unsummarized memories.

**Response:** `{ "updated": 12 }`

---

## Memory Object Schema

```json
{
  "id": "uuid-string",
  "content": "Full text content",
  "summary": "AI-generated summary or null",
  "source": "chatgpt | claude | gemini | cursor | manual | api | cli",
  "session_id": "uuid or null",
  "entities": {
    "people": [],
    "projects": [],
    "technologies": ["FastAPI", "PostgreSQL"],
    "decisions": ["Decided to use PostgreSQL."],
    "todos": []
  },
  "importance_score": 0.75,
  "is_pinned": false,
  "is_forgotten": false,
  "created_at": "2026-03-15T04:30:00Z",
  "accessed_at": "2026-03-15T04:32:00Z",
  "access_count": 3,
  "tags": [
    { "id": "uuid", "name": "database", "color": "#6366f1" }
  ]
}
```
