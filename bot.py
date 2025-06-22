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
from flask import Flask
from threading import Thread

# Bot configuration
BOT_TOKEN = "7969720988:AAHexLCWd8yMmQM7NiMyPhOmyCJ61fOXDwY"
CHANNEL_USERNAME = "@sample_123456"
CHANNEL_ID = -1002659845054  # Channel ID must be negative

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

# Flask app setup for Render.com keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active!"

def run_flask():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# Start Flask server in a separate thread
Thread(target=run_flask, daemon=True).start()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with subject buttons if user is member"""
    if await check_membership(update, context):
        await show_main_menu(update, context)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display main subject menu"""
    keyboard = [[InlineKeyboardButton(subject, callback_data=f"subject_{subject}")] for subject in SUBJECTS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text(WELCOME_MSG, reply_markup=reply_markup)
    else:  # Callback query context
        await update.callback_query.edit_message_text(WELCOME_MSG, reply_markup=reply_markup)

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if user has joined channel and show join button if not"""
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, update.effective_user.id)
        if member.status in ["left", "kicked"]:
            # Show join prompt with verification button
            keyboard = [
                [InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
                [InlineKeyboardButton("✅ I've Joined", callback_data="verify_join")]
            ]
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"⚠️ Please join our channel first: {CHANNEL_USERNAME}",
                reply_markup=InlineKeyboardMarkup(keyboard)
            return False
        return True
    except Exception as e:
        logging.error(f"Membership check error: {e}")
        return True  # Skip check if there's an error

async def handle_verification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Verify channel membership after user clicks 'I've Joined' button"""
    query = update.callback_query
    await query.answer()
    
    # Verify membership again
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, query.from_user.id)
        if member.status in ["member", "administrator", "creator"]:
            await query.edit_message_text("✅ Verification successful! Loading resources...")
            await show_main_menu(update, context)
        else:
            await query.answer("❌ You haven't joined yet. Please join the channel first.", show_alert=True)
    except Exception as e:
        logging.error(f"Verification error: {e}")
        await query.answer("⚠️ Verification failed. Please try again later.", show_alert=True)

async def handle_subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show year options for selected subject"""
    if not await check_membership(update, context):
        return
        
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
    if not await check_membership(update, context):
        return
        
    query = update.callback_query
    await query.answer()
    _, subject, option = query.data.split("_", 2)
    
    # Create folder path
    folder_name = subject.replace(" & ", "_").replace(" ", "_")
    option_folder = option.replace(" ", "_")
    folder_path = f"files/{folder_name}/{option_folder}"
    
    # Send files if they exist
    if os.path.exists(folder_path):
        files_sent = False
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                files_sent = True
                with open(file_path, 'rb') as f:
                    await context.bot.send_document(
                        chat_id=query.message.chat_id,
                        document=f,
                        caption=f"📁 {subject} - {option}"
                    )
        
        if files_sent:
            # Show main menu again after sending files
            await show_main_menu(update, context)
        else:
            await query.edit_message_text("📭 No files found in this category.")
    else:
        await query.edit_message_text("📭 No files available for this selection.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle any text message"""
    if await check_membership(update, context):
        await show_main_menu(update, context)

def main():
    """Start the bot"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_verification, pattern="^verify_join$"))
    application.add_handler(CallbackQueryHandler(handle_subject, pattern="^subject_"))
    application.add_handler(CallbackQueryHandler(handle_option, pattern="^option_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start bot
    logging.info("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
