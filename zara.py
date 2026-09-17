import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Updater

# உனது பாட் டோக்கன்
TOKEN = "8607486883:AAEUhuhrHzzNY4-0hyrxgGekiNa70MXVTI4"

# லாக்கிங் செட்டப்
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# /start கமெண்ட் மற்றும் கீழே Settings பட்டன்
def start(update: Update, context: CallbackContext):
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
    update.message.reply_text(start_text, reply_markup=reply_markup)

# Settings பட்டனை கையாளுதல்
def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "open_settings":
        settings_text = "⚙️ **Settings Menu:**\n\n(Filters and other settings will be added here step by step!)"
        keyboard = [
            [InlineKeyboardButton("« Back", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.edit_text(settings_text, reply_markup=reply_markup, parse_mode="Markdown")

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
        query.message.edit_text(settings_text if 'settings_text' in locals() else start_text, reply_markup=reply_markup)

def main():
    # பாட் அப்ளிகேஷன் உருவாக்கம் (Updater முறை - எரர் வராது)
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # ஹேண்ட்லர்கள் இணைப்பு
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_callback))

    print("Zara Bot is running successfully...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
