#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$HERE/.." && pwd)"
VENV="$HERE/venv"

echo "Installing Craig bot from: $PROJECT_ROOT"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found. Please install Python 3." >&2
  exit 1
fi

if [ ! -f "$PROJECT_ROOT/requirements.txt" ]; then
  echo "requirements.txt not found at $PROJECT_ROOT/requirements.txt" >&2
  exit 1
fi

echo "Creating virtual environment at $VENV"
if [ -d "$VENV" ]; then
  echo "Virtual environment already exists at $VENV; removing and recreating..."
  rm -rf "$VENV"
fi
python3 -m venv "$VENV"

echo "Installing Python dependencies into venv..."
"$VENV/bin/pip" install --upgrade -r "$PROJECT_ROOT/requirements.txt"

# Check if .env already exists
if [ -f "$PROJECT_ROOT/.env" ]; then
  echo ".env already exists at $PROJECT_ROOT/.env"
  read -p "Do you want to update the Discord token? [y/N] " -r UPDATE_TOKEN
  if [[ ! "$UPDATE_TOKEN" =~ ^[Yy]$ ]]; then
    echo "Skipping token configuration. Using existing .env."
    TOKEN=""
  fi
fi

# Only ask for token if we don't have an existing one or user wants to update
if [ -z "$TOKEN" ] && [ -f "$PROJECT_ROOT/.env" ] && [[ "$UPDATE_TOKEN" =~ ^[Yy]$ ]]; then
  read -p "Enter your Discord bot token: " -r TOKEN
elif [ -z "$TOKEN" ] && [ ! -f "$PROJECT_ROOT/.env" ]; then
  read -p "Enter your Discord bot token: " -r TOKEN
fi

if [ -f "$PROJECT_ROOT/.env" ] && [ -n "$TOKEN" ]; then
  echo ".env already exists, backing up to .env.bak"
  cp "$PROJECT_ROOT/.env" "$PROJECT_ROOT/.env.bak"
fi

if [ -n "$TOKEN" ]; then
  if [ -z "$TOKEN" ]; then
    echo "No token provided. Aborting." >&2
    exit 1
  fi

if [ -n "$TOKEN" ]; then
  echo "Writing .env with new token"
  cat > "$PROJECT_ROOT/.env" <<EOF
DISCORD_TOKEN=$TOKEN
RESPONSE_CHANCE=0.5
LOG_FILE=$PROJECT_ROOT/craig.log
COMMAND_PREFIX=!
EOF
else
  echo "Using existing .env configuration"
fi

SERVICE_PATH="/etc/systemd/system/craig-bot.service"
echo "Installing systemd service to $SERVICE_PATH"

sudo bash -c "cat > $SERVICE_PATH <<EOL
[Unit]
Description=Craig Discord Bot
After=network.target

[Service]
Type=simple
Restart=on-failure
WorkingDirectory=$HERE
ExecStart=$VENV/bin/python3 $HERE/craig-bot.py
User=$(whoami)
Group=$(id -gn)
Environment=PYTHONUNBUFFERED=1
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOL"

echo "Creating management scripts in /usr/local/bin/"
sudo tee /usr/local/bin/craig-start >/dev/null <<'EOS'
#!/usr/bin/env bash
systemctl start craig-bot
EOS
sudo tee /usr/local/bin/craig-stop >/dev/null <<'EOS'
#!/usr/bin/env bash
systemctl stop craig-bot
EOS
sudo tee /usr/local/bin/craig-restart >/dev/null <<'EOS'
#!/usr/bin/env bash
systemctl restart craig-bot
EOS
sudo tee /usr/local/bin/craig-status >/dev/null <<'EOS'
#!/usr/bin/env bash
systemctl status craig-bot --no-pager
EOS
sudo tee /usr/local/bin/craig-log >/dev/null <<'EOS'
#!/usr/bin/env bash
journalctl -u craig-bot -f
EOS

sudo chmod +x /usr/local/bin/craig-* || true

echo "Setting file permissions"
sudo chown -R $(whoami):$(id -gn) "$HERE"
sudo chmod -R 750 "$HERE"

echo "Reloading systemd daemon"
sudo systemctl daemon-reload
sudo systemctl enable --now craig-bot

echo "Installation complete. Service status:"
systemctl status craig-bot --no-pager || true

cat <<EOF

Management commands:
- craig-start   : start the bot
- craig-stop    : stop the bot
- craig-restart : restart the bot
- craig-status  : check service status
- craig-log     : follow logs

To reconfigure the token, edit .env in the project root and run 'craig-restart'.
EOF
