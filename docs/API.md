# MemoryOS API Reference

Base URL: `http://localhost:8765`

## Health

```
GET /health
```

## Memories

```
GET    /api/v1/memories              List memories
POST   /api/v1/memories              Add memory
POST   /api/v1/memories/bulk         Bulk add (used by extension)
GET    /api/v1/memories/{id}         Get memory
PUT    /api/v1/memories/{id}         Update memory
DELETE /api/v1/memories/{id}         Forget memory (soft delete)
POST   /api/v1/memories/{id}/pin     Pin/unpin toggle
```

## Search

```
GET  /api/v1/search?q=...            Hybrid semantic+keyword search
POST /api/v1/search/similar          Find similar to text
GET  /api/v1/search/context?q=...   Get prompt-ready context string
```

## Sessions

```
GET  /api/v1/sessions               List sessions
POST /api/v1/sessions               Create session
GET  /api/v1/sessions/{id}          Session detail + memories
GET  /api/v1/sessions/{id}/summary  AI-generated summary
```

## Export

```
GET /api/v1/export?format=json|markdown|csv|obsidian
```

## Stats

```
GET /api/v1/stats
```
