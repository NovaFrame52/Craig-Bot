#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$HERE/.." && pwd)"
VENV="$HERE/venv"
REPO_URL="https://github.com/NovaFrame52/Craig-Bot.git"

FORCE=0

while [ $# -gt 0 ]; do
  case "$1" in
    -f|--force) FORCE=1; shift ;;
    -h|--help) echo "Usage: $0 [-f|--force] [-h|--help]"; exit 0 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

echo "Updating Craig bot from: $PROJECT_ROOT"

# Check if git is installed
if ! command -v git >/dev/null 2>&1; then
  echo "git not found. Please install git." >&2
  exit 1
fi

# Check if we're in a git repo
if [ ! -d "$PROJECT_ROOT/.git" ]; then
  echo "Initializing git repository..."
  cd "$PROJECT_ROOT"
  git init
  git remote add origin "$REPO_URL"
fi

# Check if the remote URL is correct
CURRENT_REMOTE=$(git -C "$PROJECT_ROOT" config --get remote.origin.url 2>/dev/null || echo "")
if [ "$CURRENT_REMOTE" != "$REPO_URL" ]; then
  echo "Updating git remote URL to $REPO_URL"
  git -C "$PROJECT_ROOT" remote set-url origin "$REPO_URL"
fi

echo "Fetching latest changes from GitHub..."
git -C "$PROJECT_ROOT" fetch origin main

# Check if there are any updates
LOCAL=$(git -C "$PROJECT_ROOT" rev-parse HEAD 2>/dev/null || echo "")
REMOTE=$(git -C "$PROJECT_ROOT" rev-parse origin/main 2>/dev/null || echo "")

if [ -z "$LOCAL" ] || [ -z "$REMOTE" ]; then
  echo "Unable to determine git revision; attempting to reset to origin/main..."
  git -C "$PROJECT_ROOT" reset --hard origin/main
elif [ "$LOCAL" = "$REMOTE" ]; then
  echo "already up to date."
else
  echo "Updates available. Pulling from GitHub..."
  git -C "$PROJECT_ROOT" pull origin main
fi

# Check if requirements.txt changed
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
  if [ -d "$VENV" ]; then
    echo "Checking dependencies..."
    # Create a temp requirements file with current installed packages
    TEMP_REQS=$(mktemp)
    "$VENV/bin/pip" freeze > "$TEMP_REQS" || true
    
    # Simple check: if the number of lines differs significantly, reinstall
    NEW_REQS_COUNT=$(wc -l < "$PROJECT_ROOT/requirements.txt")
    INSTALLED_REQS_COUNT=$(wc -l < "$TEMP_REQS" || echo "0")
    
    if [ "$INSTALLED_REQS_COUNT" -lt "$NEW_REQS_COUNT" ] || [ "$NEW_REQS_COUNT" -eq 0 ]; then
      echo "Updating Python dependencies..."
      "$VENV/bin/pip" install --upgrade -r "$PROJECT_ROOT/requirements.txt"
    else
      echo "Dependencies appear up to date."
    fi
    
    rm -f "$TEMP_REQS"
  else
    echo "Warning: Virtual environment not found at $VENV"
    echo "Run the install script to set up the environment."
  fi
fi

# Restart the service
if systemctl is-active --quiet craig-bot; then
  if [ "$FORCE" -eq 1 ]; then
    echo "Restarting craig-bot service..."
    sudo systemctl restart craig-bot
    echo "Service restarted."
  else
    echo ""
    read -p "Restart craig-bot service now? [y/N] " -r RESTART_SERVICE
    if [[ "$RESTART_SERVICE" =~ ^[Yy]$ ]]; then
      echo "Restarting craig-bot service..."
      sudo systemctl restart craig-bot
      echo "Service restarted."
    else
      echo "Service not restarted. Run 'sudo systemctl restart craig-bot' when ready."
    fi
  fi
else
  echo "Note: craig-bot service is not currently running."
fi

echo ""
echo "Update complete."
