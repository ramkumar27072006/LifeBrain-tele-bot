# utils/daily_summary.py
from datetime import datetime
from utils.weather import get_weather
from utils.news import get_news
from utils.db import get_tasks
from utils.memory import get_user_pref  # ✅ Added import

def get_daily_summary(user_id, default_city="your city"):
    """Generate a full daily summary: tasks, weather, and news."""
    
    # 🗓️ Tasks
    tasks = get_tasks(user_id)
    if tasks:
        task_text = "\n".join([f"• {t[0]} — {t[1]}" for t in tasks])
    else:
        task_text = "No tasks for today ✅"

    # 🏙️ City preference
    saved_city = get_user_pref(user_id, "city") or default_city

    # 🌤️ Weather
    weather_info = get_weather(saved_city)

    # 📰 News
    news_info = get_news("technology")

    # 📅 Format summary
    now = datetime.now().strftime("%A, %d %B %Y")
    summary = (
        f"🌅 *Good Morning!*\n\n"
        f"📅 {now}\n\n"
        f"🌤️ Weather in {saved_city}:\n{weather_info}\n\n"
        f"📰 News:\n{news_info}\n\n"
        f"🗓️ Tasks:\n{task_text}\n\n"
        f"💡 Have a productive day!"
    )
    return summary
