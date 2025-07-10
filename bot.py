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
import json
from datetime import datetime

# --- Flask Web Server for Render Port Requirement ---
from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def health():
    return "OK", 200

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
# ---------------------------------------------------

BOT_TOKEN = "7969720988:AAHexLCWd8yMmQM7NiMyPhOmyCJ61fOXDwY"
CHANNEL_USERNAME = "HUESAchannel"  # No @
CHANNEL_ID = -1002040479523
ADMIN_USER_ID = 1952017668  # Your admin user ID

# File to store user data
USERS_FILE = "users.json"

# Initialize user storage
def load_users():
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"Error loading users: {e}")
        return {}

def save_users(users_data):
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users_data, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving users: {e}")

def add_user(user_id, username=None, first_name=None, last_name=None):
    users_data = load_users()
    if str(user_id) not in users_data:
        users_data[str(user_id)] = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "joined_date": datetime.now().isoformat(),
            "last_interaction": datetime.now().isoformat()
        }
        save_users(users_data)
        return True  # New user
    else:
        # Update last interaction
        users_data[str(user_id)]["last_interaction"] = datetime.now().isoformat()
        if username:
            users_data[str(user_id)]["username"] = username
        if first_name:
            users_data[str(user_id)]["first_name"] = first_name
        if last_name:
            users_data[str(user_id)]["last_name"] = last_name
        save_users(users_data)
        return False  # Existing user

def get_user_count():
    users_data = load_users()
    return len(users_data)

def get_all_user_ids():
    users_data = load_users()
    return [int(uid) for uid in users_data.keys()]

MAIN_FIELDS = [
    "Economics", "Gender", "Psychology", "Accounting", "Managment",
    "PADM", "Sociology", "Journalism", "Hotel & Tourism Management"
]
YEARS = ["2 year", "3 year", "4 year"]
SEMESTERS = ["1 semester", "2 semester"]

def is_same_message(message, new_text, new_reply_markup):
    current_text = message.text or ""
    current_markup = message.reply_markup
    return (current_text == (new_text or "")) and (current_markup == new_reply_markup)

# Updated make_centered_big_buttons to handle text overflow, blank buttons, and improved left-corner positioning
def make_centered_big_buttons(rows, back_callback=None, max_length=50, include_feedback=False):
    keyboard = []
    for text, callback in rows:
        display_text = text
        if not text.strip():
            display_text = "Coming soon!"
            callback = "coming_soon"
        else:
            # Truncate text if too long, but keep readable
            if len(text) > max_length:
                display_text = text[:max_length - 4] + "…"
        # Create buttons with left alignment for better fit
        keyboard.append([InlineKeyboardButton(f"📋 {display_text}", callback_data=callback)])
    
    # Add navigation and feedback buttons in a separate row for better corner positioning
    bottom_row = []
    if back_callback:
        bottom_row.append(InlineKeyboardButton("🔙 Back", callback_data=back_callback))
    if include_feedback:
        bottom_row.append(InlineKeyboardButton("💬 Feedback", callback_data="request_feedback"))
    
    if bottom_row:
        keyboard.append(bottom_row)
    
    return InlineKeyboardMarkup(keyboard)

