# Craig — Disappointed Dad Discord Bot

Craig responds like a disappointed, divorced father — purely for entertainment.

Features
- Responds to 50+ trigger phrases (case-insensitive) with ~50% chance
- Always responds to direct mentions (e.g., "Hey Craig" or @Craig)
- Slash commands: `/dadjoke`, `/roast`, `/wisdom`, `/sigh`
- Uses a large bank of varied disappointed-dad responses
- Runs as a systemd service and logs to the journal and a log file
- Installs into an isolated Python virtual environment for easy cleanup

Quick install

1. Make the script executable and run it:

    chmod +x install.sh
    sudo ./install.sh

The installer will:
- Create an isolated Python virtual environment in the installation directory
- Install dependencies into the venv
- Prompt for your Discord bot token
- Set up a systemd service

This isolates Craig from your system Python, making uninstall clean and easy.

Management commands (installed to /usr/local/bin)

- craig-start   : start the bot
- craig-stop    : stop the bot
- craig-restart : restart the bot
- craig-status  : check service status
- craig-log     : follow logs (journalctl -u craig-bot -f)

Slash Commands

Craig responds to these slash commands in Discord:

- `/dadjoke` - Get a random disappointed dad response
- `/roast [target]` - Get roasted by Craig (optionally roast someone/something else)
- `/wisdom` - Craig shares a disappointed life lesson
- `/sigh` - Craig sighs in disappointment

Uninstall

Run the provided `uninstall.sh` to stop and remove the service and helper scripts. It will also offer to remove the bot files.

Configuration

Edit the `.env` file in the installation directory. Values:

- DISCORD_TOKEN — your bot token
- RESPONSE_CHANCE — probability (0.0-1.0) Craig reacts to trigger phrases (default 0.5)
- LOG_FILE — path to file where Craig logs
- COMMAND_PREFIX — reserved for future commands

Troubleshooting

- If the service doesn't start, run `journalctl -u craig-bot -b` to see logs.
- Ensure `python3` and `pip3` are installed and that dependencies from `requirements.txt` installed successfully.
- If you change `.env`, run `craig-restart`.

Development

Run locally for testing:

    python3 craig-bot.py

License: MIT[LICENSE]
