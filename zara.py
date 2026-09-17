import os
import asyncio
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

# Start command handler
@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    # Settings button creation
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Settings", callback_data="open_settings")]
        ]
    )
    await message.reply_text(
        "Hello! I am **Zara**, your advanced assistant bot.",
        reply_markup=keyboard
    )

# Help command handler
@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    help_text = (
        "**Zara Bot Help Menu**\n\n"
        "• /start - Start the bot\n"
        "• /help - Get help details\n"
    )
    await message.reply_text(help_text)

# Settings button callback handler
@app.on_callback_query(filters.regex("open_settings"))
async def settings_menu(client: Client, callback_query: CallbackQuery):
    back_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Back", callback_data="back_to_home")]
        ]
    )
    await callback_query.message.edit_text(
        "**Zara Settings Menu**\n\n"
        "Advanced configurations will be added here soon.",
        reply_markup=back_keyboard
    )

# Back button callback handler
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
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    app.run()



