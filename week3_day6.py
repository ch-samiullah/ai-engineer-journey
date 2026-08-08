# =============================================
# WEEK 3 · SATURDAY PROJECT
# PakInfo CLI — Pakistan Information Tool
# =============================================
import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

WEATHER_KEY = os.getenv("WEATHER_API_KEY")
NEWS_KEY    = os.getenv("NEWS_API_KEY")

# =============================================
# API FUNCTIONS
# =============================================
def safe_get(url, params=None, headers=None):
    try:
        r = requests.get(url, params=params,
                        headers=headers, timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP Error: {e}"}
    except requests.exceptions.ConnectionError:
        return {"error": "No internet connection!"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out!"}
    except Exception as e:
        return {"error": str(e)}

def get_weather(city):
    data = safe_get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "q"     : city,
            "appid" : WEATHER_KEY,
            "units" : "metric"
        }
    )
    if "error" in data:
        return data
    return {
        "city"      : data['name'],
        "temp"      : data['main']['temp'],
        "feels"     : data['main']['feels_like'],
        "humidity"  : data['main']['humidity'],
        "condition" : data['weather'][0]['description'].title(),
        "wind"      : data['wind']['speed'],
        "country"   : data['sys']['country']
    }

def get_news(topic, count=5):
    data = safe_get(
        "https://newsapi.org/v2/everything",
        params={
            "q"        : topic,
            "apiKey"   : NEWS_KEY,
            "pageSize" : count,
            "language" : "en",
            "sortBy"   : "publishedAt"
        }
    )
    if "error" in data:
        return []
    return [
        {
            "title"  : a['title'],
            "source" : a['source']['name'],
            "date"   : a['publishedAt'][:10],
            "url"    : a['url']
        }
        for a in data.get("articles", [])
    ]

def get_country_info(country="pakistan"):
    data = safe_get(
        f"https://restcountries.com/v3.1/name/{country}"
    )
    if "error" in data or not data:
        return {"error": "Country info unavailable"}
    c = data[0]
    currencies = c.get("currencies", {})
    currency   = list(currencies.keys())[0] if currencies else "N/A"
    languages  = list(c.get("languages", {}).values())
    return {
        "name"       : c['name']['common'],
        "capital"    : c.get('capital', ['N/A'])[0],
        "population" : c.get('population', 0),
        "region"     : c.get('region', 'N/A'),
        "currency"   : currency,
        "languages"  : ", ".join(languages),
        "flag"       : c.get('flag', '')
    }

def get_advice():
    data = safe_get("https://api.adviceslip.com/advice")
    if "error" in data:
        return "Keep coding. Every day counts. 💪"
    return data['slip']['advice']

# =============================================
# DISPLAY FUNCTIONS
# =============================================
def print_header(title):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")

def print_section(title):
    print(f"\n  {title}")
    print(f"  {'─'*45}")

def display_weather(weather):
    print_section("🌤️  WEATHER")
    if "error" in weather:
        print(f"  {weather['error']}")
        return
    print(f"  City        : {weather['city']}")
    print(f"  Temperature : {weather['temp']}°C "
          f"(Feels {weather['feels']}°C)")
    print(f"  Condition   : {weather['condition']}")
    print(f"  Humidity    : {weather['humidity']}%")
    print(f"  Wind        : {weather['wind']} m/s")

def display_news(news, topic):
    print_section(f"📰  LATEST NEWS — {topic.upper()}")
    if not news:
        print("  No news found.")
        return
    for i, a in enumerate(news):
        title = a['title'][:60] + "..." \
                if len(a['title']) > 60 else a['title']
        print(f"  {i+1}. {title}")
        print(f"     {a['source']} — {a['date']}")

def display_country(info):
    print_section("🌍  PAKISTAN INFO")
    if "error" in info:
        print(f"  {info['error']}")
        return
    print(f"  Capital    : {info['capital']}")
    print(f"  Population : {info['population']:,}")
    print(f"  Currency   : {info['currency']}")
    print(f"  Languages  : {info['languages']}")
    print(f"  Flag       : {info['flag']}")

def display_advice(advice):
    print_section("💡  TODAY'S ADVICE")
    print(f"  \"{advice}\"")

# =============================================
# SAVE REPORT
# =============================================
def save_report(city, topic, weather, news, country, advice):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    date_str  = datetime.now().strftime("%Y%m%d_%H%M")

    # Save JSON
    report = {
        "timestamp" : timestamp,
        "city"      : city,
        "topic"     : topic,
        "weather"   : weather,
        "news"      : news,
        "country"   : country,
        "advice"    : advice
    }
    json_file = f"pakinfo_{date_str}.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    # Save TXT
    txt_file = f"pakinfo_{date_str}.txt"
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(f"PAKINFO REPORT — {timestamp}\n")
        f.write("=" * 55 + "\n\n")

        f.write("WEATHER\n")
        f.write("-" * 45 + "\n")
        if "error" not in weather:
            f.write(f"City      : {weather['city']}\n")
            f.write(f"Temp      : {weather['temp']}°C\n")
            f.write(f"Condition : {weather['condition']}\n\n")

        f.write(f"NEWS — {topic.upper()}\n")
        f.write("-" * 45 + "\n")
        for i, a in enumerate(news):
            f.write(f"{i+1}. {a['title']}\n")
            f.write(f"   {a['source']} — {a['date']}\n")
        f.write("\n")

        f.write("PAKISTAN INFO\n")
        f.write("-" * 45 + "\n")
        if "error" not in country:
            f.write(f"Capital    : {country['capital']}\n")
            f.write(f"Population : {country['population']:,}\n")
            f.write(f"Currency   : {country['currency']}\n\n")

        f.write("TODAY'S ADVICE\n")
        f.write("-" * 45 + "\n")
        f.write(f'"{advice}"\n')

    print(f"\n  ✅ JSON saved → {json_file}")
    print(f"  ✅ TXT saved  → {txt_file}")

# =============================================
# MAIN
# =============================================
def main():
    print_header("PAKINFO CLI — Pakistan Information Tool")
    print(f"  {datetime.now().strftime('%A, %d %B %Y — %I:%M %p')}")

    city  = input("\n  Your city (default: Rawalpindi): ").strip()
    city  = city if city else "Rawalpindi"
    topic = input("  News topic (default: Pakistan): ").strip()
    topic = topic if topic else "Pakistan"

    print("\n  Fetching data — please wait... ⏳")

    # Fetch all data
    weather = get_weather(city)
    news    = get_news(topic)
    country = get_country_info("pakistan")
    advice  = get_advice()

    # Display
    print_header("YOUR PAKINFO REPORT")
    display_weather(weather)
    display_news(news, topic)
    display_country(country)
    display_advice(advice)
    print(f"\n{'='*55}")

    # Save
    save = input("\n  Save report? (y/n): ").strip()
    if save.lower() == "y":
        save_report(city, topic, weather,
                   news, country, advice)

    print("\n  Goodbye! Keep coding. ")
    print("=" * 55)

main()