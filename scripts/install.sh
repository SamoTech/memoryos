#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'; NC='\033[0m'

echo -e "${CYAN}\n🧠 Installing MemoryOS...${NC}\n"

# Check Python 3.11+
if ! command -v python3 &>/dev/null; then
  echo -e "${RED}✗ Python 3 not found. Please install Python 3.11+${NC}"
  exit 1
fi

python3 - <<'PY'
import sys
if sys.version_info < (3, 11):
    print(f"Python 3.11+ required, found {sys.version}")
    sys.exit(1)
PY

echo -e "${GREEN}✓ Python version OK${NC}"

# Install memoryos
echo -e "Installing memoryos via pip..."
pip install --upgrade pip -q
pip install memoryos -q
echo -e "${GREEN}✓ memoryos installed${NC}"

# Optional: Ollama
read -rp "$(echo -e "${YELLOW}Install Ollama for local AI summarization? [Y/n]: ${NC}")" yn
yn=${yn:-Y}
if [[ "$yn" =~ ^[Yy]$ ]]; then
  if ! command -v ollama &>/dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
    echo -e "${GREEN}✓ Ollama installed${NC}"
  else
    echo -e "${GREEN}✓ Ollama already installed${NC}"
  fi
  echo "Pulling llama3 model (this may take a few minutes)..."
  ollama pull llama3 || echo -e "${YELLOW}⚠ Could not pull llama3 automatically. Run: ollama pull llama3${NC}"
fi

# Start server
echo -e "\nStarting MemoryOS..."
memoryos start --no-browser &
sleep 3

# Open browser
if command -v xdg-open &>/dev/null; then
  xdg-open http://localhost:3000 &>/dev/null &
elif command -v open &>/dev/null; then
  open http://localhost:3000
fi

echo -e "\n${GREEN}${BOLD}✓ MemoryOS is running!${NC}"
echo -e "  Dashboard: ${CYAN}http://localhost:3000${NC}"
echo -e "  API:       ${CYAN}http://localhost:8765${NC}"
echo -e "\n${YELLOW}📦 Install the browser extension to start capturing AI conversations.${NC}\n"
