import os
import logging
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, ContextTypes, filters

# Logging setup for debugging and error tracking
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram Bot Token
BOT_TOKEN = "8607486883:AAEUhuhrHzzNY4-0hyrxgGekiNa70MXVTI4"

# Dictionary to store filters (Keyword list -> Reply text)
# இதில் பல வார்த்தைகளை சேமிக்கலாம். பத்தியில் இதில் உள்ள ஒரு வார்த்தை இருந்தாலும் ரிப்ளை செய்யும்.
filter_database = {
    "hi": "Hello! How can I help you?",
    "hello": "Hi there! Welcome to Zara Bot.",
    "zara": "Yes, I am Zara! Your personal assistant.",
    "help": "Type /help to see available commands.",
    "python": "Python is a powerful programming language!"
}

# Flask Web Server setup for Render (Keep-alive)
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Zara Bot with Advanced Text Filters is active and running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host="0.0.0.0", port=port)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Settings", callback_data="open_settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hello! I am **Zara**, your advanced filter assistant bot.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# /help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "**Zara Bot Help Menu**\n\n"
        "• /start - Start the bot\n"
        "• /filter [keyword] [reply] - Set a custom filter\n"
        "• /help - Get help details\n"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# /filter command handler to add custom keywords dynamically
async def set_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text(
            "⚠️ Usage format:\n`/filter keyword reply_message`\nExample: `/filter school I am studying in 11th standard`",
            parse_mode="Markdown"
        )
        return
    
    keyword = args[0].lower()
    reply_message = " ".join(args[1:])
    
    filter_database[keyword] = reply_message
    await update.message.reply_text(f"✅ Filter saved successfully for keyword: `{keyword}`", parse_mode="Markdown")

# Advanced message handler: Checks if ANY word from the paragraph matches our filter list
async def check_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    # User sent text (can be a full paragraph)
    user_paragraph = update.message.text.lower()
    
    # Split the paragraph into individual words to check accurately
    user_words = user_paragraph.split()
    
    # Check if any keyword in our database matches any word in the user's paragraph
    for keyword, reply in filter_database.items():
        if keyword in user_words or keyword in user_paragraph:
            await update.message.reply_text(reply)
            break  # Send only the first matching reply

# Settings callback handler
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "open_settings":
        back_keyboard = [
            [InlineKeyboardButton("Back", callback_data="back_to_home")]
        ]
        reply_markup = InlineKeyboardMarkup(back_keyboard)
        await query.edit_message_text(
            "**Zara Settings Menu**\n\nActive Filters Count: " + str(len(filter_database)),
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    elif query.data == "back_to_home":
        keyboard = [
            [InlineKeyboardButton("Settings", callback_data="open_settings")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Hello! I am **Zara**, your advanced filter assistant bot.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

def main():
    # Start Flask server in a separate background thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    logger.info("Flask server started in background thread.")

    # Build Telegram Application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("filter", set_filter))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), check_filters))
    application.add_handler(CallbackQueryHandler(button_callback))

    logger.info("Zara Telegram Bot is starting polling...")
    application.run_polling()

if __name__ == "__main__":
    main()
