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
    MessageHandler,
    filters,
)
import os
import asyncio
from telegram.error import Conflict

# --- Dummy web server for deployment platforms requiring open ports ---
from aiohttp import web

async def handle(request):
    return web.Response(text="Bot is running!")

def start_web_server():
    port = int(os.environ.get("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, "0.0.0.0", port)
    loop.run_until_complete(site.start())
    print(f"Dummy web server running on port {port}")

# ========== BOT CONFIGURATION ==========
BOT_TOKEN = os.getenv("BOT_TOKEN", "PASTE_YOUR_BOT_TOKEN_HERE")
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

# ====== UTIL: PREVENT EDIT MESSAGE ERROR ======
def is_same_message(message, new_text, new_reply_markup):
    current_text = message.text or ""
    current_markup = message.reply_markup
    return (current_text == (new_text or "")) and (current_markup == new_reply_markup)

# ========== YOUR COURSES DATA ==========
courses = {
    "Economics": {
        "1 year": {
            "1 semester": [
                {
                    "name": "Calculus for Economics",
                    "files": [
                        {"file_id": "BQACAgQAAyEFAASeigO-AAMEaFh1xjxYUA9dOnrzT9gLMs7U_U8AAtEYAAKhpchSpSkYPNh2RDs2BA"},
                        {"file_id": "BQACAgQAAyEFAASeigO-AAMFaFh1xr6Nhb5I8lvjtmVVwfrrx1oAAtIYAAKhpchSu9ofq12HUWM2BA"}
                    ]
                },
                {
                    "name": "Accounting 1",
                    "files": [
                        {"title": "Textbook", "file_id": "PASTE_REAL_FILE_ID_3"}
                    ]
                },
                {
                    "name": "Macro Economics 1",
                    "files": [
                        {"title": "Slides", "file_id": "PASTE_REAL_FILE_ID_4"}
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
        }
    }
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
    join_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Join our channel", url=f"https://t.me/{CHANNEL_USERNAME}")],
        [InlineKeyboardButton("✅ I have joined", callback_data="check_membership")]
    ])
    if not await is_user_member(user_id, context):
        if not is_same_message(update.message, "Please join our channel to access the bot!", join_button):
            await update.message.reply_text(
                "Please join our channel to access the bot!", reply_markup=join_button
            )
        return
    # Show only main fields, without years
    keyboard = [
        [InlineKeyboardButton(field, callback_data=f"field|{field}")]
        for field in MAIN_FIELDS
    ]
    if not is_same_message(update.message, WELCOME_TEXT, InlineKeyboardMarkup(keyboard)):
        await update.message.reply_text(WELCOME_TEXT, reply_markup=InlineKeyboardMarkup(keyboard))

# ========== BUTTON HANDLER ==========
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    join_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Join our channel", url=f"https://t.me/{CHANNEL_USERNAME}")],
        [InlineKeyboardButton("✅ I have joined", callback_data="check_membership")]
    ])

    # Special handler for "I have joined" check
    if query.data == "check_membership":
        if not await is_user_member(user_id, context):
            if not is_same_message(query.message, "You are still not a member of the channel. Please join and try again!", join_button):
                await query.edit_message_text(
                    "You are still not a member of the channel. Please join and try again!",
                    reply_markup=join_button
                )
            return
        keyboard = [
            [InlineKeyboardButton(field, callback_data=f"field|{field}")]
            for field in MAIN_FIELDS
        ]
        markup = InlineKeyboardMarkup(keyboard)
        if not is_same_message(query.message, WELCOME_TEXT, markup):
            await query.edit_message_text(WELCOME_TEXT, reply_markup=markup)
        return

    # Membership check for all other buttons
    if not await is_user_member(user_id, context):
        if not is_same_message(query.message, "Please join our channel to access the bot!", join_button):
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
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_main")])
        text = f"Select year for {field}:"
        markup = InlineKeyboardMarkup(keyboard)
        if not is_same_message(query.message, text, markup):
            await query.edit_message_text(text, reply_markup=markup)

    elif data[0] == "year":
        year = data[1]
        keyboard = [
            [InlineKeyboardButton(field, callback_data=f"select_year|{field}|{year}")]
            for field in MAIN_FIELDS
        ]
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_main")])
        text = f"Select field for {year}:"
        markup = InlineKeyboardMarkup(keyboard)
        if not is_same_message(query.message, text, markup):
            await query.edit_message_text(text, reply_markup=markup)

    elif data[0] == "select_year":
        field, year = data[1], data[2]
        semesters = list(courses.get(field, {}).get(year, {}).keys())
        keyboard = [
            [InlineKeyboardButton(sem, callback_data=f"semester|{field}|{year}|{sem}")] for sem in semesters
        ]
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=f"field|{field}")])
        text = f"Select semester for {field} - {year}:"
        markup = InlineKeyboardMarkup(keyboard)
        if not is_same_message(query.message, text, markup):
            await query.edit_message_text(text, reply_markup=markup)

    elif data[0] == "semester":
        field, year, semester = data[1], data[2], data[3]
        course_list = courses.get(field, {}).get(year, {}).get(semester, [])
        keyboard = [
            [InlineKeyboardButton(course["name"], callback_data=f"course|{field}|{year}|{semester}|{idx}")]
            for idx, course in enumerate(course_list)
        ]
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=f"select_year|{field}|{year}")])
        text = f"Select course for {field} - {year} - {semester}:"
        markup = InlineKeyboardMarkup(keyboard)
        if not is_same_message(query.message, text, markup):
            await query.edit_message_text(text, reply_markup=markup)

    elif data[0] == "course":
        field, year, semester, idx = data[1], data[2], data[3], int(data[4])
        course = courses.get(field, {}).get(year, {}).get(semester, [])[idx]
        files = course.get("files", [])
        if course["name"] == "Calculus for Economics" and len(files) == 2 and all("file_id" in f for f in files):
            for f in files:
                file_id = f.get("file_id")
                if file_id:
                    await query.message.reply_document(
                        file_id,
                        protect_content=True
                    )
            # Show back button after sending files, and resend file menu at the top for chat history style
            keyboard = [
                [InlineKeyboardButton("🔙 Back", callback_data=f"semester|{field}|{year}|{semester}")]
            ]
            text = "Choose what to do next:"
            markup = InlineKeyboardMarkup(keyboard)
            # Send the course menu again, so files always appear above the back button
            course_list = courses.get(field, {}).get(year, {}).get(semester, [])
            file_menu_keyboard = [
                [InlineKeyboardButton(course["name"], callback_data=f"course|{field}|{year}|{semester}|{idx}")]
                for idx, course in enumerate(course_list)
            ]
            file_menu_keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=f"select_year|{field}|{year}")])
            file_menu_markup = InlineKeyboardMarkup(file_menu_keyboard)
            await query.message.reply_text(
                f"Select course for {field} - {year} - {semester}:",
                reply_markup=file_menu_markup
            )
            return
        else:
            if files:
                keyboard = [
                    [InlineKeyboardButton(f.get("title", "File"), callback_data=f"file|{field}|{year}|{semester}|{idx}|{fidx}")]
                    for fidx, f in enumerate(files)
                ]
                keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=f"semester|{field}|{year}|{semester}")])
                text = f"Choose a file for {course['name']}:"
                markup = InlineKeyboardMarkup(keyboard)
                if not is_same_message(query.message, text, markup):
                    await query.edit_message_text(text, reply_markup=markup)
            else:
                keyboard = [
                    [InlineKeyboardButton("🔙 Back", callback_data=f"semester|{field}|{year}|{semester}")]
                ]
                text = "No files available for this course."
                markup = InlineKeyboardMarkup(keyboard)
                if not is_same_message(query.message, text, markup):
                    await query.edit_message_text(text, reply_markup=markup)

    elif data[0] == "file":
        field, year, semester, idx, fidx = data[1], data[2], data[3], int(data[4]), int(data[5])
        course = courses.get(field, {}).get(year, {}).get(semester, [])[idx]
        file = course.get("files", [])[fidx]
        file_id = file.get("file_id")
        url = file.get("url")
        if file_id:
            await query.message.reply_document(
                file_id,
                protect_content=True
            )
        elif url:
            await query.message.reply_text(f"{file.get('title', '')}: {url}")
        else:
            await query.message.reply_text("Sorry, this file is not available.")
        # After sending, show file menu again (so files appear above)
        files = course.get("files", [])
        keyboard = [
            [InlineKeyboardButton(f.get("title", "File"), callback_data=f"file|{field}|{year}|{semester}|{idx}|{fidx2}")]
            for fidx2, f in enumerate(files)
        ]
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=f"course|{field}|{year}|{semester}|{idx}")])
        text = f"Choose a file for {course['name']}:"
        markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(text, reply_markup=markup)

    elif data[0] == "back_to_main":
        keyboard = [
            [InlineKeyboardButton(field, callback_data=f"field|{field}")]
            for field in MAIN_FIELDS
        ]
        markup = InlineKeyboardMarkup(keyboard)
        if not is_same_message(query.message, WELCOME_TEXT, markup):
            await query.edit_message_text(WELCOME_TEXT, reply_markup=markup)

# ========== DOCUMENT HANDLER TO PRINT file_id ==========
async def doc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.document:
        file_id = update.message.document.file_id
        print(f"file_id: {file_id}")
        await update.message.reply_text(
            f"Received! file_id printed to console:\n{file_id}"
        )

# ========== MAIN ==========
def main():
    try:
        start_web_server()
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button))
        app.add_handler(MessageHandler(filters.Document.ALL, doc_handler))
        logger.info("Bot is running...")
        app.run_polling()
    except Conflict as e:
        logger.error("Another instance of the bot is already running. Please stop it before starting a new one.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
