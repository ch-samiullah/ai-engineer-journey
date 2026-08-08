# =============================================
# WEEK 3 · DAY 3 — OpenWeatherMap API
# =============================================
import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

API_KEY  = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
LOG_FILE = "weather_log.json"

# =============================================
# PART 1 — Get Weather Function
# =============================================
def get_weather(city):
    params = {
        "q"     : city,
        "appid" : API_KEY,
        "units" : "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        return {"error": f"City '{city}' not found!"}
    except requests.exceptions.ConnectionError:
        return {"error": "No internet connection!"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out!"}

def display_weather(data):
    if "error" in data:
        print(data["error"])
        return
    print(f"\n{'='*40}")
    print(f"  Weather in {data['name']}, "
          f"{data['sys']['country']}")
    print(f"{'='*40}")
    print(f"  Temperature : {data['main']['temp']}°C")
    print(f"  Feels like  : {data['main']['feels_like']}°C")
    print(f"  Humidity    : {data['main']['humidity']}%")
    print(f"  Condition   : "
          f"{data['weather'][0]['description'].title()}")
    print(f"  Wind Speed  : {data['wind']['speed']} m/s")
    print(f"{'='*40}")

# =============================================
# PART 2 — Save to Log
# =============================================
def save_to_log(city, temp, condition):
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            log = json.load(f)
    else:
        log = []

    log.append({
        "city"      : city,
        "temp"      : temp,
        "condition" : condition,
        "time"      : datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=4)

def view_log():
    if not os.path.exists(LOG_FILE):
        print("No searches yet.")
        return
    with open(LOG_FILE, "r") as f:
        log = json.load(f)

    print(f"\n--- Last {min(5, len(log))} Searches ---")
    for entry in log[-5:]:
        print(f"{entry['time']} | {entry['city']:15} | "
              f"{entry['temp']}°C | {entry['condition']}")

# =============================================
# PART 3 — Pakistan Dashboard
# =============================================
def weather_dashboard():
    cities = ["Rawalpindi", "Lahore", "Karachi",
              "Islamabad", "Peshawar"]

    print(f"\n{'='*55}")
    print(f"  {'PAKISTAN WEATHER DASHBOARD':^50}")
    print(f"{'='*55}")
    print(f"  {'City':15} | {'Temp':>6} | "
          f"{'Humidity':>8} | Condition")
    print(f"{'─'*55}")

    results = []
    for city in cities:
        data = get_weather(city)
        if "error" not in data:
            temp      = data['main']['temp']
            humidity  = data['main']['humidity']
            condition = data['weather'][0]['description'].title()
            results.append({
                "city"      : city,
                "temp"      : temp,
                "humidity"  : humidity,
                "condition" : condition
            })
            save_to_log(city, temp, condition)
            print(f"  {city:15} | {temp:>5}°C | "
                  f"{humidity:>7}% | {condition}")
        else:
            print(f"  {city:15} | Error!")

    print(f"{'─'*55}")

    if results:
        hottest  = max(results, key=lambda x: x['temp'])
        coldest  = min(results, key=lambda x: x['temp'])
        avg_temp = sum(r['temp'] for r in results) / len(results)
        print(f"  Hottest : {hottest['city']} ({hottest['temp']}°C)")
        print(f"  Coldest : {coldest['city']} ({coldest['temp']}°C)")
        print(f"  Average : {avg_temp:.1f}°C")
    print(f"{'='*55}")

# =============================================
# MAIN — Run Everything
# =============================================
def main():
    print("=" * 40)
    print("   SAMIULLAH'S WEATHER APP")
    print("=" * 40)
    print("1. Pakistan Dashboard")
    print("2. Search Any City")
    print("3. View Recent Searches")
    print("0. Exit")
    print("=" * 40)

    while True:
        choice = input("\nChoose (0-3): ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            weather_dashboard()
        elif choice == "2":
            city = input("Enter city name: ").strip()
            if city:
                data = get_weather(city)
                display_weather(data)
                if "error" not in data:
                    save_to_log(
                        city,
                        data['main']['temp'],
                        data['weather'][0]['description']
                    )
        elif choice == "3":
            view_log()
        else:
            print("Invalid choice!")
 
main()