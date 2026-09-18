import os
import json
import logging
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8607486883:AAEUhuhrHzzNY4-0hyrxgGekiNa70MXVTI4"
FILTER_FILE = "filter_backup.json"

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

app = Flask(__name__)
telegram_app = Application.builder().token(TOKEN).build()

# பில்டர்ஸ்களை லோட் செய்தல் (GitHub/Local Backup-ல் இருந்து)
def load_filters():
    if os.path.exists(FILTER_FILE):
        try:
            with open(FILTER_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_filters(data):
    with open(FILTER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

filters_db = load_filters()

# /start கமெண்ட்
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Add me to your chat!", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="open_settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Hey there! My name is Zara - I'm here to help you manage your groups!", reply_markup=reply_markup)

# பட்டன் கையாளுதல்
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "open_settings":
        keyboard = [
            [InlineKeyboardButton("📁 Filters", callback_data="menu_filters")],
            [InlineKeyboardButton("« Back", callback_data="back_to_start")]
        ]
        await query.message.edit_text("⚙️ **Settings Menu:**", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    elif query.data == "menu_filters":
        keyboard = [[InlineKeyboardButton("« Back to Settings", callback_data="open_settings")]]
        text = "📁 **Filters Management:**\n\nUse `/save <keyword> <reply>` to add a filter."
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    elif query.data == "back_to_start":
        keyboard = [
            [InlineKeyboardButton("Add me to your chat!", url=f"https://t.me/{context.bot.username}?startgroup=true")],
            [InlineKeyboardButton("⚙️ Settings", callback_data="open_settings")]
        ]
        await query.message.edit_text("Hey there! My name is Zara - I'm here to help you manage your groups!", reply_markup=InlineKeyboardMarkup(keyboard))

# பில்டர் சேமிக்கும் கமெண்ட் (/save)
async def save_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /save <keyword> <reply message>")
        return
    keyword = args[0].lower()
    reply_text = " ".join(args[1:])
    
    chat_id = str(update.effective_chat.id)
    if chat_id not in filters_db:
        filters_db[chat_id] = {}
    
    filters_db[chat_id][keyword] = reply_text
    save_filters(filters_db)
    await update.message.reply_text(f"Saved filter for keyword: `{keyword}`", parse_mode="Markdown")

# பில்டரைச் சோதித்து பதில் அளிக்கும் பகுதி
async def check_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    chat_id = str(update.effective_chat.id)
    text = update.message.text.lower()
    
    if chat_id in filters_db:
        for keyword, reply in filters_db[chat_id].items():
            if keyword in text:
                await update.message.reply_text(reply)
                break

@app.route('/')
def home():
    return "Zara Bot with Backup is running!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.method == "POST":
        json_data = request.get_json(force=True)
        update = Update.de_json(json_data, telegram_app.bot)
        asyncio.run(telegram_app.process_update(update))
    return "OK"

if __name__ == '__main__':
    asyncio.run(telegram_app.initialize())
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("save", save_filter))
    telegram_app.add_handler(CallbackQueryHandler(button_callback))
    from telegram.ext import MessageHandler, filters
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_filters))
    
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
