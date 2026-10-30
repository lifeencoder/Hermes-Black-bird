#!/usr/bin/env bash
set -e

# ==============================================================================
# Hermes Black Bird - Marimo App Launcher
# ==============================================================================

NOTEBOOK_FILE="notebook.py"
PORT="${1:-2718}"

echo "Starting Marimo Application on port $PORT..."
marimo edit "$NOTEBOOK_FILE" --host 0.0.0.0 --port "$PORT" --no-token
