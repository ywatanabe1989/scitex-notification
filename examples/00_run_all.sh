#!/bin/bash
# Timestamp: "2026-03-16 (ywatanabe)"
# File: ./examples/00_run_all.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "=== Running all scitex-notification examples ==="
for script in "$SCRIPT_DIR"/[0-9][0-9]_*.py; do
    echo "--- Running $(basename "$script") ---"
    python "$script" || echo "WARN: $(basename "$script") failed (may need backend configured)"
done
echo "=== Done ==="

# EOF
