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

# You do NOT need aiohttp/web server for polling mode on Render as a Background Worker.

BOT_TOKEN = "7969720988:AAHexLCWd8yMmQM7NiMyPhOmyCJ61fOXDwY"
CHANNEL_USERNAME = "sample_123456"  # No @
CHANNEL_ID = -1002659845054

MAIN_FIELDS = [
    "Economics", "Gender", "Psychology", "Accounting", "Managment",
    "PADM", "Sociology", "Journalism", "Hotel & Tourism Management"
]
YEARS = ["1 year", "2 year", "3 year"]
SEMESTERS = ["1 semester", "2 semester"]

def is_same_message(message, new_text, new_reply_markup):
    current_text = message.text or ""
    current_markup = message.reply_markup
    return (current_text == (new_text or "")) and (current_markup == new_reply_markup)

def make_centered_big_buttons(rows, back_callback=None):
    # 1 button per row, visually "bigger" with EM SPACE for width
    keyboard = [[InlineKeyboardButton(f"        {text}        ", callback_data=callback)] for text, callback in rows]
    if back_callback:
        keyboard.append([InlineKeyboardButton("        🔙 Back        ", callback_data=back_callback)])
    return InlineKeyboardMarkup(keyboard)

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
                        {"file_id": "BQACAgQAAxkBAAIBD2hZBmDMyIH9XkQhmXxeypNkYLkMAALgFgACAvDIUtsihO9VRhHeNgQ"},
                        {"file_id": "BQACAgQAAxkBAAIBEGhZBmDxZAPjdNnJ6T91cW6qs3qzAALhFgACAvDIUoM_a7ntjMW3NgQ"},
                        {"file_id": "BQACAgQAAxkBAAIBEWhZBmBFNDzyCgdcqXUkVEYrwhdBAALiFgACAvDIUtMv-EeSTSoPNgQ"},
                        {"file_id": "BQACAgQAAxkBAAIBEmhZBmDmiuOlJnIwF5oXC6seoAABHgAC4xYAAgLwyFK6NIdjWRBqgTYE"},
                        {"file_id": "BQACAgQAAxkBAAIBE2hZBmD0eV7kBJAfQDWeyIF7WrDBAALkFgACAvDIUn-VROTRFzCTNgQ"},
                        {"file_id": "BQACAgQAAxkBAAIBFGhZBmBxJATDi9CSGtc41IC_2MBWAALlFgACAvDIUr1Lc8-h9dUpNgQ"},
                        {"file_id": "BQACAgQAAxkBAAIBFWhZBmBxTaKe-jK-0g964Z2mCqoGAALmFgACAvDIUlOksdz9ddQdNgQ"},
                        {"file_id": "BQACAgQAAxkBAAIBFmhZBmBvjH6sYYrsGzILz0CNBGAEAALnFgACAvDIUizGebp3PbgNNgQ"},
                        {"file_id": "BQACAgQAAxkBAAIBF2hZBmCvvdQ2c_JSPGmNInO5zvn1AALoFgACAvDIUhX9FL6SQ9gyNgQ"}
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

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def is_user_member(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.warning(f"Failed to check membership: {e}")
        return False

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
    field_rows = [(field, f"field|{field}") for field in MAIN_FIELDS]
    await update.message.reply_text("Select your field:", reply_markup=make_centered_big_buttons(field_rows))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    join_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Join our channel", url=f"https://t.me/{CHANNEL_USERNAME}")],
        [InlineKeyboardButton("✅ I have joined", callback_data="check_membership")]
    ])

    if query.data == "check_membership":
        if not await is_user_member(user_id, context):
            if not is_same_message(query.message, "You are still not a member of the channel. Please join and try again!", join_button):
                await query.edit_message_text(
                    "You are still not a member of the channel. Please join and try again!",
                    reply_markup=join_button
                )
            return
        field_rows = [(field, f"field|{field}") for field in MAIN_FIELDS]
        markup = make_centered_big_buttons(field_rows)
        if not is_same_message(query.message, "Select your field:", markup):
            await query.edit_message_text("Select your field:", reply_markup=markup)
        return

    if not await is_user_member(user_id, context):
        if not is_same_message(query.message, "Please join our channel to access the bot!", join_button):
            await query.edit_message_text(
                "Please join our channel to access the bot!", reply_markup=join_button
            )
        return

    data = query.data.split("|")
    if data[0] == "field":
        field = data[1]
        year_rows = [(year, f"select_year|{field}|{year}") for year in YEARS]
        markup = make_centered_big_buttons(year_rows, back_callback="back_to_main")
        text = f"Select year for {field}:"
        if not is_same_message(query.message, text, markup):
            await query.edit_message_text(text, reply_markup=markup)

    elif data[0] == "year":
        year = data[1]
        field_rows = [(field, f"select_year|{field}|{year}") for field in MAIN_FIELDS]
        markup = make_centered_big_buttons(field_rows, back_callback="back_to_main")
        text = f"Select field for {year}:"
        if not is_same_message(query.message, text, markup):
            await query.edit_message_text(text, reply_markup=markup)

    elif data[0] == "select_year":
        field, year = data[1], data[2]
        semesters = list(courses.get(field, {}).get(year, {}).keys())
        sem_rows = [(sem, f"semester|{field}|{year}|{sem}") for sem in semesters]
        markup = make_centered_big_buttons(sem_rows, back_callback=f"field|{field}")
        text = f"Select semester for {field} - {year}:"
        if not is_same_message(query.message, text, markup):
            await query.edit_message_text(text, reply_markup=markup)

    elif data[0] == "semester":
        field, year, semester = data[1], data[2], data[3]
        course_list = courses.get(field, {}).get(year, {}).get(semester, [])
        course_rows = [(course["name"], f"course|{field}|{year}|{semester}|{idx}") for idx, course in enumerate(course_list)]
        markup = make_centered_big_buttons(course_rows, back_callback=f"select_year|{field}|{year}")
        text = f"Select course for {field} - {year} - {semester}:"
        if not is_same_message(query.message, text, markup):
            await query.edit_message_text(text, reply_markup=markup)

    elif data[0] == "course":
        field, year, semester, idx = data[1], data[2], data[3], int(data[4])
        course = courses.get(field, {}).get(year, {}).get(semester, [])[idx]
        files = course.get("files", [])
        try:
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        except Exception as e:
            logger.warning(f"Failed to delete menu message: {e}")
        if course["name"] == "Calculus for Economics" and len(files) == 2 and all("file_id" in f for f in files):
            for f in files:
                file_id = f.get("file_id")
                if file_id:
                    await context.bot.send_document(
                        chat_id=query.message.chat_id,
                        document=file_id,
                        protect_content=True
                    )
            markup = make_centered_big_buttons([], back_callback=f"semester|{field}|{year}|{semester}")
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="Choose what to do next:",
                reply_markup=markup
            )
            return
        else:
            if files:
                file_rows = [
                    (f.get("title", "File"), f"file|{field}|{year}|{semester}|{idx}|{fidx}")
                    for fidx, f in enumerate(files)
                ]
                markup = make_centered_big_buttons(file_rows, back_callback=f"semester|{field}|{year}|{semester}")
                text = f"Choose a file for {course['name']}:"
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=text,
                    reply_markup=markup
                )
            else:
                markup = make_centered_big_buttons([], back_callback=f"semester|{field}|{year}|{semester}")
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text="No files available for this course.",
                    reply_markup=markup
                )

    elif data[0] == "file":
        field, year, semester, idx, fidx = data[1], data[2], data[3], int(data[4]), int(data[5])
        course = courses.get(field, {}).get(year, {}).get(semester, [])[idx]
        file = course.get("files", [])[fidx]
        file_id = file.get("file_id")
        url = file.get("url")
        try:
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        except Exception as e:
            logger.warning(f"Failed to delete menu message: {e}")
        if file_id:
            await context.bot.send_document(
                chat_id=query.message.chat_id,
                document=file_id,
                protect_content=True
            )
        elif url:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"{file.get('title', '')}: {url}"
            )
        else:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="Sorry, this file is not available."
            )
        markup = make_centered_big_buttons([], back_callback=f"course|{field}|{year}|{semester}|{idx}")
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Choose what to do next:",
            reply_markup=markup
        )

    elif data[0] == "back_to_main":
        try:
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        except Exception as e:
            logger.warning(f"Failed to delete select year message: {e}")
        field_rows = [(field, f"field|{field}") for field in MAIN_FIELDS]
        markup = make_centered_big_buttons(field_rows)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Select your field:",
            reply_markup=markup
        )

async def doc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.document:
        file_id = update.message.document.file_id
        print(f"file_id: {file_id}")
        await update.message.reply_text(
            f"Received! file_id printed to console:\n{file_id}"
        )

def main():
    try:
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
