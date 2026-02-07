#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"

echo "Stopping craig-bot service (if running)"
sudo systemctl stop craig-bot || true
sudo systemctl disable craig-bot || true

echo "Removing systemd service file"
sudo rm -f /etc/systemd/system/craig-bot.service || true

echo "Removing management scripts"
sudo rm -f /usr/local/bin/craig-start /usr/local/bin/craig-stop /usr/local/bin/craig-restart /usr/local/bin/craig-status /usr/local/bin/craig-log || true

echo "Reloading systemd daemon"
sudo systemctl daemon-reload

read -p "Remove bot files and venv in $HERE as well? [y/N] " -r RESP
if [[ "$RESP" =~ ^[Yy]$ ]]; then
  sudo rm -rf "$HERE"
  echo "Removed $HERE and virtual environment"
fi

echo "Uninstall complete."
