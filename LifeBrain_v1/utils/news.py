# utils/news.py
import os
import requests

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

def get_news(topic="AI"):
    if not NEWS_API_KEY:
        return "⚠️ News API key not set. Add NEWS_API_KEY to .env"
    try:
        url = "https://newsapi.org/v2/everything"
        params = {"q": topic, "apiKey": NEWS_API_KEY, "language": "en", "pageSize": 3}
        r = requests.get(url, params=params, timeout=10).json()
        articles = r.get("articles", [])
        if not articles:
            return "📰 No news found."
        headlines = []
        for a in articles[:3]:
            title = a.get("title", "No title")
            url = a.get("url", "")
            headlines.append(f"🗞️ {title}\n🔗 {url}")
        return "\n\n".join(headlines)
    except Exception as e:
        return f"⚠️ News error: {e}"
