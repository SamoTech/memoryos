# Installation Guide

## Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| Python | 3.11 | 3.12 |
| RAM | 512 MB | 2 GB |
| Disk | 500 MB | 2 GB |
| OS | Linux, macOS, Windows (WSL2) | Ubuntu 22.04 / macOS 13+ |

---

## Method 1: One-liner (Linux / macOS)

```bash
curl -fsSL https://raw.githubusercontent.com/SamoTech/memoryos/main/scripts/install.sh | bash
```

This script:
1. Checks Python 3.11+
2. Installs `memoryos` via pip
3. Optionally installs Ollama + pulls `llama3`
4. Starts the server
5. Opens the dashboard in your browser

---

## Method 2: pip

```bash
pip install memoryos
memoryos start
```

---

## Method 3: Docker

```bash
git clone https://github.com/SamoTech/memoryos
cd memoryos
docker-compose up -d
```

Data is persisted in `./data/` (Docker volume).

---

## Method 4: Development Install

```bash
git clone https://github.com/SamoTech/memoryos
cd memoryos/backend
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
memoryos start

# Frontend (separate terminal)
cd ../frontend
npm install && npm run dev
```

---

## Browser Extension

1. Build: `bash scripts/build-extension.sh`
2. Open `chrome://extensions/` → Enable *Developer mode*
3. *Load unpacked* → select `extension/dist/`
4. The 🧠 icon appears in your toolbar
5. Start a conversation on ChatGPT, Claude, or Gemini — memories are captured automatically

---

## Local AI (Optional but recommended)

For privacy-first summarization, install Ollama:

```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3
```

Set in `~/.memoryos/.env`:
```env
SUMMARIZER_PROVIDER=ollama
OLLAMA_MODEL=llama3
```

---

## Verify Installation

```bash
# Check health
curl http://localhost:8765/health

# Check stats
memoryos stats

# Add a test memory
memoryos add "Test: MemoryOS is working!"

# Search it
memoryos search "test memoryos"
```

---

## Upgrading

```bash
pip install --upgrade memoryos
memoryos stop && memoryos start
```

Database migrations run automatically on start.

---

## Uninstall

```bash
pip uninstall memoryos
rm -rf ~/.memoryos   # Removes all data
```