courses = {
    "Economics": {
        "2 year": {
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
                        {"file_id": "BQACAgQAAxkBAAIByWhZn4PR-6a680joi0B3Aoz2bCbcAALcFwACAvDIUsqkj9_BXNpkNgQ"},
                        {"file_id": "BQACAgQAAxkBAAIBymhZn4PeIFppRYXYxUVEGYKaT_vGAALdFwACAvDIUsrlKC0k_7_HNgQ"},
                        {"file_id": "BQACAgQAAxkBAAIBy2hZn4Osn3iEPL1jwCiPZKna93ptAALeFwACAvDIUjOQsNfACtODNgQ"},
                        {"file_id": "BQACAgQAAxkBAAIBzGhZn4N_tqaFzqknoNl9v8qrA_HJAALfFwACAvDIUqJDGuXE5Nz1NgQ"},
                        {"file_id": "BQACAgQAAxkBAAIBzWhZn4PmmUKEpzM8ZJZ9zT9PgyexAALgFwACAvDIUqsW5LWBMWABNgQ"},
                        {"file_id": "BQACAgQAAxkBAAIBzmhZn4Pe_gSxz01JYyu8HGQeaOb5AALhFwACAvDIUrq-1e_01erdNgQ"},
                        {"file_id": "BQACAgQAAxkBAAIBz2hZn4N634WfAUJUpq4Y_--KKp2sAALiFwACAvDIUs228owIljvVNgQ"},
                        {"file_id": "BQACAgQAAxkBAAIB0GhZn4Nhz7wsoE2XAxiR68PbmgoaAALjFwACAvDIUi4AAc67BlBtOjYE"},
                        {"file_id": "BQACAgQAAxkBAAIB0WhZn4PlgtyYrY2G0ech4UCP5ZjDAALkFwACAvDIUvbZpImnYI4yNgQ"},
                        {"file_id": "BQACAgQAAxkBAAIB0mhZn4MuMEdd-anR-Wl5IFWAc4AOAALlFwACAvDIUmOZJ_Rlg7PZNgQ"},
                        {"file_id": "BQACAgQAAxkBAAIB3WhZn4rIWIwKvteA1S4OD-jkSz8vAALmFwACAvDIUqeLLt8SfX9qNgQ"}
                    ]
                },
                {
                    "name": "Micro Economics 1",
                    "files": [
                        {"file_id": "BQACAgQAAxkBAAIB32hZoWvm6QhsxWnO8LC6aUVXNJ3nAALnFwACAvDIUutmFpX7hhoQNgQ"},
                        {"file_id": "BQACAgQAAxkBAAIB4GhZoWtrckPrkYfmJPrwTcSwot0FAALoFwACAvDIUm9ARP7GFhPfNgQ"},
                        {"file_id": "BQACAgQAAxkBAAIB4WhZoWv2PPbReP08Cb4WpDGMT5zpAALpFwACAvDIUiwqqXZjMmXQNgQ"},
                        {"file_id": "BQACAgQAAIB4mhZoWtmgPYMCvg9TztJXtkVEHkKAALqFwACAvDIUrYpYhEaiAO9NgQ"},
                        {"file_id": "BQACAgQAAIB42hZoWspeWj2rsL93KIIjCn05eaNAALrFwACAvDIUmFJzI88Bn5LNgQ"},
                        {"file_id": "BQACAgQAAIB5GhZoWsge3pr2cvARP8wiAOQZPcaAALsFwACAvDIUthRNbMSa8kvNgQ"},
                        {"file_id": "BQACAgQAAIB5WhZoWuXvimgHEEsMCm5dgQH2kcMAALtFwACAvDIUgbjsEi83uQTNgQ"}
                    ]
                },
                {
                    "name": "Introduction to Statistics",
                    "files": [
                        {"file_id": "BQACAgQAAxkBAAIB72hZo_uvtzHZAAI_swRRf9w4GNpcAALzFwACAvDIUjegO6N8lW5KNgQ"},
                        {"file_id": "BQACAgQAAIB8GhZo_vIzcjLjG89xW_tS3RddSoJAAL0FwACAvDIUntqyRXdCF6MNgQ"}
                    ]
                },
                {
                    "name": "Basic Computer Skill of MS Applications",
                    "files": [
                        {"file_id": "BQACAgQAAxkBAAIB_GhZqBF6uStb8p5Kp_7teinNgzkQAAL2FwACAvDIUhcHgVaUC6vcNgQ"},
                        {"file_id": "BQACAgQAAIB_WhZqBEOLQq8Wywr4iXbfFWZcG27AAL3FwACAvDIUjww2Evy6-LrNgQ"},
                        {"file_id": "BQACAgQAAIB_mhZqBHMbgxzBgRLztXuOa9DXdMCAAL4FwACAvDIUtN127nEa3BdNgQ"}
                    ]
                }
            ],
            "2 semester": [
                {
                    "name": "Linear Algebra for Economics",
                    "files": [
                        {"file_id": "BQACAgQAAICpWhZtCi-BC7w-UPDPa-wvJK_ObJRAAMYAAIC8MhSD1s-R5ltZc82BA"},
                        {"file_id": "BQACAgQAAICpmhZtCgMZRWCs5DRR-wC9ZVLa7uiAAIBGAACAvDIUsGvKqPwj9x_NgQ"},
                        {"file_id": "BQACAgQAAICp2hZtCgDhrQthEnQBnGLNumDbftgAAIDGAACAvDIUthVIzX1Qqe3NgQ"},
                        {"file_id": "BQACAgQAAICqGhZtCj1B43-4zKlUcmw8G7I6tCFAAICGAACAvDIUntoEf5o5LeENgQ"},
                        {"file_id": "BQACAgQAAICqWhZtCgdEWW72I6iH1FHCfAgfb8HAAIEGAACAvDIUpkGeBqAPB2_NgQ"},
                        {"file_id": "BQACAgQAAICqmhZtCh8tkqq5Yaa7hpoNAABMzNhrAACBRgAAgLwyFIrL6EM7_3jCzYE"},
                        {"file_id": "BQACAgQAAICq2hZtCjzNMXBKbE_HU4bbcNwTCOCAAIGGAACAvDIUvVrW4flTDk2NgQ"},
                        {"file_id": "BQACAgQAAICrGhZtCi6LzwtGpEzq6LXjLzzlFVIAAIIGAACAvDIUoYpV99wd_KyNgQ"},
                        {"file_id": "BQACAgQAAICrWhZtCgfdR7e5_YDPRP6fPoY1JxCAAIJGAACAvDIUsNuRy0UmbHnNgQ"}
                    ]
                },
                {
                    "name": "Accounting 2",
                    "files": [
                        {"file_id": "BQACAgQAAICt2hZtKp835jnDdaAp_UqkN20zxuXAAIKGAACAvDIUv2c5kRuqqNnNgQ"},
                        {"file_id": "BQACAgQAAICuGhZtKo_qHKS-rBPbYs-UpKh9ylCAAILGAACAvDIUh0Nzuq0mPwONgQ"},
                        {"file_id": "BQACAgQAAICuWhZtKpujcb27-7GN-rsFwy1M-d-AAIMGAACAvDIUhU8Jjya_25rNgQ"},
                        {"file_id": "BQACAgQAAICumhZtKq9nDukHeMkZ6OyeH07OfF3AAINGAACAvDIUvZpUpMniBXGNgQ"},
                        {"file_id": "BQACAgQAAICu2hZtKr1Kd4of8q1xDRRbFHGA3eSAAIOGAACAvDIUpCutJF2ztGbNgQ"},
                        {"file_id": "BQACAgQAAICvGhZtKqPuaY5Vjo7XA3NF_Q3dUpjAAIPGAACAvDIUph7RdNcIV4SNgQ"},
                        {"file_id": "BQACAgQAAICvWhZtKoG2GYqOvmYB6BHd1w0XwbdAAIQGAACAvDIUj2VWfOIO9weNgQ"}
                    ]
                },
                {
                    "name": "Macro Economics 2",
                    "files": [
                        {"file_id": "BQACAgQAAICxWhZtVoqzMQOEQ6hSI5463Zt4-YTAAIRGAACAvDIUs_rWIC4UrlhNgQ"},
                        {"file_id": "BQACAgQAAICxmhZtVpZvfszTcfQgNrQqZ4l0InwAAISGAACAvDIUjGvE1HgF-h6NgQ"},
                        {"file_id": "BQACAgQAAICx2hZtVqjPqriD3LTxD4klxElJQSJAAITGAACAvDIUifxu8bQprJpNgQ"}
                    ]
                },
                {
                    "name": "Micro Economics 2",
                    "files": [
                        {"file_id": "BQACAgQAAICy2hZtea6pN1CL5tWWmsUt-35gGhgAAIUGAACAvDIUi_lopYn4m7VNgQ"},
                        {"file_id": "BQACAgQAAICzGhZteaE9nwVEqBJHsgwFTBlPAiNAAIVGAACAvDIUqBJCxTzGAyPNgQ"},
                        {"file_id": "BQACAgQAAICzWhZtebZdw87_2Lo9nkGDCmoFCjvAAIWGAACAvDIUkgaSRbw6PLDNgQ"},
                        {"file_id": "BQACAgQAAICzmhZteZuFVPhQSa2YgofFo5bzeqoAAIXGAACAvDIUpzv8NUaoadmNgQ"},
                        {"file_id": "BQACAgQAAICz2hZteYRf78bXkZ6QuS4QkGAV4jlAAIYGAACAvDIUj8YDeqQXXsiNgQ"}
                    ]
                },
                {
                    "name": "Statistics for Economics",
                    "files": [
                        {"file_id": "BQACAgQAAIC1WhZtjY3UnlPzqJCzGTQ22hiqes3AALeGAACFaJBUfgkRvllkdxVNgQ"},
                        {"file_id": "BQACAgQAAIC1mhZtjYHP1Jt7Bhe-WdJUvrmlXolAALfGAACFaJBUT_W86L5NWyxNgQ"}
                    ]
                },
                {
                    "name": "Basic Writing Skill",
                    "files": [
                        {"file_id": "BQACAgQAAIC2WhZtqxpTOh-qhGKstxWro48RtUnAAIzCgACXBrYUmbTAuHahzXJNgQ"}
                    ]
                }
            ]
        },
        "3 year": {
            "1 semester": [
                {
                    "name": "Mathematical Economics",
                    "files": [
                        {"file_id": "BQACAgQAAIDBWhZvM8eClDFYgo7CPDkJxQhP7kXAAJ5FgACDtQgU0w8DeCP0seINgQ"},
                        {"file_id": "BQACAgQAAIDBmhZvM95-qZflBrfHdJrS2q5sRyaAAL4DgAC1LGgUhlSv4Fttk4JNgQ"},
                        {"file_id": "BQACAgQAAIDB2hZvM_HWjS8UpbAPyuQF3iotta5AAIOFgACVDwwU1lX7F-M15fENgQ"},
                        {"file_id": "BQACAgQAAIDCGhZvM8CWyqpoo5W80qrtvBIOwAB7wACDhgAAreaCVIadiY-n2rpODYE"},
                        {"file_id": "BQACAgQAAIDCWhZvM_zaMTKPn5ipiT-MY4U01YWAAICFwAC91mhUfRvxlhsi09pNgQ"},
                        {"file_id": "BQACAgQAAIDCmhZvM8feg3lFo6yYEAG8K_YbleFAAI9HQACw08YUUpQkVBlvMdENgQ"},
                        {"file_id": "BQACAgQAAIDC2hZvM9Rth5Kr01efUhEKRPWzoULAAIOGQACV-1oUOak6Nt2npK-NgQ"},
                        {"file_id": "BQACAgQAAIDDGhZvM8XmOGkWYVJnrQCc20KjR3-AAKXHAAC_8IoUpHbVLM-Bu7hNgQ"},
                        {"file_id": "BQACAgQAAIDDWhZvM_WEjweAAGngqPO4hCEURmLYwACPhcAAqkI6FJ0c83JNr2KkzYE"}
                    ]
                },
                {
                    "name": "Econometrics 1",
                    "files": [
                        {"file_id": "BQACAgQAAIDF2hZvUInOerbVn7SXOKc7fuX_VrSAAJ1FgACDtQgU1cxMgTEGThoNgQ"},
                        {"file_id": "BQACAgQAAIDGGhZvUILG5AZs9OheBAk-m9GbFPFAAKAFgACDtQgU-FlxpoRl1oUNgQ"},
                        {"file_id": "BQACAgQAAIDGWhZvUKqMBOQ7hRQbOhAtnQ1vnBnAAMTAAIfJ1FT86d9Knfy2Bc2BA"},
                        {"file_id": "BQACAgQAAIDGmhZvUJ309hYE82GXyLPQCexS4nvAAJrEwACmRqYUxrkuQUdY3apNgQ"},
                        {"file_id": "BQACAgQAAIDG2hZvUJ2eXBk9mzOLi5aNwGcaK_QAAIHEwACjMXpUWyMm8hFPBekNgQ"},
                        {"file_id": "BQACAgQAAIDHGhZvUKko638mBbQukgCgoYiSoTwAAJREwACjMXpUSs2c5B7Sd7fNgQ"},
                        {"file_id": "BQACAgQAAIDHWhZvUKGKKpCDgHApN_ErOrzrdm3AAIKGAACt5oJUnyuqySQVSPUNgQ"},
                        {"file_id": "BQACAgQAAIDHmhZvUJSKgVDUslymGRLpLGWMq7pAAL7FgAC91mhUXQ4q4a-7_vlNgQ"},
                        {"file_id": "BQACAgQAAIDH2hZvUKPaauUqRhLAAGe1VUFhUPlFAACPB0AAsNPGFF5KQnANEgOJjYE"},
                        {"file_id": "BQACAgQAAIDIGhZvUKBJvQFO3QIX1aLPn7S1rhZAAIoFwAC8HbwU-DYW5jyfm4-NgQ"},
                        {"file_id": "BQACAgQAAIDIWhZvUJgGBf8-OSVORXLFsXH9v7bAAK2FgACAcc4UCbqEZtmVuPXNgQ"},
                        {"file_id": "BQACAgQAAIDImhZvULzYto6ZqXwHOJijdOugg8QAAJfFQACpZbpUBDnzCv8evI7NgQ"},
                        {"file_id": "BQACAgQAAIDI2hZvUJ3fwMh-RScgVIMNukro4CLAAJrLgACSyDQUT0xKqdNf7qDNgQ"},
                        {"file_id": "BQACAgQAAIDJGhZvUIvHT3pxRtKE6dgZLqzgSBGAAKKFAACS9ygUBKxlMGiXm63NgQ"}
                    ]
                },
                {
                    "name": "Financial Economics 1",
                    "files": [
                        {"file_id": "BQACAgQAAIDM2hZvaX3WtpOqL3xI40R8e8fy52-AAIgFQAClBwJU_B0VgKvZ-SdNgQ"},
                        {"file_id": "BQACAgQAAIDNGhZvaX__B6Zi4fPf8D7ERX3tI3vAAI7FgACDdUAAVAjYK4iNEsGJzYE"},
                        {"file_id": "BQACAgQAAIDNWhZvaXEs0VQ-V3v3uFxwvpdWE--AAIdEgACcGg5UTiN3rsgrIC_NgQ"},
                        {"file_id": "BQACAgQAAIDNmhZvaU67J_cxl6J-SQ3PF19AhS0AAIsEgACF4voURVxBD8b18v1NgQ"},
                        {"file_id": "BQACAgQAAIDN2hZvaWFSYi0OdrcoaPpUTQhM_7dAAKeFQACSSKRUVN6BdNZlfnJNgQ"},
                        {"file_id": "BQACAgQAAIDOGhZvaX4FNpjoBZIiYEQ4X99MXOkAAJ0FQACnighUmTBoOsK6Qz2NgQ"},
                        {"file_id": "BQACAgQAAIDOmhZvaXvUszh0zUopOSpuCj3sTVUAAJ1FQACnighUonU6bcSmd2ENgQ"},
                        {"file_id": "BQACAgQAAIDOmhZvaWcdPE7rxnhbBHIR10DZddMAAJ2FQACnighUkk3Z-4Emo1QNgQ"},
                        {"file_id": "BQACAgQAAIDOmhZvaWRvYxYtgTAHOP4kiQZuBFzAAJ4FQACnighUvLtr5oah9gNNgQ"}
                    ]
                },
                {
                    "name": "Introduction to Management",
                    "files": [
                        {"file_id": "BQACAgQAAIDRWhZvgnFRmnycqh46TRggA6fDytqAAJ7EQACH8GAU153-r8JRyfBNgQ"},
                        {"file_id": "BQACAgQAAIDRmhZvglxxFgJ6Gl2pQ5tg7RHpdEGAAKAEAACxWlwUKdlY3XWQUQ8NgQ"},
                        {"file_id": "BQACAgQAAIDR2hZvgn33IiWzolDWXgRsnkLE8OaAAKBEAACxWlwUD5i4VG9o6ASNgQ"},
                        {"file_id": "BQACAgQAAIDSGhZvgmpBZzAkem8HyiGHHPDJA7SAALpEQACfwABcFHjEMehOv7i8TYE"},
                        {"file_id": "BQACAgQAAIDSWhZvgklTodRo1-5Mm5x7QysSbWnAAIlGAACcQ6xUGqhVdRgLPLENgQ"},
                        {"file_id": "BQACAgQAAIDSmhZvgkomD0RVFG2Jz8yUWHD8qsOAAL0GAACoOgZUqLA5mXpc5tnNgQ"}
                    ]
                },
                {
                    "name": "Labor Economics",
                    "files": [
                        {"file_id": "BQACAgQAAIDUWhZvm6xLG9VnV9JF8kJy3U7IuGYAAJ6FgACDtQgU1kzFjXs6ce0NgQ"},
                        {"file_id": "BQACAgQAAIDUmhZvm56JFe-vypIQQ5L2rMcIauUAAK5FAACtG8AAVOaheGQEkCP5zYE"},
                        {"file_id": "BQACAgQAAIDU2hZvm7goqj5OKXLLvUAAcWcW77POQACuhQAArRvAAFTfZrGF1M9ZbM2BA"},
                        {"file_id": "BQACAgQAAIDVGhZvm4BVZG-_Oefg9wjFWE9KjS0AAK7FAACtG8AAVPRSYwg50lSRzYE"},
                        {"file_id": "BQACAgQAAIDVWhZvm7rpgjJlI8AAfwBOBxEqPhhegACPhMAAkoIkFPvwtisEhSrejYE"},
                        {"file_id": "BQACAgQAAIDVmhZvm4AAUhI2rnfpiIVNxaAGTKIlgAC6RcAAtOGwVNCsTD5OArT1zYE"},
                        {"file_id": "BQACAgQAAIDV2hZvm7DBEiVPpkqssCX0Sh5wLZHAALqFwAC04bBU_p2VLfjDjDjNgQ"},
                        {"file_id": "BQACAgQAAIDWGhZvm5VYblel7BZOPg-dTq3_xI9AALsFwAC04bBU4M2eHdIzOLCNgQ"},
                        {"file_id": "BQACAgQAAIDWWhZvm6e_6mGBsjI5_SKG2Pn2rM2AAJTGwACDgfhU88bEt7ga_16NgQ"},
                        {"file_id": "BQACAgQAAIDWmhZvm73GDhLhRKmZ75ejrKRfjlmAAJUGwACDgfhUxAcbzRBf_VzNgQ"},
                        {"file_id": "BQACAgQAAIDW2hZvm4524-Xk8MK06Pc790vrFoqAAJVGwACDgfhU-Fn76pyiAxRNgQ"},
                        {"file_id": "BQACAgQAAIDXGhZvm6kDbrCtEaEopdLohuip3zYAAJWGwACDgfhU_AR63zRVyXVNgQ"},
                        {"file_id": "BQACAgQAAIDXWhZvm5gKotHQjmmeMjUSy4TgP0IAAKGFgACipsBUAtU8HE5leWrNgQ"},
                        {"file_id": "BQACAgQAAIDXmhZvm7OoatRMt6-181_Gf3MDQjMAAJnGAACPdphUXdNJRDL6emnNgQ"},
                        {"file_id": "BQACAgQAAIDX2hZvm5g9Yd6oV5n-pfwQrgk2kOOAAJuGAACPdphUUKvpbzoywW6NgQ"},
                        {"file_id": "BQACAgQAAIDYGhZvm5UuyktKIyMCo6opYY0dpKEAAK7FgACUXeoUSHZRETHB6FDNgQ"},
                        {"file_id": "BQACAgQAAIDYWhZvm7XVnx7bS9uVTqGwF9j9bGnAALSFgACjse4UTh9TF0i4gXBNgQ"},
                        {"file_id": "BQACAgQAAIDYmhZvm7PVf9AYmg1pd8NZGFaH8DbAAIMFgACjsfAUYcEL8ci1mRZNgQ"},
                        {"file_id": "BQACAgQAAIDY2hZvm6eKHevOBqkcKR7066G_J3ZAAKrGAACiMTAUVoLediyfDcpNgQ"}
                    ]
                },
                {
                    "name": "Developmental Economics 1",
                    "files": [
                        {"file_id": "BQACAgQAAIDd2hZvtdSln3q0KU7Ph7gMIrD9UVRAAIIEwACK3thUDjb8ByVuSyuNgQ"},
                        {"file_id": "BQACAgQAAIDeGhZvtdhheTLeaKd8yLc0ygWS2LzAALLDQACMu_ZU7HZHaeihLddNgQ"},
                        {"file_id": "BQACAgQAAIDeWhZvtdpLdl_Q0gmyjslUoUZ3DkjAAKBGAACLcqZU-G0orjJdxZ_NgQ"},
                        {"file_id": "BQACAgQAAIDemhZvtc6vgOUlmBbKtc2IxZSzJTlAAIQFgACVDwwUwpg0rHbzE4SNgQ"},
                        {"file_id": "BQACAgQAAIDe2hZvtfolo3Mi5d1yHG7Vp2-q4vXAAIVFwAC91mhUXoWZHh8enspNgQ"},
                        {"file_id": "BQACAgQAAIDfGhZvtelL7dGmmMRa1ATXnIPedfDAALWFAACmXB4UDgC38n9zCe0NgQ"},
                        {"file_id": "BQACAgQAAIDfWhZvtclzUQx1iEmT1fcZ9SnOiVZAAJSEQACPcaxUvmUjEhrpIXwNgQ"},
                        {"file_id": "BQACAgQAAIDfmhZvtd3zjY2q-5RT1IGKxdeIwToAAJbEAAC92j4UiPocX-E4ZgGNgQ"},
                        {"file_id": "BQACAgQAAIDf2hZvtcLTq2q3ziWYHZv_y2EJKoJAAJ2FwACGTUhUGE92roWUGf_NgQ"},
                        {"file_id": "BQACAgQAAIDgGhZvtfpRqmTY6olSOOG11oviWvBAAJ3FwACGTUhUI9MCU5wjMNxNgQ"},
                        {"file_id": "BQACAgQAAIDgWhZvtf4JAf3NAalDbSl1w1Lro7zAAJ4FwACGTUhUGF3baAZCAPmNgQ"},
                        {"file_id": "BQACAgQAAIDgmhZvtcKfGOn7OJ-tSBQQhQ4YIobAAJQFQAC1HbIUeKAzFZZ-qr_NgQ"},
                        {"file_id": "BQACAgQAAIDg2hZvteluogiir6HJybDUsNwxUjAAAJRFQAC1HbIUbE_4HFDKM8MNgQ"},
                        {"file_id": "BQACAgQAAIDhGhZvtda-b82JEzHMrJa5RSrGjwdAAJSFQAC1HbIUYZMZwThIOt8NgQ"}
                    ]
                },
                {
                    "name": "International Economics 1",
                    "files": [
                        {"file_id": "BQACAgQAAIDk2hZvz5DUmmLkiL1Jh6w0jNt8hGRAAJ7FgACDtQgU8bthk47hey4NgQ"},
                        {"file_id": "BQACAgQAAIDlGhZvz6Djyjz2FMAAc49OW679_bcFAACfBYAAg7UIFPYyrPcg8rSBjYE"},
                        {"file_id": "BQACAgQAAIDlWhZvz7ZKf7s1wFnmqAQ5DyqZaFgAAJ9FgACDtQgU44aPH4gX2vKNgQ"},
                        {"file_id": "BQACAgQAAIDlmhZvz5jS_yM-oI1V7Z9-HDcbjtuAAJQEQACZN1pUkZD-1Xj9c80NgQ"},
                        {"file_id": "BQACAgQAAIDl2hZvz6fJFqXDWX1VDYPi2Hpria0AAKuFAACOwPAUob7bgZIj7GuNgQ"},
                        {"file_id": "BQACAgQAAIDmGhZvz6opelmI3VsK13AbbTkqbCkAAJMEAACVMGgU7UHsAxBZdxENgQ"},
                        {"file_id": "BQACAgQAAIDmWhZvz7zPyYIUNot0LT7yn3SkX5lAAILFAACrOk5URaV2iLP-swsNgQ"},
                        {"file_id": "BQACAgQAAIDmmhZvz4bJPa54lYLAmUXySVL27MhAAIMFAACrOk5UT39SAQB4lSVNgQ"},
                        {"file_id": "BQACAgQAAIDm2hZvz6AJLMxs6G3b35sXgdKfmKDAAINFAACrOk5UUfAl5UhhnWnNgQ"},
                        {"file_id": "BQACAgQAAIDnGhZvz7vq4dWW5-cn2xWvkuzGFj4AALIFAACMLVhUxOtkjplMr6CNgQ"},
                        {"file_id": "BQACAgQAAIDnWhZvz4gTA2cCP1U6hE-SgABMNGlYwACyRQAAjC1YVOgpEFjjs8rbzYE"},
                        {"file_id": "BQACAgQAAIDnmhZvz5UoLGnMcI5qmNib6cRiHdIAALKFAACMLVhU3BcSxEKg9b9NgQ"},
                        {"file_id": "BQACAgQAAIDn2hZvz7epivJsNId6RZqb136TMCAAALLFAACMLVhU13b8BGsM8gCNgQ"},
                        {"file_id": "BQACAgQAAIDoGhZvz6tWQd6BhYSu5lGhzTTtSRCAALMFAACMLVhUyBfS67mXIvkNgQ"},
                        {"file_id": "BQACAgQAAIDoWhZvz5XEvZGdToGhJBNxqV2Sy4TAAILGAACt5oJUgHqAtakdpn-NgQ"},
                        {"file_id": "BQACAgQAAIDomhZvz5Ds442kwL-KD7bwmxh5HamAAIDFwAC91mhUeuN9_TWt5fhNgQ"},
                        {"file_id": "BQACAgQAAIDo2hZvz4YRrf0luyuZvcbll6X6OXHAAI-HQACw08YUbCH9JkrsPHLNgQ"},
                        {"file_id": "BQACAgQAAIDpGhZvz6kcqA4sDhyYE7ZMV07Qgo9AAI7HQACw08YUU3SFgU8jrZeNgQ"},
                        {"file_id": "BQACAgQAAIDpWhZvz6JJWUCEuhPHOizEibE_QX7AAKUEgACXApYU1-CTEym5nErNgQ"},
                        {"file_id": "BQACAgQAAIDpmhZvz4227zZ6GU_i-zzBAHaS7PqAAKVEgACXApYU2sAAQpG9exZAAE2BA"},
                        {"file_id": "BQACAgQAAIDp2hZvz4Y4k3rJt3UwLHhddHJlvAxAAJPEQACZN1pUl9imsaX-f3iNgQ"},
                        {"file_id": "BQACAgQAAIDqGhZvz7WBCjkIthsHYcyi0JkYZ8pAAIpFwACPk_wUy5S5NMvtF2UNgQ"},
                        {"file_id": "BQACAgQAAIDqWhZvz5kiwFlE78z00Mq5BPozVyiAAIqFwACPk_wU893uNWNjOMMNgQ"},
                        {"file_id": "BQACAgQAAIDqmhZvz58L1t5_aotS_PJ4p3LkRrdAAJAFwACbhBxUfOCYFBGjhvvNgQ"},
                        {"file_id": "BQACAgQAAIDq2hZvz6-FsZZtQmAKSWxj6_BmguPAALuGQAC7hJhUeBSw-YGhSefNgQ"}
                    ]
                }
            ],
            "2 semester": [
                {
                    "name": "Development economics 2",
                    "files": [
                        {"file_id": "BQACAgQAAIEEmhZ0GOSJyU0XYCcmV8fNArVsRUVAAJcGAACJ9_5UuanxdZp6feHNgQ"},
                        {"file_id": "BQACAgQAAIEE2hZ0GOMwhwvzl-drgqxFt_QZlXSAALaFwACky3BU5xTF8DpWESLNgQ"},
                        {"file_id": "BQACAgQAAIEFGhZ0GNRsC3rWbQ4fcZvXMTJmGDrAALbFwACky3BU2QlWxFJaEO-NgQ"},
                        {"file_id": "BQACAgQAAIEFWhZ0GMJ24-z-JMG2WhNJ-oW7-lqAALcFwACky3BU84v-FFtz1-iNgQ"},
                        {"file_id": "BQACAgQAAIEFmhZ0GM8RuJonlaYjepMsEt0LORhAALdFwACky3BU51-ZIFE_4I3NgQ"},
                        {"file_id": "BQACAgQAAIEF2hZ0GMdkexatNVOMsIyl9yx5RpKAALeFwACky3BU440OKj3vV1YNgQ"},
                        {"file_id": "BQACAgQAAIEGGhZ0GNKl-lR40c5dsI2OsaCZ_GoAALfFwACky3BU8HxwETSFzpKNgQ"},
                        {"file_id": "BQACAgQAAIEGWhZ0GNtxl-8SeR-qcT5LzTg5JSqAALhFwACky3BU-llX93ImwMXNgQ"}
                    ]
                },
                {
                    "name": "International economics 2",
                    "files": [
                        {"file_id": "BQACAgQAAIEImhZ0P_85VBP3K0cYWXpuHU8-e9HAALvFQACczUoU2IiKQABH2PGqjYE"},
                        {"file_id": "BQACAgQAAIEI2hZ0P-ohQKPqbMiEq_MP2bSWceOAALwFQACczUoU9NJZkzJ_jElNgQ"},
                        {"file_id": "BQACAgQAAIEJGhZ0P-CZ4dvWjJK1FhJnY_knoEmAALxFQACczUoU--BTBKKBIPVNgQ"},
                        {"file_id": "BQACAgQAAIEJWhZ0P85mxcS_L1qx2klAxHIwITkAALyFQACczUoU8pUrcNYNESENgQ"},
                        {"file_id": "BQACAgQAAIEJmhZ0P-TzRX3TsWCLxTQFB3j22LcAAJDGAAC4Hl4U2ilIxqNmc6YNgQ"},
                        {"file_id": "BQACAgQAAIEJ2hZ0P_3NjMdJvO0HGe8-ZrtIog6AAJEGAAC4Hl4U6Tue9BAFNl8NgQ"},
                        {"file_id": "BQACAgQAAIEKGhZ0P_k-SRJtRfgcLag7RkeO5KQAAIvFgACfq_JU-xjviIjR5NFNgQ"},
                        {"file_id": "BQACAgQAAIEKmhZ0P9LIDvC1_o3HKj_ZpSI7gaVAAISGwACnOyxUKEpUUvYP19XNgQ"},
                        {"file_id": "BQACAgQAAIEK2hZ0P9OqQ0HfiwQNAyPr0DwExl0AAIEFwAC91mhUWxtfCR5GupoNgQ"},
                        {"file_id": "BQACAgQAAIELGhZ0P9WezYlgwUy1vTr5k7oUG0pAAIdHAACC34hUbS4QDsvH5dCNgQ"}
                    ]
                },
                {
                    "name": "Econometrics 2",
                    "files": [
                        {"file_id": "BQACAgQAAIEOGhZ0Vfk96NFgucJCLtA1v_qGlFCAAKHFwACt33ZU2XyWX-pMQu-NgQ"},
                        {"file_id": "BQACAgQAAIEOWhZ0Vc9dGpe835LWRASWt9z6qwWAAL3FgACZjvZUyFsBZadPkGSNgQ"},
                        {"file_id": "BQACAgQAAIEOmhZ0Vc_47oLRFMoOXY-MPc_4O4lAAKbFwACt33ZU37kdW8nP7SuNgQ"},
                        {"file_id": "BQACAgQAAIEO2hZ0Vfqe9sH0DyJLQwCEEzCz06uAALpGAAC1T5wUoc1TopMk_yCNgQ"},
                        {"file_id": "BQACAgQAAIEPGhZ0Vf40ikZ_jlDzI07pykR4NznAALqGAAC1T5wUo_STSvEwVLfNgQ"},
                        {"file_id": "BQACAgQAAIEPmhZ0Vf8KhsH3fvdgNmFDUmTAlkDAAImGQACXsXpUG74TtoHUuIzNgQ"},
                        {"file_id": "BQACAgQAAIEP2hZ0VfCfsswPt5UbXgswu9btj3aAAIWFgACanQ4UUqZibhXgGcNNgQ"}
                    ]
                },
                {
                    "name": "Research method for economics",
                    "files": [
                        {"file_id": "BQACAgQAAIESGhZ0bhzpk_6pBMWWCnhavLYK_-XAAJ4FAACNzogU3KOdDtzkldcNgQ"},
                        {"file_id": "BQACAgQAAIESWhZ0bg1Pous6gSFbi2sjRHIUXH9AAJ5FAACNzogUxgqWk7KriWDNgQ"},
                        {"file_id": "BQACAgQAAIESmhZ0bg9FD9mxaxFVqRA52im_7ZcAAJ6FAACNzogU8J8hjHa9he9NgQ"},
                        {"file_id": "BQACAgQAAIES2hZ0biDQJf3x9hXYqHem7hgPby1AAJ7FAACNzogU5JwWhWGC0HNNgQ"},
                        {"file_id": "BQACAgQAAIETGhZ0bjbZ22yB3E8ZJGqOQindmDlAAJ8FAACNzogU392d0k98TjVNgQ"},
                        {"file_id": "BQACAgQAAIETWhZ0bgQNoq66HKYfH0coRKzZs8YAAJ9FAACNzogU_HrvKt56DYyNgQ"},
                        {"file_id": "BQACAgQAAIETmhZ0bgXD5TUoEN65Mj7AR7fwKQUAAL4GAACZfaYUUUxhMfLi5WxNgQ"}
                    ]
                },
                {
                    "name": "Natural resources and environmental economics",
                    "files": [
                        {"file_id": "BQACAgQAAIEVmhZ0h2OzIk-9x5OR7k1v6SiN1XcAALCFQACRDYpU_vG22trf22yNgQ"},
                        {"file_id": "BQACAgQAAIEV2hZ0h3VOjrYxjnwuHfNbRe4rs1uAALDFQACRDYpU8eZq2l0JjoLNgQ"},
                        {"file_id": "BQACAgQAAIEWGhZ0h0N8P1nsCkeegYcAVS6DSCqAALFFQACRDYpU_J3m5L5GXKLNgQ"},
                        {"file_id": "BQACAgQAAIEWWhZ0h3bdAVH4kyW_nRoROmkgzcEAAKkFwACMn0xU9xRBIIQO3FUNgQ"},
                        {"file_id": "BQACAgQAAIEWmhZ0h3xkJhzfwKBMVk0wpYOXdMGAAJHFwACsGRQUzXY14iMxYYqNgQ"},
                        {"file_id": "BQACAgQAAIEW2hZ0h04tFiV8h6uuqmI60nWy4w1AAIbDwAC7WypUlegWqRv0Vw_NgQ"},
                        {"file_id": "BQACAgQAAIEXGhZ0h1207ztHtDfPJfozuZs4zdnAAKpGwACr_moU3xpOfPqZ-y_NgQ"},
                        {"file_id": "BQACAgQAAIEXWhZ0h2syRUPQbP2Ej46QAaBKBChAAJWHAAC41_oUCC4Q3OkBj9xNgQ"},
                        {"file_id": "BQACAgQAAIEXmhZ0h1LAnmvtSc4hTvRQpEtpBEBAALIFgACSLwQUUdwiJI03_1ZNgQ"},
                        {"file_id": "BQACAgQAAIEX2hZ0h1jWOq4AqWSTz0hJ86sZe3DAAIfGwACNT4wUc3uvHrA4Z-qNgQ"}
                    ]
                },
                {
                    "name": "Economics of industry",
                    "files": [
                        {"file_id": "BQACAgQAAIEa2hZ0nCGKcgznf8fyWjPTRo_q55cAAJzEwACbQVgUwfYj8cwYLlONgQ"},
                        {"file_id": "BQACAgQAAIEbGhZ0nAaIsJ03bMLUeBEh6ZoJgz_AAJOFwACksVBUYxahYGArijQNgQ"}
                    ]
                }
            ]
        },
        "4 year": {
            "1 semester": [
                {
                    "name": "Development planning and project analysis 1",
                    "files": [
                        {"file_id": "BQACAgQAAIEpGhZ1_Wo2a-NjkQRJO8xMIPrLGXNAAJgGAACXNZRUnJNiMgdTibjNgQ"},
                        {"file_id": "BQACAgQAAIEpWhZ1_UQuZRnvStKhesEeAInFt8iAAJhGAACXNZRUr8saqf1zVMkNgQ"},
                        {"file_id": "BQACAgQAAIEpmhZ1_UZgjboDsdqUBgvGOqt2uj6AAJ3FwACGl6wUs5BqDUDGKbxNgQ"},
                        {"file_id": "BQACAgQAAIEp2hZ1_VswR16AuRGYWT0TjBsEhP4AAIcGAACruQgU-xQ0-YtHHkWNgQ"},
                        {"file_id": "BQACAgQAAIEqGhZ1_X84U4DCedYzzAc64uAdQOVAAIUEgAC6ev4UkPRlK78T-i7NgQ"}
                    ]
                },
                {
                    "name": "Statistical software application in economics",
                    "files": [
                        {"file_id": "BQACAgQAAIEsGhZ2Em9TCaFHAIOhVZTQNAdm1u6AAIBFwAC4wzRUvVaHNBApDA5NgQ"},
                        {"file_id": "BQACAgQAAIEsWhZ2EmdqvlYz9s2xl4p9ftXbvCMAAIGFwAC4wzRUpWV6sVI3b-LNgQ"},
                        {"file_id": "BQACAgQAAIEsmhZ2El2AAHu_fWLYCCbxmDwDLpyRwACrBgAAg5u-FDwD1TvfoDB3zYE"}
                    ]
                },
                {
                    "name": "History of economic thought",
                    "files": [
                        {"file_id": "BQACAgQAAIEtmhZ2IgoHzUtgE1YAuBtl9AP31m2AAK_EwACOtSAUlYeqsHvfYAnNgQ"},
                        {"file_id": "BQACAgQAAIEt2hZ2Ii5yl166XjtklyVPiN1wQvrAALBEwACOtSAUiu_sZpQwJAzNgQ"},
                        {"file_id": "BQACAgQAAIEuGhZ2Ii1tbx8l8xLXAVi2NHFi23yAALAEwACOtSAUtNIYHP-SxdjNgQ"},
                        {"file_id": "BQACAgQAAIEuWhZ2IgC71LJ0mrf3R9o09UvaBi1AAMXAALjDNFS1BgAAUYY5egFNgQ"}
                    ]
                },
                {
                    "name": "Economics of agriculture",
                    "files": [
                        {"file_id": "BQACAgQAAIEvmhZ2PUnxumUAAGsmzXN6WQ-tMxQegACKBUAAjv8sVIa5yjHPmGrWDYE"},
                        {"file_id": "BQACAgQAAIEv2hZ2PXGV7SU2BJsph1FjDBsGsNRAAIIGAACLy7BUs_b6LT2uhShNgQ"},
                        {"file_id": "BQACAgQAAIEwGhZ2PUZ5paKH-HyiVcGMZcqO_yfAAJuFgACgZ-BUAvbI3-HuKLaNgQ"},
                        {"file_id": "BQACAgQAAIEwWhZ2PXUjUndR4Cv7sMj2NwHKUg4AAJvFgACgZ-BUJO8rUKWZ6SXNgQ"},
                        {"file_id": "BQACAgQAAIEwmhZ2PWVPdbeWPzcwB5xdTxfM2JeAAL0GQACk1roUr8hyYmbxYbzNgQ"}
                    ]
                },
                {
                    "name": "Introduction to institutional and behavioral economics",
                    "files": [
                        {"file_id": "BQACAgQAAIEzGhZ2TrHrzIIGywCYuZyCZaXrEw0AAKfFAACbKXIUDtcT0eR5OQ2NgQ"},
                        {"file_id": "BQACAgQAAIEzWhZ2TqSKRxIPJH2Z5i5i0NE7Fq8AAKEGgAC0rEhUGwDjHYuerpVNgQ"}
                    ]
                },
                {
                    "name": "Monetary economics",
                    "files": [
                        {"file_id": "BQACAgQAAIE0GhZ2Xt5mh9hWnHXpc6wXfJYXD7QAAKREwACMGCAUuq94MUfuin9NgQ"}
                    ]
                }
            ],
            "2 semester": [
                # Add courses for 4 year 2 semester here later
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
    user = update.effective_user
    
    # Track the user
    is_new_user = add_user(
        user_id=user_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    if is_new_user:
        logger.info(f"New user joined: {user_id} (@{user.username})")
    
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
    await update.message.reply_text("Select your field:", reply_markup=make_centered_big_buttons(field_rows, include_feedback=True))

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
        markup = make_centered_big_buttons(field_rows, include_feedback=True)
        if not is_same_message(query.message, "Select your field:", markup):
            await query.edit_message_text("Select your field:", reply_markup=markup)
        return

    if not await is_user_member(user_id, context):
        if not is_same_message(query.message, "Please join our channel to access the bot!", join_button):
            await query.edit_message_text(
                "Please join our channel to access the bot!", reply_markup=join_button
            )
        return

    # If "coming soon" was pressed, just show a notice and do nothing more
    if query.data == "coming_soon":
        await query.answer("Coming soon!", show_alert=True)
        return
    
    # Handle feedback request
    if query.data == "request_feedback":
        await query.answer()
        await query.edit_message_text(
            "📝 Please send your feedback message. We value your input!\n\n"
            "Type your feedback and send it as a regular message.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main")
            ]])
        )
        # Store feedback state in user context
        context.user_data['awaiting_feedback'] = True
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
        # Add a blank ("") semester if list is empty to show "Coming soon!"
        if not semesters:
            sem_rows = [("", "")]
        else:
            sem_rows = [(sem, f"semester|{field}|{year}|{sem}") for sem in semesters]
        markup = make_centered_big_buttons(sem_rows, back_callback=f"field|{field}")
        text = f"Select semester for {field} - {year}:"
        if not is_same_message(query.message, text, markup):
            await query.edit_message_text(text, reply_markup=markup)

    elif data[0] == "semester":
        field, year, semester = data[1], data[2], data[3]
        course_list = courses.get(field, {}).get(year, {}).get(semester, [])
        # If there are no courses, show a "Coming soon!" button
        if not course_list:
            course_rows = [("", "")]
        else:
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

        # Send course name first
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"📚 {course['name']}"
        )

        # Send all files as protected_content (prevents forwarding/saving to gallery, but not download)
        if files:
            for f in files:
                file_id = f.get("file_id")
                if file_id:
                    await context.bot.send_document(
                        chat_id=query.message.chat_id,
                        document=file_id,
                        protect_content=True
                    )
        else:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="No files available for this course."
            )

        # Show only the back button
        markup = make_centered_big_buttons([], back_callback=f"semester|{field}|{year}|{semester}")
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Choose what to do next:",
            reply_markup=markup
        )

    elif data[0] == "file":
        pass

    elif data[0] == "back_to_main":
        try:
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        except Exception as e:
            logger.warning(f"Failed to delete select year message: {e}")
        field_rows = [(field, f"field|{field}") for field in MAIN_FIELDS]
        markup = make_centered_big_buttons(field_rows, include_feedback=True)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Select your field:",
            reply_markup=markup
        )

