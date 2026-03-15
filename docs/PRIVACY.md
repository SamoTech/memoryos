# MemoryOS Privacy Policy

**TL;DR: MemoryOS is 100% local by default. Your data never leaves your machine.**

---

## What MemoryOS Stores (All Local)

| File | Contents | Location |
|---|---|---|
| `memories.db` | All memory records, sessions, tags | `~/.memoryos/` |
| `chroma/` | Vector embeddings (numbers, not text) | `~/.memoryos/` |
| `models/all-MiniLM-L6-v2/` | Embedding model weights | `~/.memoryos/` |
| `server.pid` | Server process ID | `~/.memoryos/` |
| `.env` | Your configuration | `~/.memoryos/` |

---

## What Is NEVER Sent Externally (By Default)

- ✅ Your chat content
- ✅ Your memory data
- ✅ Your usage patterns
- ✅ Any analytics or telemetry
- ✅ Your API keys (stored only in `~/.memoryos/.env`)

---

## Optional External Calls (Only If YOU Configure Them)

| Service | When Called | What's Sent | How to Disable |
|---|---|---|---|
| **Ollama** | Summarization | Memory content | Runs locally — no network | 
| **Groq API** | Summarization fallback | Memory content (truncated to 2000 chars) | Remove `GROQ_API_KEY` from `.env` |
| **OpenAI API** | Summarization fallback | Memory content (truncated to 2000 chars) | Remove `OPENAI_API_KEY` from `.env` |
| **OpenAI Embeddings** | If `EMBEDDING_PROVIDER=openai` | Memory content | Set `EMBEDDING_PROVIDER=local` |
| **PyPI** | Install only | Package metadata | One-time only |
| **HuggingFace** | First run only | Nothing (downloads model) | Pre-download model |

---

## Browser Extension

The extension:
- **Only** communicates with `http://localhost:8765`
- **Never** sends data to any external server
- **Never** reads page content outside of the whitelisted AI sites
- **Only** captures conversation turns (user + assistant messages)
- Uses content hashing to avoid sending duplicates

---

## Data Deletion

```bash
# Forget a specific memory
memoryos forget <id>

# Delete ALL data
rm -rf ~/.memoryos/
```

That's it. No servers to contact, no account to delete.

---

## GDPR / Data Rights

Since all data is local and you control it entirely:
- **Right to access**: `memoryos export --format json`
- **Right to erasure**: `rm -rf ~/.memoryos/`
- **Right to portability**: `memoryos export --format json` or `--format markdown`
- **Data controller**: You.
