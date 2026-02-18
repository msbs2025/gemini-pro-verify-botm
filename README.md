# Gemini Pro Verify Bot (Telegram)

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](Dockerfile)

A Telegram bot that automates SheerID student verification to get **Google AI Pro (Gemini Pro)** free for 1 year.

## Features

- **Auto-generate student identity** — Random name, PSU email, date of birth, and Student ID
- **Student card PNG** — LionPATH Penn State University template rendered as PNG screenshot via Playwright
- **6-step SheerID verification** — Submit personal data → skip SSO → upload document → done
- **SQLite logging** — Every verification attempt is logged to a local database
- **Docker support** — Ready to deploy via Docker Compose

---

## Prerequisites

- **Python** 3.11 or later
- **Docker** and **Docker Compose** (optional, for container deployment)

---

## Getting Your BOT_TOKEN

This bot requires a token from Telegram BotFather. Follow these steps:

1. Open **Telegram** and search for **@BotFather**
2. Send the command `/newbot`
3. BotFather will ask for a **bot name** — type your desired name (e.g., `Gemini Verify Bot`)
4. Next, enter a **bot username** ending with `bot` (e.g., `gemini_verify_bot`)
5. Once done, BotFather will provide a **token** that looks like this:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
6. **Copy the token** — this will be used as your `BOT_TOKEN`

---

## Quick Start (Local)

```bash
# 1. Clone the repository
git clone <repository-url>
cd gemini-pro-verify-bot

# 2. Copy the configuration file
cp .env.example .env

# 3. Open .env and fill in BOT_TOKEN with your BotFather token
#    BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install Chromium browser for Playwright
playwright install chromium

# 6. Run the bot
python bot.py
```

If successful, the terminal will display a log like:
```
2025-xx-xx - __main__ - INFO - Bot starting...
```

---

## Quick Start (Docker)

```bash
# 1. Copy configuration file and fill in BOT_TOKEN
cp .env.example .env
# Edit .env, fill in BOT_TOKEN

# 2. Build and run the container
docker-compose up -d

# 3. View bot logs
docker-compose logs -f bot

# 4. To stop the bot
docker-compose down
```

> **Important:** Docker Compose is configured with `shm_size: 2gb` which is required by Playwright/Chromium. Do not modify this configuration.

---

## Bot Usage

After the bot is running, open Telegram and search for your bot by the username you registered with BotFather.

### Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Display welcome message |
| `/help` | Display usage instructions |
| `/verify <link>` | Run SheerID verification process |

### How to Get the SheerID Link

1. Open the **Google AI Pro** (Gemini Pro) registration page in your browser
2. Select the student verification option — you will be redirected to SheerID
3. Copy the URL from the browser. The URL contains a `verificationId` parameter, for example:
   ```
   https://services.sheerid.com/verify/67c8c14f5f17a83b745e3f82/?verificationId=abc123def456
   ```
4. Send it to the bot:
   ```
   /verify https://services.sheerid.com/verify/67c8c14f5f17a83b745e3f82/?verificationId=abc123def456
   ```

The bot will automatically:
- Generate a fake student identity
- Create a student card PNG screenshot
- Submit to the SheerID API
- Report the result (success/pending/failed)

---

## Project Structure

```
gemini-pro-verify-bot/
├── bot.py                  # Main bot entry point
├── config.py               # Load BOT_TOKEN from .env
├── database.py             # SQLite verification logging
├── requirements.txt        # Python dependencies
├── .env.example            # Configuration template
├── .gitignore              # Git ignored files
├── Dockerfile              # Docker image for the bot
├── docker-compose.yml      # Docker Compose configuration
├── LICENSE                 # MIT License
├── data/
│   └── verifications.db    # SQLite database (auto-created)
├── verifier/
│   ├── __init__.py
│   ├── config.py           # PROGRAM_ID, university list, API URLs
│   ├── sheerid.py          # SheerID API client (6-step flow)
│   ├── identity.py         # Name, email, date of birth generator
│   └── document.py         # Student card HTML → PNG generator
└── handlers/
    ├── __init__.py
    └── commands.py          # /start, /help, /verify command handlers
```

---

## Configuration

### `.env` File

Only one variable is required:

```env
BOT_TOKEN=your_bot_token_here
```

### `verifier/config.py`

This file contains the SheerID configuration:

| Variable | Value | Description |
|----------|-------|-------------|
| `PROGRAM_ID` | `67c8c14f5f17a83b745e3f82` | Gemini program ID on SheerID |
| `SHEERID_BASE_URL` | `https://services.sheerid.com` | SheerID API base URL |
| `DEFAULT_SCHOOL_ID` | `2565` | Penn State University - Main Campus |

---

## Important Notes

### PROGRAM_ID May Expire

`PROGRAM_ID` is the verification program ID from Google/SheerID. If verifications start failing with errors, the ID may have expired. To update it:

1. Open the Google AI Pro registration page in your browser
2. Open Developer Tools (F12) → Network tab
3. Look for requests to `services.sheerid.com` — the URL contains the new PROGRAM_ID
4. Update the `PROGRAM_ID` value in `verifier/config.py`

### Personal Use

This bot is designed for **personal use only**. There is no credit system, user registration, or admin panel. Anyone with access to your bot on Telegram can use it.

### Docker — Shared Memory

The `shm_size: '2gb'` configuration in `docker-compose.yml` is **required**. Playwright Chromium needs large shared memory for rendering. Without this configuration, Chromium will crash when creating student card screenshots.

---

## License

This project is licensed under the [MIT License](LICENSE).
