import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# உனது பாட் டோக்கன்
TOKEN = "8607486883:AAEUhuhrHzzNY4-0hyrxgGekiNa70MXVTI4"

# லாக்கிங் செட்டப்
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# டெலிகிராம் அப்ளிகேஷன் உருவாக்கம்
telegram_app = Application.builder().token(TOKEN).build()

async def setup_bot():
    await telegram_app.initialize()

# /start கமெண்ட் மற்றும் கீழே Settings பட்டன்
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_text = (
        "Hey there! My name is Zara - I'm here to help you manage your groups! "
        "Use /help to find out how to use me to my full potential.\n\n"
        "Join my news channel to get information on all the latest updates.\n\n"
        "Check /privacy to view the privacy policy, and interact with your data."
    )
    keyboard = [
        [InlineKeyboardButton("Add me to your chat!", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="open_settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(start_text, reply_markup=reply_markup)

# பட்டன் கிளிக் கையாளுதல் (Settings மற்றும் Filters)
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "open_settings":
        settings_text = "⚙️ **Settings Menu:**\n\nChoose an option below to configure your group:"
        keyboard = [
            [InlineKeyboardButton("📁 Filters", callback_data="menu_filters")],
            [InlineKeyboardButton("« Back", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(settings_text, reply_markup=reply_markup, parse_mode="Markdown")

    elif query.data == "menu_filters":
        filters_text = (
            "📁 **Filters Management:**\n\n"
            "Filters allow the bot to respond automatically when specific keywords are sent in the group.\n\n"
            "🔹 **How to set a filter:**\n"
            "Send `/save <keyword> <reply message>` in your group to save a new filter.\n"
            "🔹 **How to check filters:**\n"
            "Send `/filters` to view all saved filters in the group.\n"
            "🔹 **How to delete a filter:**\n"
            "Send `/stop <keyword>` to remove a specific filter."
        )
        keyboard = [
            [InlineKeyboardButton("« Back to Settings", callback_data="open_settings")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(filters_text, reply_markup=reply_markup, parse_mode="Markdown")

    elif query.data == "back_to_start":
        start_text = (
            "Hey there! My name is Zara - I'm here to help you manage your groups! "
            "Use /help to find out how to use me to my full potential.\n\n"
            "Join my news channel to get information on all the latest updates.\n\n"
            "Check /privacy to view the privacy policy, and interact with your data."
        )
        keyboard = [
            [InlineKeyboardButton("Add me to your chat!", url=f"https://t.me/{context.bot.username}?startgroup=true")],
            [InlineKeyboardButton("⚙️ Settings", callback_data="open_settings")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(start_text, reply_markup=reply_markup)

# பிளாஸ்க் ஹோம் ரூட்
@app.route('/')
def home():
    return "Zara Bot is running successfully with Flask!"

# டெலிகிராம் வெப்ஹுக் ரூட்
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.method == "POST":
        json_data = request.get_json(force=True)
        update = Update.de_json(json_data, telegram_app.bot)
        
        async def process():
            await telegram_app.process_update(update)

        asyncio.run(process())
    return "OK"

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_bot())
    
    # ஹேண்ட்லர்கள் இணைப்பு
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CallbackQueryHandler(button_callback))
    
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
