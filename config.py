import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # During scaffold verification, python-dotenv might not be installed in the environment
    pass

BOT_TOKEN = os.getenv("BOT_TOKEN")
