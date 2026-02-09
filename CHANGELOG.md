# Changelog

All notable changes to the Craig Discord Bot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-09

### Added
- Expanded response library with 50+ new disappointed dad responses
- New insult responses for when Craig is directly insulted (20 total)
- New disbelief/sarcasm responses (18 total)
- New exasperation responses (21 total)
- New frustration responses (20 total)
- New general/fallback responses for commands and mentions (50 total)
- **7 new slash commands**:
  - `/disappointed` - Express deep disappointment in someone or something
  - `/lecture` - Craig delivers a lengthy disappointed lecture
  - `/advice` - Craig shares unsolicited wisdom
  - `/memories` - Craig reminisces about better times
  - `/coffee` - Craig comments while drinking coffee
  - `/rant` - Craig goes on a mild rant
  - `/expectations` - Craig discusses his lowered expectations
- **2 new utility commands**:
  - `/about` - Display Craig's commands and bot information
  - `/sync` - Manually sync Craig's commands to the server (admin only)
- Enhanced response variety while maintaining consistent character personality

### Improved
- Better response coverage for all emotional categories
- More nuanced disappointed dad character development
- Increased engagement through response diversity
- Expanded command library from 4 to 13 slash commands
- Added in-Discord help system with /about command

## [1.0.5] - 2026-01-20

### Added
- `Scripts/update.sh` - Automated update script for easy version upgrades

### Improved
- Simplified update process for users with ≥[v1.0.5] installations

## [1.0.0] - Initial Release

### Added
- Discord bot with trigger-based response system
- Trigger categories: insult, disbelief, exasperation, frustration
- Slash commands: `/dadjoke`, `/roast`, `/wisdom`, `/sigh`
- Configurable response chance via environment variables
- Comprehensive logging to file and console
- Systemd service file for running as a service
- Installation, uninstallation, and update scripts
- Normalized trigger text matching for reliable phrase detection
- Direct mention detection ("Craig" in message or @mention)
- Responses tailored by trigger category
