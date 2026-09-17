import os
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

BOT_TOKEN = "8607486883:AAEUhuhrHzzNY4-0hyrxgGekiNa70MXVTI4"

app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Zara Bot is active and running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host="0.0.0.0", port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Settings", callback_data="open_settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hello! I am **Zara**, your advanced assistant bot.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "**Zara Bot Help Menu**\n\n"
        "• /start - Start the bot\n"
        "• /help - Get help details\n"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "open_settings":
        back_keyboard = [
            [InlineKeyboardButton("Back", callback_data="back_to_home")]
        ]
        reply_markup = InlineKeyboardMarkup(back_keyboard)
        await query.edit_message_text(
            "**Zara Settings Menu**\n\nAdvanced configurations will be added here soon.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    elif query.data == "back_to_home":
        keyboard = [
            [InlineKeyboardButton("Settings", callback_data="open_settings")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Hello! I am **Zara**, your advanced assistant bot.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

def main():
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_callback))

    application.run_polling()

if __name__ == "__main__":
    main()