# Admin commands
async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /broadcast command - Admin only"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    
    if not context.args:
        await update.message.reply_text(
            "📢 *Broadcast Command Usage:*\n\n"
            "/broadcast <message>\n\n"
            "Example: `/broadcast Hello everyone! New materials have been added.`\n\n"
            "The message will be sent to all bot users.",
            parse_mode='Markdown'
        )
        return
    
    # Get the message to broadcast
    broadcast_message = " ".join(context.args)
    user_ids = get_all_user_ids()
    
    if not user_ids:
        await update.message.reply_text("❌ No users found to broadcast to.")
        return
    
    # Send confirmation message
    await update.message.reply_text(
        f"📢 Starting broadcast to {len(user_ids)} users...\n"
        f"Message: {broadcast_message}"
    )
    
    # Broadcast the message
    successful = 0
    failed = 0
    
    for uid in user_ids:
        try:
            await context.bot.send_message(
                chat_id=uid,
                text=f"📢 *Broadcast Message:*\n\n{broadcast_message}",
                parse_mode='Markdown'
            )
            successful += 1
            await asyncio.sleep(0.1)  # Rate limiting
        except Exception as e:
            failed += 1
            logger.warning(f"Failed to send broadcast to {uid}: {e}")
    
    # Send summary
    await update.message.reply_text(
        f"✅ *Broadcast Complete!*\n\n"
        f"📊 Summary:\n"
        f"• Successful: {successful}\n"
        f"• Failed: {failed}\n"
        f"• Total: {len(user_ids)}",
        parse_mode='Markdown'
    )

