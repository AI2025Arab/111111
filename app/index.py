import telebot
from telebot import types
import os
import logging
import json

# Get the bot token from environment variables
API_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# Initialize bot
# Using "dummy_token" if API_TOKEN is None allows the file to be imported by Vercel for introspection
# even if the env var is missing during build, but operations will fail if it's not set at runtime.
# The handler function will check for API_TOKEN at runtime.
bot = telebot.TeleBot(API_TOKEN if API_TOKEN else "dummy_token_for_init", threaded=False)

# Setup basic logging
logger = telebot.logger
# Set level to INFO, can be changed to DEBUG for more verbose output during development/debugging
telebot.logger.setLevel(logging.INFO)

if not API_TOKEN:
    # Log a critical error if the token is missing. The bot will not function.
    # This log will appear when Vercel loads the file if the token isn't set.
    logger.critical("CRITICAL: TELEGRAM_BOT_TOKEN environment variable is not set at import time!")


# --- Define command handlers ---

# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info(f"Processing /start command for chat ID: {message.chat.id}")
    if not API_TOKEN: # Runtime check
        logger.error("Cannot send welcome message, API_TOKEN is not configured.")
        return
    try:
        bot.reply_to(message, "Welcome! This bot is built with pyTelegramBotAPI. Use /links to see some links.")
        logger.info(f"Replied to /start command for chat ID: {message.chat.id}")
    except Exception as e:
        logger.error(f"Error in send_welcome for chat ID {message.chat.id}: {e}", exc_info=True)

# Handle '/links'
@bot.message_handler(commands=['links'])
def links_command(message):
    logger.info(f"Processing /links command for chat ID: {message.chat.id}")
    if not API_TOKEN: # Runtime check
        logger.error("Cannot send links, API_TOKEN is not configured.")
        return
    try:
        markup = types.InlineKeyboardMarkup()
        btn_google = types.InlineKeyboardButton("Google", url="https://www.google.com")
        btn_telegram = types.InlineKeyboardButton("Telegram", url="https://telegram.org")
        btn_vercel = types.InlineKeyboardButton("Vercel", url="https://vercel.com")
        markup.add(btn_google)
        markup.add(btn_telegram)
        markup.add(btn_vercel)
        bot.reply_to(message, "Here are some useful links:", reply_markup=markup)
        logger.info(f"Replied to /links command for chat ID: {message.chat.id}")
    except Exception as e:
        logger.error(f"Error in links_command for chat ID {message.chat.id}: {e}", exc_info=True)


# --- Vercel Handler ---
# Vercel's Python runtime will call this function for each incoming HTTP request.
# The 'event' parameter (first parameter) will contain the parsed JSON body of the webhook request from Telegram.
def handler(event, context=None): # 'context' is optional, Vercel might pass it but we don't use it.
    if not API_TOKEN:
        logger.critical("CRITICAL: TELEGRAM_BOT_TOKEN is not set. Cannot process Telegram update.")
        return {'statusCode': 500, 'body': 'Bot configuration error: Token not set.'}

    try:
        # 'event' from Vercel (for a JSON POST) is expected to be the parsed dictionary from Telegram.
        if isinstance(event, dict):
            # If Vercel passes the parsed JSON as a dict directly
            update_payload = event
        elif isinstance(event, str):
            # If Vercel passes the body as a string (less common for application/json POSTs)
            logger.debug("Event body is a string, attempting to parse as JSON.")
            update_payload = json.loads(event)
        else:
            logger.error(f"Unexpected event type: {type(event)}. Event content (first 200 chars): {str(event)[:200]}")
            return {'statusCode': 400, 'body': 'Invalid request format.'}

        logger.debug(f"Received update payload: {update_payload}")
        update = telebot.types.Update.de_json(update_payload)
        bot.process_new_updates([update])
        logger.info("Telegram update processed successfully.")
        return {'statusCode': 200, 'body': 'OK'}

    except json.JSONDecodeError as e:
        logger.error(f"JSONDecodeError: Failed to parse event. Error: {e}. Event (first 200 chars if string): {str(event)[:200] if isinstance(event, str) else 'Event is not a string.'}", exc_info=True)
        return {'statusCode': 400, 'body': 'Invalid JSON input'}
    except Exception as e:
        logger.error(f"Error processing Telegram update: {e}", exc_info=True)
        return {'statusCode': 500, 'body': 'Internal server error processing update.'}

# For local development testing (run this file directly: python app/index.py)
# This block will not run on Vercel.
if __name__ == "__main__":
    # Setup more verbose logging for local development if needed.
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.info("Running bot in local development mode (polling)...")

    if not API_TOKEN:
        logger.critical("CRITICAL: TELEGRAM_BOT_TOKEN environment variable not set. Cannot start local polling.")
    else:
        # To prevent issues with the logger during polling and ensure detailed logs:
        # bot.polling(none_stop=True) # This is a simpler way
        # A more robust way for local polling if you face issues:
        logger.info("Starting infinity_polling() for local development.")
        try:
            # infinity_polling is blocking, good for scripts.
            # logger_level can make telebot's internal logs more verbose.
            bot.infinity_polling(logger_level=logging.DEBUG, timeout=60, long_polling_timeout=30)
        except Exception as e_poll:
            logger.critical(f"Infinity polling failed during local development: {e_poll}", exc_info=True)
        logger.info("Local polling stopped.")
