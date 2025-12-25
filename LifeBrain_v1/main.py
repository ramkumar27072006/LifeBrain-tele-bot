# main.py
import asyncio
import os
import re
import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, CallbackQueryHandler, filters
)
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

# Fix for Windows event loop (safe guard)
try:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
except Exception:
    pass

# --- Import utility modules (your existing utils) ---
from utils.solver import solve_expression
from utils.translator import translate_text
from utils.weather import get_weather
from utils.news import get_news
from utils.db import init_db, add_task, get_tasks, delete_task
from utils.memory import init_memory
from utils.daily_summary import get_daily_summary

# --- Telegram Token ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
if not TELEGRAM_TOKEN:
    raise RuntimeError("❌ TELEGRAM_BOT_TOKEN missing. Add TELEGRAM_BOT_TOKEN to your .env file.")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

scheduler = BackgroundScheduler()
scheduler.start()

# -----------------------
# Helpers
# -----------------------
def format_tasks_text(user_id: int) -> str:
    """Return formatted tasks message for a user id."""
    tasks = get_tasks(user_id)
    if not tasks:
        return "🗓️ No tasks yet! Use /addtask <task> <HH:MM> to add one."
    # tasks expected to be list of (task, time) tuples
    lines = [f"{i+1}. {t[0]} — ⏰ {t[1]}" for i, t in enumerate(tasks)]
    return "📋 <b>Your Tasks:</b>\n" + "\n".join(lines)

def schedule_reminder(application, user_id, message, when):
    async def send_reminder():
        try:
            await application.bot.send_message(chat_id=user_id, text=f"⏰ Reminder: {message}")
        except Exception as e:
            print(f"Reminder failed: {e}")

    # APScheduler will call the lambda at the run_date
    scheduler.add_job(lambda: asyncio.run(send_reminder()), 'date', run_date=when)

# ==============================
# /start
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧮 Solve", callback_data="solve_help"),
         InlineKeyboardButton("🌦 Weather", callback_data="weather_help")],
        [InlineKeyboardButton("📰 News", callback_data="news_help"),
         InlineKeyboardButton("🗓 Tasks", callback_data="show_tasks")],
        [InlineKeyboardButton("❓ Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "🌿 <b>Welcome to LifeBrain Bot</b> — your AI-powered productivity assistant.\n\n"
        "💡 Try commands like:\n"
        "• /solve 25*(4/3)\n"
        "• /translate bonjour\n"
        "• /weather chennai\n"
        "• /news ai\n"
        "• /addtask drink water 14:00\n"
        "• /showtasks\n"
        "• /daily 09:00"
    )
    # reply to the user who started the bot
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="HTML")

