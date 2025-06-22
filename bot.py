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
CHANNEL_ID = -1002659845054

# Define subjects and years
SUBJECTS = [
    "Economics", "Gender", "Psychology", "Accounting", 
    "Managment", "PADM", "Sociology", "Journalism", 
    "Hotel & Tourism Management"
]
YEARS = ["1 year", "2 year", "3 year", "Questions"]
SEMESTERS = ["1 Semester", "2 Semester"]

# Define courses for each subject (example structure)
COURSES = {
    "Economics": ["Microeconomics", "Macroeconomics", "Econometrics", "Development Economics", "International Trade"],
    "Gender": ["Gender Studies", "Feminist Theory", "Gender and Development", "Sexuality Studies", "Women's History"],
    "Psychology": ["Cognitive Psychology", "Abnormal Psychology", "Social Psychology", "Developmental Psychology", "Biopsychology"],
    "Accounting": ["Financial Accounting", "Managerial Accounting", "Auditing", "Taxation", "Accounting Information Systems"],
    "Managment": ["Organizational Behavior", "Strategic Management", "Human Resource Management", "Operations Management", "Leadership"],
    "PADM": ["Public Policy", "Administrative Law", "Public Budgeting", "Nonprofit Management", "Urban Planning"],
    "Sociology": ["Sociological Theory", "Research Methods", "Social Stratification", "Urban Sociology", "Criminology"],
    "Journalism": ["News Writing", "Media Ethics", "Digital Journalism", "Broadcast Journalism", "Investigative Reporting"],
    "Hotel & Tourism Management": ["Hospitality Management", "Tourism Marketing", "Event Planning", "Food and Beverage Management", "Sustainable Tourism"]
}

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
logger = logging.getLogger(__name__)

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
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(WELCOME_MSG, reply_markup=reply_markup)

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if user has joined channel and show join button if not"""
    try:
        # Check membership only in private chats
        if update.effective_chat.type == "private":
            member = await context.bot.get_chat_member(CHANNEL_ID, update.effective_user.id)
            if member.status in ["left", "kicked"]:
                # Show join prompt with verification button
                keyboard = [
                    [InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
                    [InlineKeyboardButton("✅ I've Joined", callback_data="verify_join")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                if update.message:
                    await update.message.reply_text(
                        f"⚠️ Please join our channel first: {CHANNEL_USERNAME}",
                        reply_markup=reply_markup
                    )
                else:
                    query = update.callback_query
                    await query.answer()
                    await query.edit_message_text(
                        f"⚠️ Please join our channel first: {CHANNEL_USERNAME}",
                        reply_markup=reply_markup
                    )
                return False
        return True
    except Exception as e:
        logger.error(f"Membership check error: {e}")
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
        logger.error(f"Verification error: {e}")
        await query.answer("⚠️ Verification failed. Please try again later.", show_alert=True)

async def handle_subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show year options for selected subject"""
    if not await check_membership(update, context):
        return
        
    query = update.callback_query
    await query.answer()
    subject = query.data.split("_", 1)[1]
    
    # Store subject in context for later use
    context.user_data['current_subject'] = subject
    
    keyboard = [[InlineKeyboardButton(year, callback_data=f"year_{year}")] for year in YEARS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"📚 {subject} - Select Year:",
        reply_markup=reply_markup
    )

async def handle_year(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show semester options for selected year"""
    if not await check_membership(update, context):
        return
        
    query = update.callback_query
    await query.answer()
    year = query.data.split("_", 1)[1]
    
    # Store year in context
    context.user_data['current_year'] = year
    
    keyboard = [[InlineKeyboardButton(semester, callback_data=f"semester_{semester}")] for semester in SEMESTERS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"📅 {context.user_data['current_subject']} - {year} - Select Semester:",
        reply_markup=reply_markup
    )

async def handle_semester(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show course options for selected semester"""
    if not await check_membership(update, context):
        return
        
    query = update.callback_query
    await query.answer()
    semester = query.data.split("_", 1)[1]
    
    # Store semester in context
    context.user_data['current_semester'] = semester
    
    # Get courses for the current subject
    subject = context.user_data['current_subject']
    courses = COURSES.get(subject, [])
    
    # Create buttons for courses (5-8 courses)
    keyboard = []
    for i in range(0, len(courses), 2):
        row = courses[i:i+2]
        keyboard.append([InlineKeyboardButton(course, callback_data=f"course_{course}") for course in row])
    
    # Add back button
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_years")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"📖 {subject} - {context.user_data['current_year']} - {semester} - Select Course:",
        reply_markup=reply_markup
    )

async def handle_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send files for selected course"""
    if not await check_membership(update, context):
        return
        
    query = update.callback_query
    await query.answer()
    course = query.data.split("_", 1)[1]
    
    # Get current path parameters
    subject = context.user_data['current_subject']
    year = context.user_data['current_year']
    semester = context.user_data['current_semester']
    
    # Create folder path
    folder_name = subject.replace(" & ", "_").replace(" ", "_")
    year_folder = year.replace(" ", "_")
    semester_folder = semester.replace(" ", "_")
    course_folder = course.replace(" ", "_")
    
    folder_path = f"files/{folder_name}/{year_folder}/{semester_folder}/{course_folder}"
    
    # Send files if they exist
    try:
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
                            caption=f"📁 {subject} - {year}\n📅 {semester}\n📖 {course}"
                        )
            
            if files_sent:
                # Show course menu again after sending files
                await handle_semester(update, context)
            else:
                await query.edit_message_text("📭 No files found for this course.")
        else:
            await query.edit_message_text("📭 No files available for this course.")
    except Exception as e:
        logger.error(f"File sending error: {e}")
        await query.edit_message_text("⚠️ Error loading files. Please try again later.")

async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle back button navigation"""
    query = update.callback_query
    await query.answer()
    
    # Go back to year selection
    subject = context.user_data.get('current_subject', SUBJECTS[0])
    keyboard = [[InlineKeyboardButton(year, callback_data=f"year_{year}")] for year in YEARS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"📚 {subject} - Select Year:",
        reply_markup=reply_markup
    )

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
    application.add_handler(CallbackQueryHandler(handle_year, pattern="^year_"))
    application.add_handler(CallbackQueryHandler(handle_semester, pattern="^semester_"))
    application.add_handler(CallbackQueryHandler(handle_course, pattern="^course_"))
    application.add_handler(CallbackQueryHandler(handle_back, pattern="^back_to_years$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start bot
    logger.info("Bot is running with semester and course navigation...")
    application.run_polling()

if __name__ == "__main__":
    main()