async def users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /users command - Admin only"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    
    user_count = get_user_count()
    await update.message.reply_text(
        f"👥 *Bot Statistics:*\n\n"
        f"📊 Total Users: *{user_count}*\n"
        f"🤖 Bot is running smoothly!",
        parse_mode='Markdown'
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command - Admin only, detailed statistics"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    
    users_data = load_users()
    user_count = len(users_data)
    
    if user_count == 0:
        await update.message.reply_text("No users found.")
        return
    
    # Calculate statistics
    users_with_username = sum(1 for user in users_data.values() if user.get('username'))
    
    # Recent users (last 7 days)
    from datetime import datetime, timedelta
    week_ago = datetime.now() - timedelta(days=7)
    recent_users = 0
    
    for user in users_data.values():
        try:
            joined_date = datetime.fromisoformat(user.get('joined_date', ''))
            if joined_date >= week_ago:
                recent_users += 1
        except:
            continue
    
    stats_message = (
        f"📊 *Detailed Bot Statistics:*\n\n"
        f"👥 Total Users: *{user_count}*\n"
        f"📧 Users with Username: *{users_with_username}*\n"
        f"🆕 New Users (Last 7 days): *{recent_users}*\n"
        f"📱 Bot ID: `{ADMIN_USER_ID}`\n"
        f"🏠 Channel: @{CHANNEL_USERNAME}"
    )
    
    await update.message.reply_text(stats_message, parse_mode='Markdown')

async def export_users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /export command - Admin only, export user list"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    
    users_data = load_users()
    
    if not users_data:
        await update.message.reply_text("No users to export.")
        return
    
    # Create user list text
    user_list = "📋 *Bot Users Export*\n\n"
    for idx, (uid, user_info) in enumerate(users_data.items(), 1):
        username = user_info.get('username', 'N/A')
        first_name = user_info.get('first_name', 'N/A')
        joined_date = user_info.get('joined_date', 'N/A')[:10]  # Date only
        
        user_list += f"{idx}. ID: `{uid}`\n"
        if username != 'N/A':
            user_list += f"   @{username}\n"
        user_list += f"   {first_name}\n"
        user_list += f"   Joined: {joined_date}\n\n"
        
        # Telegram message limit protection
        if len(user_list) > 3500:
            await update.message.reply_text(user_list, parse_mode='Markdown')
            user_list = ""
    
    if user_list:
        await update.message.reply_text(user_list, parse_mode='Markdown')

async def doc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.document:
        file_id = update.message.document.file_id
        print(f"file_id: {file_id}")
        await update.message.reply_text(
            f"Received! file_id printed to console:\n{file_id}"
        )

async def feedback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if user is awaiting feedback
    if context.user_data.get('awaiting_feedback', False):
        # Clear the feedback state
        context.user_data['awaiting_feedback'] = False
        
        # Get the feedback message
        feedback_text = update.message.text
        user = update.effective_user
        
        # Log feedback (you can also send it to admins, save to database, etc.)
        logger.info(f"Feedback received from {user.first_name} (ID: {user.id}): {feedback_text}")
        
        # Send thank you message
        await update.message.reply_text(
            "🙏 **Thank you for your feedback!**\n\n"
            "We really appreciate you taking the time to share your thoughts with us. "
            "Your feedback helps us improve our service and provide better resources for students.\n\n"
            "We'll review your message and work on making things even better! 💪",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("📚 Back to Main Menu", callback_data="back_to_main")
            ]])
        )
        return
    
    # If not awaiting feedback, ignore the message or handle other text messages
    return

def main():
    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        
        # Regular command handlers
        app.add_handler(CommandHandler("start", start))
        
        # Admin command handlers
        app.add_handler(CommandHandler("broadcast", broadcast_command))
        app.add_handler(CommandHandler("users", users_command))
        app.add_handler(CommandHandler("stats", stats_command))
        app.add_handler(CommandHandler("export", export_users_command))
        
        # Other handlers
        app.add_handler(CallbackQueryHandler(button))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, feedback_handler))
        app.add_handler(MessageHandler(filters.Document.ALL, doc_handler))
        
        logger.info("Bot is running...")
        app.run_polling()
    except Conflict as e:
        logger.error("Another instance of the bot is already running. Please stop it before starting a new one.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    main()
    
