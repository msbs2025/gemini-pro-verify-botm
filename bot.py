"""Telegram bot entry point - Gemini Verify Bot"""
import logging
import os

from telegram.ext import Application, CommandHandler

from config import BOT_TOKEN
from database import Database
from handlers import commands
from handlers.commands import start_command, help_command, verify_command

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def error_handler(update: object, context) -> None:
    """Global error handler"""
    logger.error(f"Update {update} caused error: {context.error}")


def main():
    """Main entry point"""
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Initialize database
    db = Database()
    
    # Inject database into handlers module
    commands.db = db
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("verify", verify_command))
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    logger.info("Bot starting...")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
