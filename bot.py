import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
import os
import asyncio
from telegram.error import Conflict

# ========== BOT CONFIGURATION ==========
BOT_TOKEN = os.getenv("BOT_TOKEN", "7969720988:AAHexLCWd8yMmQM7NiMyPhOmyCJ61fOXDwY")
CHANNEL_USERNAME = "sample_123456"  # No @
CHANNEL_ID = -1002659845054  # negative for supergroups

WELCOME_TEXT = (
    "👋 Welcome to Smart ማህደር!\n"
    "Your trusted hub for educational materials, notes, and PDFs — all in one smart place.\n\n"
    "📚 Looking for helpful resources? Just tap the buttons below to explore, download, and learn with ease.\n"
    "🧠 Stay smart. Stay ahead. With Smart ማህደር."
)

MAIN_FIELDS = [
    "Economics", "Gender", "Psychology", "Accounting", "Managment",
    "PADM", "Sociology", "Journalism", "Hotel & Tourism Management"
]
YEARS = ["1 year", "2 year", "3 year", "Questions"]
SEMESTERS = ["1 semester", "2 semester"]

# ========== YOUR COURSES DATA ==========
courses = {
    "Economics": {
        "1 year": {
            "1 semester": [
                {
                    "name": "Calculus for Economics",
                    "files": [
                        {
                            "title": "Lecture Notes",
                            "url": "https://t.me/sample_123456/4"
                        },
                        {"title": "Past Exam", "file_id": "BQACAgUAA2"}
                    ]
                },
                {
                    "name": "Accounting 1",
                    "files": [
                        {"title": "Textbook", "file_id": "BQACAgUAA3"}
                    ]
                },
                {
                    "name": "Macro Economics 1",
                    "files": [
                        {"title": "Slides", "file_id": "BQACAgUAA4"}
                    ]
                },
                {
                    "name": "Micro Economics 1",
                    "files": []
                },
                {
                    "name": "Introduction to Statistics",
                    "files": []
                },
                {
                    "name": "Basic Computer Skill of MS Applications",
                    "files": []
                }
            ],
            "2 semester": [
                {
                    "name": "Linear Algebra for Economics",
                    "files": []
                },
                {
                    "name": "Accounting 2",
                    "files": []
                },
                {
                    "name": "Macro Economics 2",
                    "files": []
                },
                {
                    "name": "Micro Economics 2",
                    "files": []
                },
                {
                    "name": "Statistics for Economics",
                    "files": []
                },
                {
                    "name": "Basic Writing Skill",
                    "files": []
                }
            ]
        },
        "2 year": {
            "1 semester": [
                {
                    "name": "Mathematical Economics",
                    "files": []
                },
                {
                    "name": "Econometrics 1",
                    "files": []
                },
                {
                    "name": "Financial Economics 1",
                    "files": []
                },
                {
                    "name": "Introduction to Management",
                    "files": []
                },
                {
                    "name": "Labor Economics",
                    "files": []
                },
                {
                    "name": "Developmental Economics 1",
                    "files": []
                },
                {
                    "name": "International Economics 1",
                    "files": []
                }
            ]
            # Add "2 semester" as needed
        }
        # Add "3 year" and "Questions" as needed
    }
    # Add more fields as needed...
}

# ========== LOGGING ==========
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========== CHANNEL MEMBERSHIP CHECK ==========
async def is_user_member(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.warning(f"Failed to check membership: {e}")
        return False

# ========== START HANDLER ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_user_member(user_id, context):
        join_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join our channel", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("✅ I have joined", callback_data="check_membership")]
        ])
        await update.message.reply_text(
            "Please join our channel to access the bot!", reply_markup=join_button
        )
        return
    # Show only main fields, without years
    keyboard = [
        [InlineKeyboardButton(field, callback_data=f"field|{field}")]
        for field in MAIN_FIELDS
    ]
    await update.message.reply_text(WELCOME_TEXT, reply_markup=InlineKeyboardMarkup(keyboard))

