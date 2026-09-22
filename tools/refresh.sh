#!/usr/bin/env bash
# Refresh the library end to end. Use this rather than calling harvest directly:
# a bare harvest re-downloads the photographic scans (the English Criminal
# Procedure Code is 102 MB) and they will go straight out to the server.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/harvest.py "$@"
python3 tools/compress.py 4000000
python3 tools/prune_oversize.py 12
python3 tools/build.py
echo
echo "  ready to deploy:  $(du -sh legislation | cut -f1)"
