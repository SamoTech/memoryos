# MemoryOS Privacy Policy

MemoryOS is 100% local. Here is every file it writes to disk:

| File | Contents | Purpose |
|------|----------|---------|
| `~/.memoryos/memories.db` | All memory records, sessions, tags | Primary database |
| `~/.memoryos/chroma/` | Vector embeddings | Semantic search |
| `~/.memoryos/models/all-MiniLM-L6-v2/` | Embedding model weights | Local embeddings |
| `~/.memoryos/server.pid` | Server process ID | Lifecycle management |
| `~/.memoryos/.env` | Your configuration | Settings |

## What is NEVER sent externally

- Your chat content
- Your memories
- Your usage patterns
- Any telemetry or analytics

## Optional external calls (only if YOU configure them)

- **Groq API** — only if `GROQ_API_KEY` is set, only for summarization
- **OpenAI API** — only if `OPENAI_API_KEY` is set, only for summarization/embeddings
- **Ollama** — runs locally at `localhost:11434`

## Browser Extension

The extension communicates **only** with `http://localhost:8765`. It never sends data to any external server.
