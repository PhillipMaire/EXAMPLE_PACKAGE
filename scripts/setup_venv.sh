#!/bin/bash
set -e

echo "=== Persistent Python 3.12 venv setup ==="

# Make sure we're inside /workspace (persistent storage)
cd /workspace

# Ensure Python 3.12 exists
if ! command -v python3.12 &> /dev/null; then
  echo "Python 3.12 not found, installing..."
  sudo apt update
  sudo apt install -y python3.12 python3.12-venv python3.12-distutils
fi

# Create venv if missing
if [ ! -d "/workspace/venv" ]; then
  echo "Creating virtual environment at /workspace/venv ..."
  python3.12 -m venv /workspace/venv
fi

# Activate it for the current session
source /workspace/venv/bin/activate

# Upgrade pip and wheel
pip install --upgrade pip wheel

# Auto-load on future sessions
if ! grep -q 'source /workspace/venv/bin/activate' "$HOME/.bashrc" 2>/dev/null; then
  echo 'source /workspace/venv/bin/activate' >> "$HOME/.bashrc"
  echo "Added auto-activation to ~/.bashrc"
fi

echo "✅ Virtual environment ready!"
echo "Next time you open a shell, it will auto-activate."
echo "If not, you can activate manually with:"
echo "    source /workspace/venv/bin/activate"
