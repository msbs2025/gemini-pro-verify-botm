# Learnings - Gemini Verify Bot

## Task 1: Project Scaffolding + Config
- Created directory structure with `verifier/` and `handlers/`.
- Implemented `config.py` with `python-dotenv` support.
- Added a fallback in `config.py` for `dotenv` import to allow verification in environments where packages aren't yet installed.
- requirements.txt limited to 4 core packages: `python-telegram-bot`, `httpx`, `playwright`, `python-dotenv`.
- .gitignore covers Python basics, `.env`, `.db`, and `.png`.