# ==============================
# /help
# ==============================
HELP_TEXT = (
    "🆘 <b>LifeBrain Help Menu</b>\n\n"
    "🧮 /solve <expr> — Calculate expressions\n"
    "🗣 /translate <text> — Translate text\n"
    "🌦 /weather <city> — Weather updates\n"
    "📰 /news <topic> — Latest headlines\n"
    "🗓 /addtask <task> <HH:MM> — Add tasks\n"
    "📋 /showtasks — View tasks\n"
    "🌅 /daily <HH:MM> — Daily summary\n"
    "🗑 /deletetask <number> — Delete a task manually\n"
    "💬 Just type anything — Chat with AI (offline mode)"
)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Works for both:
     - message-based calls (/help)
     - callback_query-based calls (button press)
    """
    # If this was triggered by a callback query, prefer sending the help to the user
    if update.callback_query is not None:
        q = update.callback_query
        # answer the callback (removes spinner)
        await q.answer()
        # send help as a new message to the user (so original inline menu remains)
        await context.bot.send_message(chat_id=q.from_user.id, text=HELP_TEXT, parse_mode="HTML")
        return

    # else normal message-based /help
    await update.message.reply_text(HELP_TEXT, parse_mode="HTML")

# ==============================
# /solve
# ==============================
async def solve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /solve 24*(5/3)")
        return
    expr = " ".join(context.args)
    try:
        result = solve_expression(expr)
    except Exception as e:
        result = f"⚠️ Error computing expression: {e}"
    await update.message.reply_text(f"🧮 Result: {result}")

# ==============================
# /translate
# ==============================
async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /translate hola amigo")
        return
    text = " ".join(context.args)
    try:
        translated = translate_text(text)
    except Exception as e:
        translated = f"⚠️ Translation error: {e}"
    await update.message.reply_text(f"Translation: {translated}")

# ==============================
# /weather
# ==============================
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /weather <city>")
        return
    city = " ".join(context.args)
    try:
        resp = get_weather(city)
    except Exception as e:
        resp = f"⚠️ Weather error: {e}"
    await update.message.reply_text(resp)

# ==============================
# /news
# ==============================
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args) if context.args else "AI"
    try:
        resp = get_news(topic)
    except Exception as e:
        resp = f"⚠️ News error: {e}"
    await update.message.reply_text(resp)

# ==============================
# TASKS (add/show)
# ==============================
async def addtask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /addtask <task> <time>\nExample: /addtask drink tea 13:30")
        return

    task = " ".join(context.args[:-1])
    time_str = context.args[-1]
    now = datetime.now()

    # Validate HH:MM
    if not re.match(r"^\d{1,2}:\d{2}$", time_str):
        await update.message.reply_text("❌ Invalid time format. Use HH:MM (24-hour).")
        return

    try:
        hour, minute = map(int, time_str.split(":"))
        task_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if task_time < now:
            task_time += timedelta(days=1)
    except Exception:
        await update.message.reply_text("❌ Invalid time values. Use HH:MM.")
        return

    add_task(update.effective_user.id, task, time_str)
    await update.message.reply_text(f"✅ Task added: {task} at {time_str}")
    schedule_reminder(context.application, update.effective_user.id, task, task_time)

async def showtasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Works for both message and callback: prefer user id from callback_query if present
    user_id = update.effective_user.id
    text = format_tasks_text(user_id)
    # If called from callback, answer and send new message so inline keyboard isn't replaced
    if update.callback_query is not None:
        await update.callback_query.answer()
        await context.bot.send_message(chat_id=user_id, text=text, parse_mode="HTML")
        return
    await update.message.reply_text(text, parse_mode="HTML")

async def deletetask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Usage: /deletetask <task_number>\nExample: /deletetask 2"
        )
        return

    try:
        index = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Task number must be a number.")
        return

    success = delete_task(update.effective_user.id, index)

    if success:
        await update.message.reply_text("✅ Task deleted successfully.")
    else:
        await update.message.reply_text("❌ Invalid task number.")


# ==============================
# /daily summary
# ==============================
def schedule_daily_summary(application, user_id, hour=7, minute=0):
    def send_summary():
        summary = get_daily_summary(user_id)
        asyncio.run(application.bot.send_message(chat_id=user_id, text=summary, parse_mode="HTML"))

    now = datetime.now()
    first_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if first_time < now:
        first_time += timedelta(days=1)

    scheduler.add_job(send_summary, 'interval', days=1, next_run_time=first_time)

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if context.args:
        match = re.match(r"^(\d{1,2}):(\d{2})$", context.args[0])
        if not match:
            await update.message.reply_text("⚠️ Invalid format! Use /daily HH:MM (e.g., /daily 8:30)")
            return
        hour, minute = int(match.group(1)), int(match.group(2))
        if not (0 <= hour < 24 and 0 <= minute < 60):
            await update.message.reply_text("⚠️ Invalid hour/minute range.")
            return
        schedule_daily_summary(context.application, user_id, hour, minute)
        await update.message.reply_text(f"✅ Daily summary set for {hour:02d}:{minute:02d} every day 🌅")
        return

    schedule_daily_summary(context.application, user_id)
    await update.message.reply_text("✅ Daily summary enabled at 07:00 AM 🌅")

# ==============================
# Offline simple chat replies
# ==============================
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    if text.startswith("/"):
        return

    responses = {
        "hi": ["Hey there 👋", "Hi! How can I help today?", "Hello friend! 😊"],
        "how are you": ["I'm just a bot, but feeling great!", "Doing awesome, thanks for asking!"],
        "who are you": ["I'm LifeBrain, your AI assistant.", "Your digital buddy for tasks and info."],
        "bye": ["Goodbye! 👋", "See you later!"],
    }

    reply = None
    for key, vals in responses.items():
        if key in text:
            reply = random.choice(vals)
            break

    if not reply:
        reply = random.choice([
            "Interesting! 🤔",
            "Tell me more!",
            "Got it 👍",
            "I'm here to help — try /help to see what I can do."
        ])

    await update.message.reply_text(reply)

# ==============================
# CallbackQuery handler
# ==============================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is None:
        return
    await query.answer()

    if query.data == "solve_help":
        await context.bot.send_message(chat_id=query.from_user.id, text="Usage: /solve 24*(5/3)")
    elif query.data == "weather_help":
        await context.bot.send_message(chat_id=query.from_user.id, text="Usage: /weather <city>")
    elif query.data == "news_help":
        await context.bot.send_message(chat_id=query.from_user.id, text="Usage: /news <topic>")
    elif query.data == "show_tasks":
        # send the tasks list to the user
        await context.bot.send_message(chat_id=query.from_user.id, text=format_tasks_text(query.from_user.id), parse_mode="HTML")
    elif query.data == "help":
        # reuse help_command but call it with the callback update
        await help_command(update, context)
    else:
        await query.edit_message_text("ℹ️ Use /help to see available commands.")

# ==============================
# Handlers registration
# ==============================
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("solve", solve))
app.add_handler(CommandHandler("translate", translate))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("news", news))
app.add_handler(CommandHandler("addtask", addtask))
app.add_handler(CommandHandler("showtasks", showtasks))
app.add_handler(CommandHandler("daily", daily))
app.add_handler(CommandHandler("deletetask", deletetask))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.add_handler(CallbackQueryHandler(button_handler))

# ==============================
# Main
# ==============================
if __name__ == "__main__":
    print("🚀 LifeBrain Bot running (free version)...")
    init_db()
    init_memory()
    app.run_polling()
            