import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Telegram API credentials and Bot Token
API_ID = 6723238
API_HASH = "9b626456073105574581f3b3d4f40f3b"
BOT_TOKEN = "8607486883:AAEUhuhrHzzNY4-0hyrxgGekiNa70MXVTI4"

# Pyrogram Client setup
app = Client(
    "ZaraBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ஃபில்டர் சேமிக்கப்படும் டேட்டாபேஸ்
filter_database = {
    "hi": "Hello! How can I help you?",
    "hello": "Hi there! Welcome to Zara Bot."
}

# /start கட்டளை
@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Settings", callback_data="open_settings")]
        ]
    )
    await message.reply_text(
        "Hello! I am **Zara**, your advanced assistant bot.",
        reply_markup=keyboard
    )

# /help கட்டளை
@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    help_text = (
        "**Zara Bot Help Menu**\n\n"
        "• /start - Start the bot\n"
        "• /help - Get help details\n"
    )
    await message.reply_text(help_text)

# பத்தியில் வார்த்தை உள்ளதா என சோதித்து ரிப்ளை செய்ய
@app.on_message(filters.text & ~filters.command)
async def check_filters(client: Client, message: Message):
    if not message.text:
        return
    
    user_paragraph = message.text.lower()
    for keyword, reply in filter_database.items():
        if keyword in user_paragraph:
            await message.reply_text(reply)
            break

# Settings மெனுவை திறக்க
@app.on_callback_query(filters.regex("open_settings"))
async def settings_menu(client: Client, callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Filters", callback_data="open_filters_guide")],
            [InlineKeyboardButton("Back", callback_data="back_to_home")]
        ]
    )
    await callback_query.message.edit_text(
        "**Zara Settings Menu**\n\n"
        "Active Filters Count: " + str(len(filter_database)) + "\n"
        "Click the button below to view filter instructions.",
        reply_markup=keyboard
    )

# Filters பட்டனை அழுத்தியவுடன் காட்டும் வழிமுறைகள் (Instructions)
@app.on_callback_query(filters.regex("open_filters_guide"))
async def filters_guide(client: Client, callback_query: CallbackQuery):
    back_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Back to Settings", callback_data="open_settings")]
        ]
    )
    guide_text = (
        "⚙️ **Filter Management Guide**\n\n"
        "1. **How to Save a Filter:**\n"
        "Use the command: `/filter keyword your_reply_message`\n\n"
        "2. **How to Delete a Filter:**\n"
        "Use the command: `/delete keyword`\n\n"
        "3. **How to Delete All Filters:**\n"
        "Use the command: `/deleteall`\n\n"
        "4. **Usage Instructions:**\n"
        "If any word from your saved filter list appears in a sent paragraph, the bot will automatically reply!"
    )
    await callback_query.message.edit_text(
        guide_text,
        reply_markup=back_keyboard
    )

# முகப்பு பக்கத்திற்குத் திரும்ப
@app.on_callback_query(filters.regex("back_to_home"))
async def back_to_home(client: Client, callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Settings", callback_data="open_settings")]
        ]
    )
    await callback_query.message.edit_text(
        "Hello! I am **Zara**, your advanced assistant bot.",
        reply_markup=keyboard
    )

if __name__ == "__main__":
    print("Zara Bot is starting...")
    app.run()
