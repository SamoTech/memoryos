#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../extension"
npm install
npm run build
echo "✓ Extension built in extension/dist/"
echo "  Load in Chrome: Settings → Extensions → Load unpacked → select extension/dist/"
