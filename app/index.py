import os
import logging
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message when the /start command is issued."""
    await update.message.reply_text(
        "Welcome to the bot! You can use /links to see available links."
    )

async def links_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message with inline keyboard buttons for useful links."""
    keyboard = [
        [InlineKeyboardButton("Google", url="https://www.google.com")],
        [InlineKeyboardButton("Telegram", url="https://telegram.org")],
        [InlineKeyboardButton("Vercel", url="https://vercel.com")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Here are some useful links:", reply_markup=reply_markup)

if __name__ == "__main__":
    # Get the bot token from environment variables
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in environment variables.")
        exit()

    # Create the Application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("links", links_command))

    # Note: We are not running bot.run_polling() or bot.start_webhook() here
    # as this script is intended to be deployed on a serverless platform like Vercel,
    # which will handle the execution.
    logger.info("Bot application configured. Ready for serverless deployment.")
