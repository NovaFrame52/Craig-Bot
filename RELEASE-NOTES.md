# Release Notes

## Version 2.0.0 - February 9, 2026

### Overview
Craig Discord Bot version 2.0.0 is a major update that massively expands both Craig's personality and interactive capabilities. With 50+ new responses across all emotional categories and 7 new slash commands, Craig is now more engaging and entertaining than ever while maintaining his signature disappointed dad character.

### What's New

#### Expanded Response Library
- **Insult Responses**: 10 new responses when Craig is insulted directly
  - Examples: "Nice. Really nice. That's how you talk to someone who paid for your childhood?"
  - Total: 20 responses

- **Disbelief Responses**: 9 new responses for expressing doubt and sarcasm
  - Examples: "As hard as it is to swallow, I'm telling the truth."
  - Total: 18 responses

- **Exasperation Responses**: 10 new responses for frustrated, tired reactions
  - Examples: "This is why I drink coffee at 3 PM."
  - Total: 21 responses

- **Frustration Responses**: 10 new responses for general frustration
  - Examples: "Yeah, well, join the club. We meet on Thursdays."
  - Total: 20 responses

- **General/Fallback Responses**: 15 new responses for commands and mentions
  - Examples: "I'm writing a book. You're chapter twelve."
  - Total: 50 responses

#### 7 New Slash Commands
Craig now has 13 slash commands total (up from 4):

- **`/disappointed [target]`** - Express deep disappointment in someone or something
  - Example: "Whatever, I looked at you and all I felt was disappointment."

- **`/lecture`** - Craig delivers a lengthy disappointed lecture
  - Example: "Sit down. We need to talk about your life choices. All of them."

- **`/advice`** - Craig shares unsolicited wisdom
  - Example: "My advice? Lower your expectations. For yourself. Significantly."

- **`/memories`** - Craig reminisces about better times
  - Example: "You know, there was a time when you made decisions I didn't immediately regret."

- **`/coffee`** - Craig has commentary while drinking coffee
  - Example: "*takes a long sip of coffee* This is getting cold faster than my faith in you."

- **`/rant`** - Craig goes on a mild rant about life
  - Example: "You know what really grinds my gears? Everything. Absolutely everything."

- **`/expectations`** - Craig discusses his lowered expectations
  - Example: "My expectations for you are so low, even you can clear them. And yet..."

#### 2 New Utility Commands
- **`/about`** - Display Craig's commands and bot information
  - Shows all available commands with descriptions in a formatted message
  - Accessible to all users

- **`/sync`** - Manually sync Craig's commands to the server
  - Requires administrator permissions
  - Useful if commands don't appear immediately after bot start

Previous commands still available:
- `/dadjoke` - Get a random dad joke
- `/roast` - Get roasted by Craig
- `/wisdom` - Craig shares life lessons
- `/sigh` - Craig expresses disappointment with just a sigh

### Character Development
The expanded response library and new commands deepen Craig's character as a disappointed dad who:
- Uses dark humor and sarcasm consistently
- References family history and shared memories
- Expresses quiet disappointment mixed with resigned acceptance
- Has specific commentary on different situations and emotions
- Maintains a consistent voice across all interactions

### Installation & Usage
No code changes required to existing installations. Simply pull the latest version and restart the bot:

```bash
./Scripts/update.sh
systemctl restart craig-bot
```

Explore the new commands to see Craig's expanded personality in action.

### System Requirements
- Python 3.8+
- discord.py library
- python-dotenv library

### Known Issues
None at this time.

### Notes
- All responses are triggered based on message content
- Direct mentions always receive a response
- Trigger-based responses have configurable probability (default: 50%)
- See `README.md` for full configuration details

---

## Version 1.0.5 - January 20, 2026

### Overview
Version 1.0.5 is a maintenance release that improves the update process for existing installations.

### What's New

#### Automated Update Script
- Added `Scripts/update.sh` for easy version updates
- Simplifies the process of upgrading to newer versions
- Users can now update with a single command instead of manual git operations

### Installation
To update from v1.0.0 to v1.0.5:

```bash
chmod +x Scripts/update.sh
./Scripts/update.sh
sudo systemctl restart craig-bot
```

### System Requirements
- Python 3.8+
- discord.py library
- python-dotenv library
- systemd (for service management)

### Known Issues
None at this time.

### Notes
- This release maintains full backward compatibility with v1.0.0
- No configuration changes required
- All existing commands and responses remain unchanged

---

## Version 1.0.0 - Initial Release

### Overview
The initial release of Craig Discord Bot, a fully functional Discord bot that embodies the personality of a disappointed father. Craig responds to specific trigger phrases and direct mentions with curated, humorous responses.

### Features

#### Trigger-Based Response System
- **4 Response Categories**:
  - Insult responses (20 total)
  - Disbelief/sarcasm responses (9 total)
  - Exasperation responses (11 total)
  - Frustration responses (10 total)
  - General/fallback responses (35 total)
- **75 Total Responses** across all categories
- Normalized text matching for reliable phrase detection
- Configurable response probability via `RESPONSE_CHANCE` environment variable

#### Trigger Phrases
Craig automatically responds to 50+ trigger phrases across four categories:
- **Insults**: "fuck you", "oh fuck you", "fuck yourself", "fuck off", "piss off", "go fuck", "bite me", "suck it", "kiss my ass", "screw you"
- **Disbelief**: "are you kidding me", "are you serious", "youre kidding", "you gotta be kidding", "no fucking way", "absolutely not"
- **Exasperation**: "what the hell", "what the fuck", "wtf", "this is bullshit", "this is crap", "come on"
- **Frustration**: "fuck this", "fuck that", "screw this", "how stupid", "how dumb", "youre shitting me"

#### Slash Commands (4 Total)
- `/dadjoke` - Get a random disappointed dad response
- `/roast [target]` - Get roasted by Craig (target optional)
- `/wisdom` - Craig shares a life lesson
- `/sigh` - Craig expresses disappointment with a sigh

#### Direct Mentions
- Craig always responds when:
  - His name is mentioned anywhere in the message
  - He is directly @mentioned
- Response type varies based on context (insult or general)

#### System Features
- Comprehensive logging to both file and console
- Systemd service integration for auto-start on boot
- Easy management commands for start/stop/restart/status
- Python virtual environment isolation
- Environment variable configuration via `.env` file

### Installation
The bot includes an automated installation script:

```bash
chmod +x Scripts/install.sh
sudo Scripts/install.sh
```

The installer handles:
- Virtual environment setup
- Python dependency installation
- Discord bot token configuration
- Systemd service registration
- Management command aliases

### Configuration
Configured via `.env` file with variables:
- `DISCORD_TOKEN` - Discord bot token (required)
- `RESPONSE_CHANCE` - Trigger response probability (0.0-1.0, default: 0.5)
- `LOG_FILE` - Log file path (default: craig.log)

### System Requirements
- Python 3.8+
- discord.py library
- python-dotenv library
- systemd (for service management)
- Discord bot token from Discord Developer Portal

### Known Limitations
- Limited slash command set (4 commands)
- Smaller response library
- Basic character personality foundation

### Notes
- All responses maintain a consistent disappointed dad character
- Responses are deterministic based on trigger category
- Bot requires proper Discord permissions for messaging and reading message content

---

For more detailed information, see [CHANGELOG.md](CHANGELOG.md)
