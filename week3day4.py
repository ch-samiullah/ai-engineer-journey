# =============================================
# MINI PROJECT — News + Weather Combined CLI
# =============================================
import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

NEWS_KEY    = os.getenv("NEWS_API_KEY")
WEATHER_KEY = os.getenv("WEATHER_API_KEY")
LOG_FILE    = "daily_briefing.json"

def get_weather(city):
    params = {
        "q"     : city,
        "appid" : WEATHER_KEY,
        "units" : "metric"
    }
    try:
        r = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params=params, timeout=5
        )
        r.raise_for_status()
        return r.json()
    except:
        return {"error": "Weather unavailable"}

def get_news(topic, count=3):
    params = {
        "q"        : topic,
        "apiKey"   : NEWS_KEY,
        "pageSize" : count,
        "language" : "en",
        "sortBy"   : "publishedAt"
    }
    try:
        r = requests.get(
            "https://newsapi.org/v2/everything",
            params=params, timeout=5
        )
        r.raise_for_status()
        return r.json()
    except:
        return {"error": "News unavailable"}

def save_briefing(city, topic, weather, headlines):
    briefing = {
        "date"      : datetime.now().strftime("%Y-%m-%d %H:%M"),
        "city"      : city,
        "topic"     : topic,
        "weather"   : weather,
        "headlines" : headlines
    }
    with open(LOG_FILE, "w") as f:
        json.dump(briefing, f, indent=4)

def daily_briefing():
    print("=" * 50)
    print("     SAMIULLAH'S DAILY BRIEFING")
    print("=" * 50)

    city  = input("Your city: ").strip()
    topic = input("News topic: ").strip()

    # --- WEATHER SECTION ---
    print(f"\n--- Weather in {city} ---")
    weather = get_weather(city)
    if "error" not in weather:
        temp      = weather['main']['temp']
        condition = weather['weather'][0]['description'].title()
        humidity  = weather['main']['humidity']
        print(f"Temperature : {temp}°C")
        print(f"Condition   : {condition}")
        print(f"Humidity    : {humidity}%")
        weather_summary = f"{temp}°C, {condition}"
    else:
        print(weather["error"])
        weather_summary = "Unavailable"

    # --- NEWS SECTION ---
    print(f"\n--- Latest News: {topic} ---")
    news     = get_news(topic)
    headlines = []

    if "error" not in news:
        articles = news.get("articles", [])
        for i, a in enumerate(articles):
            print(f"{i+1}. {a['title']}")
            print(f"   {a['source']['name']} — {a['publishedAt'][:10]}")
            headlines.append(a['title'])
    else:
        print(news["error"])

    # --- SAVE ---
    save_briefing(city, topic, weather_summary, headlines)
    print(f"\n✅ Briefing saved to {LOG_FILE}")
    print("=" * 50)

daily_briefing()
