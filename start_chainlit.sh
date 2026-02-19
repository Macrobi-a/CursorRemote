#!/bin/sh
# Startup script for Chainlit on Railway - ensures proper startup and error handling

set -e

echo "Starting Chainlit app..."

# Use Railway's PORT or default to 8000
PORT=${PORT:-8000}
echo "Using port: $PORT"

# Start Chainlit with explicit host binding
exec chainlit run app.py --host 0.0.0.0 --port "$PORT"