# ========== BUTTON HANDLER ==========
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # Special handler for "I have joined" check
    if query.data == "check_membership":
        if not await is_user_member(user_id, context):
            join_button = InlineKeyboardMarkup([
                [InlineKeyboardButton("Join our channel", url=f"https://t.me/{CHANNEL_USERNAME}")],
                [InlineKeyboardButton("✅ I have joined", callback_data="check_membership")]
            ])
            await query.edit_message_text(
                "You are still not a member of the channel. Please join and try again!",
                reply_markup=join_button
            )
            return
        # If user is a member, show the main menu
        keyboard = [
            [InlineKeyboardButton(field, callback_data=f"field|{field}")]
            for field in MAIN_FIELDS
        ]
        await query.edit_message_text(WELCOME_TEXT, reply_markup=InlineKeyboardMarkup(keyboard))
        return

    # Membership check for all other buttons
    if not await is_user_member(user_id, context):
        join_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join our channel", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("✅ I have joined", callback_data="check_membership")]
        ])
        await query.edit_message_text(
            "Please join our channel to access the bot!", reply_markup=join_button
        )
        return

    data = query.data.split("|")
    if data[0] == "field":
        field = data[1]
        keyboard = [
            [InlineKeyboardButton(year, callback_data=f"select_year|{field}|{year}")]
            for year in YEARS
        ]
        # Back button to main menu
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_main")])
        await query.edit_message_text(f"Select year for {field}:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data[0] == "year":
        year = data[1]
        keyboard = [
            [InlineKeyboardButton(field, callback_data=f"select_year|{field}|{year}")]
            for field in MAIN_FIELDS
        ]
        # Back button to main menu
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_main")])
        await query.edit_message_text(f"Select field for {year}:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data[0] == "select_year":
        field, year = data[1], data[2]
        semesters = list(courses.get(field, {}).get(year, {}).keys())
        keyboard = [
            [InlineKeyboardButton(sem, callback_data=f"semester|{field}|{year}|{sem}")] for sem in semesters
        ]
        # Back button to field menu
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=f"field|{field}")])
        await query.edit_message_text(f"Select semester for {field} - {year}:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data[0] == "semester":
        field, year, semester = data[1], data[2], data[3]
        course_list = courses.get(field, {}).get(year, {}).get(semester, [])
        keyboard = [
            [InlineKeyboardButton(course["name"], callback_data=f"course|{field}|{year}|{semester}|{idx}")]
            for idx, course in enumerate(course_list)
        ]
        # Back button to year (semester select) menu
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=f"select_year|{field}|{year}")])
        await query.edit_message_text(f"Select course for {field} - {year} - {semester}:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data[0] == "course":
        field, year, semester, idx = data[1], data[2], data[3], int(data[4])
        course = courses.get(field, {}).get(year, {}).get(semester, [])[idx]
        files = course.get("files", [])
        if files:
            keyboard = [
                [InlineKeyboardButton(f["title"], callback_data=f"file|{field}|{year}|{semester}|{idx}|{fidx}")]
                for fidx, f in enumerate(files)
            ]
            # Back button to course list
            keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=f"semester|{field}|{year}|{semester}")])
            await query.edit_message_text(
                f"Choose a file for {course['name']}:", reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            keyboard = [
                [InlineKeyboardButton("🔙 Back", callback_data=f"semester|{field}|{year}|{semester}")]
            ]
            await query.edit_message_text("No files available for this course.", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data[0] == "file":
        field, year, semester, idx, fidx = data[1], data[2], data[3], int(data[4]), int(data[5])
        course = courses.get(field, {}).get(year, {}).get(semester, [])[idx]
        file = course.get("files", [])[fidx]
        file_id = file.get("file_id")
        url = file.get("url")
        if file_id:
            await query.message.reply_document(file_id, caption=file.get("title", ""))
        elif url:
            await query.message.reply_text(f"{file.get('title', '')}: {url}")
        else:
            await query.message.reply_text("Sorry, this file is not available.")
        await query.delete_message()

    elif data[0] == "back_to_main":
        # Show main fields again (first menu)
        keyboard = [
            [InlineKeyboardButton(field, callback_data=f"field|{field}")]
            for field in MAIN_FIELDS
        ]
        await query.edit_message_text(WELCOME_TEXT, reply_markup=InlineKeyboardMarkup(keyboard))

# ========== MAIN ==========
def main():
    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button))
        logger.info("Bot is running...")
        app.run_polling()
    except Conflict as e:
        logger.error("Another instance of the bot is already running. Please stop it before starting a new one.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
