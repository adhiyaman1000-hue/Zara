import os
import asyncio

from pyrogram import Client, filters, idle
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)


# ==========================================
# FILTER DATABASE
# ==========================================

filter_database = {
    "hi": "Hello! How can I help you?",
    "hello": "Hi there! Welcome to Zara Bot."
}


# ==========================================
# MAIN FUNCTION
# ==========================================

async def main():

    # --------------------------------------
    # Telegram credentials
    # --------------------------------------

    API_ID = int(os.environ["API_ID"])
    API_HASH = os.environ["API_HASH"]
    BOT_TOKEN = os.environ["BOT_TOKEN"]


    # --------------------------------------
    # IMPORTANT:
    # Create Pyrogram Client INSIDE
    # the running asyncio event loop
    # --------------------------------------

    app = Client(
        "ZaraBot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )


    # ======================================
    # START COMMAND
    # ======================================

    @app.on_message(filters.command("start"))
    async def start_command(client: Client, message: Message):

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⚙️ Settings",
                        callback_data="open_settings"
                    )
                ]
            ]
        )

        await message.reply_text(
            "Hello! I am **Zara**, your advanced assistant bot.",
            reply_markup=keyboard
        )


    # ======================================
    # HELP COMMAND
    # ======================================

    @app.on_message(filters.command("help"))
    async def help_command(client: Client, message: Message):

        help_text = (
            "**Zara Bot Help Menu**\n\n"
            "• /start - Start the bot\n"
            "• /help - Get help details\n"
            "• /filter - Add a filter\n"
            "• /delete - Delete a filter\n"
            "• /deleteall - Delete all filters\n"
        )

        await message.reply_text(help_text)


    # ======================================
    # ADD FILTER
    # ======================================

    @app.on_message(filters.command("filter"))
    async def add_filter(client: Client, message: Message):

        if len(message.command) < 3:

            await message.reply_text(
                "❌ Correct format:\n\n"
                "`/filter keyword your reply message`"
            )

            return


        keyword = message.command[1].lower()

        reply_text = " ".join(message.command[2:])

        filter_database[keyword] = reply_text


        await message.reply_text(
            "✅ **Filter added successfully!**\n\n"
            f"**Keyword:** `{keyword}`\n"
            f"**Reply:** {reply_text}"
        )


    # ======================================
    # DELETE FILTER
    # ======================================

    @app.on_message(filters.command("delete"))
    async def delete_filter(client: Client, message: Message):

        if len(message.command) < 2:

            await message.reply_text(
                "❌ Correct format:\n\n"
                "`/delete keyword`"
            )

            return


        keyword = message.command[1].lower()


        if keyword not in filter_database:

            await message.reply_text(
                f"❌ Filter `{keyword}` was not found."
            )

            return


        del filter_database[keyword]


        await message.reply_text(
            f"✅ Filter `{keyword}` deleted successfully."
        )


    # ======================================
    # DELETE ALL FILTERS
    # ======================================

    @app.on_message(filters.command("deleteall"))
    async def delete_all_filters(
        client: Client,
        message: Message
    ):

        filter_database.clear()

        await message.reply_text(
            "🗑️ All filters have been deleted successfully."
        )


    # ======================================
    # CHECK SAVED FILTERS
    # ======================================

    @app.on_message(
        filters.text & ~filters.command()
    )
    async def check_filters(
        client: Client,
        message: Message
    ):

        if not message.text:
            return


        user_paragraph = message.text.lower()


        for keyword, reply in filter_database.items():

            if keyword in user_paragraph:

                await message.reply_text(reply)

                break


    # ======================================
    # SETTINGS MENU
    # ======================================

    @app.on_callback_query(
        filters.regex("^open_settings$")
    )
    async def settings_menu(
        client: Client,
        callback_query: CallbackQuery
    ):

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📋 Filters",
                        callback_data="open_filters_guide"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔙 Back",
                        callback_data="back_to_home"
                    )
                ]
            ]
        )


        await callback_query.message.edit_text(
            "**Zara Settings Menu**\n\n"
            f"Active Filters Count: {len(filter_database)}\n\n"
            "Click the button below to view filter instructions.",
            reply_markup=keyboard
        )


        await callback_query.answer()


    # ======================================
    # FILTER GUIDE
    # ======================================

    @app.on_callback_query(
        filters.regex("^open_filters_guide$")
    )
    async def filters_guide(
        client: Client,
        callback_query: CallbackQuery
    ):

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔙 Back to Settings",
                        callback_data="open_settings"
                    )
                ]
            ]
        )


        guide_text = (
            "⚙️ **Filter Management Guide**\n\n"

            "1. **How to Save a Filter:**\n"
            "`/filter keyword your_reply_message`\n\n"

            "2. **How to Delete a Filter:**\n"
            "`/delete keyword`\n\n"

            "3. **How to Delete All Filters:**\n"
            "`/deleteall`\n\n"

            "4. **Usage Instructions:**\n"
            "If any word from your saved filter list appears "
            "in a sent paragraph, the bot will automatically reply."
        )


        await callback_query.message.edit_text(
            guide_text,
            reply_markup=keyboard
        )


        await callback_query.answer()


    # ======================================
    # BACK TO HOME
    # ======================================

    @app.on_callback_query(
        filters.regex("^back_to_home$")
    )
    async def back_to_home(
        client: Client,
        callback_query: CallbackQuery
    ):

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⚙️ Settings",
                        callback_data="open_settings"
                    )
                ]
            ]
        )


        await callback_query.message.edit_text(
            "Hello! I am **Zara**, your advanced assistant bot.",
            reply_markup=keyboard
        )


        await callback_query.answer()


    # ======================================
    # START BOT
    # ======================================

    print("Zara Bot is starting...")


    await app.start()


    print("Zara Bot is running successfully!")


    # Keep bot running
    await idle()


    # Stop bot when Render shuts it down
    await app.stop()


    print("Zara Bot stopped.")


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    asyncio.run(main())
