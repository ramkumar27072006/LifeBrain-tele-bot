# utils/weather.py
import os
import requests

OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY", "")

def get_weather(city):
    if not OPENWEATHER_KEY:
        return "⚠️ Weather API key not set. Add OPENWEATHER_API_KEY to .env"
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": OPENWEATHER_KEY, "units": "metric"}
        r = requests.get(url, params=params, timeout=10).json()
        if r.get("cod") != 200:
            return "❌ City not found."
        desc = r["weather"][0]["description"].title()
        temp = r["main"]["temp"]
        humidity = r["main"]["humidity"]
        return f"🌤️ Weather in {city.title()}: {desc}\n🌡️ {temp}°C | 💧 {humidity}%"
    except Exception as e:
        return f"⚠️ Weather error: {e}"
