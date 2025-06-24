import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# Bot configuration
BOT_TOKEN = "7969720988:AAHexLCWd8yMmQM7NiMyPhOmyCJ61fOXDwY"
CHANNEL_USERNAME = "@HUESAchannel"
CHANNEL_ID = -1002040479523  # Channel ID must be negative

# Define subjects and options
SUBJECTS = [
    "Economics", "Gender", "Psychology", "Accounting", 
    "Managment", "PADM", "Sociology", "Journalism", 
    "Hotel & Tourism Management"
]
OPTIONS = ["1 year", "2 year", "3 year", "Questions"]

# Welcome message
WELCOME_MSG = """👋 Welcome to Smart ማህደር!
Your trusted hub for educational materials, notes, and PDFs — all in one smart place.

📚 Looking for helpful resources? Just tap the buttons below to explore, download, and learn with ease.
🧠 Stay smart. Stay ahead. With Smart ማህደር."""

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with subject buttons if user is member"""
    if await check_membership(update, context):
        keyboard = [[InlineKeyboardButton(subject, callback_data=f"subject_{subject}")] for subject in SUBJECTS]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(WELCOME_MSG, reply_markup=reply_markup)

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if user has joined channel"""
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, update.effective_user.id)
        if member.status in ["left", "kicked"]:
            await update.message.reply_text(
                f"⚠️ Please join our channel first: {CHANNEL_USERNAME}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]
                ])
            )
            return False
        return True
    except Exception:
        return True  # Skip check if there's an error

async def handle_subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show year options for selected subject"""
    query = update.callback_query
    await query.answer()
    subject = query.data.split("_", 1)[1]
    
    keyboard = [[InlineKeyboardButton(option, callback_data=f"option_{subject}_{option}")] for option in OPTIONS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"📚 {subject} - Select Year:",
        reply_markup=reply_markup
    )

async def handle_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send files for selected subject and year"""
    query = update.callback_query
    await query.answer()
    _, subject, option = query.data.split("_", 2)
    
    # Create folder path
    folder_name = subject.replace(" & ", "_").replace(" ", "_")
    option_folder = option.replace(" ", "_")
    folder_path = f"files/{folder_name}/{option_folder}"
    
    # Send files if they exist
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    await context.bot.send_document(
                        chat_id=query.message.chat_id,
                        document=f,
                        caption=f"📁 {subject} - {option}"
                    )
        # Show main menu again
        keyboard = [[InlineKeyboardButton(subject, callback_data=f"subject_{subject}")] for subject in SUBJECTS]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Select another subject:",
            reply_markup=reply_markup
        )
    else:
        await query.edit_message_text("📭 No files available for this selection.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle any text message"""
    if await check_membership(update, context):
        await start(update, context)

def main():
    """Start the bot"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_subject, pattern="^subject_"))
    application.add_handler(CallbackQueryHandler(handle_option, pattern="^option_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start bot
    application.run_polling()

if __name__ == "__main__":
    main()
