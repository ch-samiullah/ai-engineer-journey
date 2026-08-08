# =============================================
# WEEK 4 · SATURDAY PROJECT
# Smart API Dashboard — Complete CLI Tool
# =============================================

import requests      # HTTP requests ke liye
import os            # environment variables ke liye
import time          # rate limiting ke liye
import json          # JSON save/load ke liye
from dotenv import load_dotenv    # .env file load karne ke liye
from datetime import datetime     # date/time ke liye

load_dotenv()   # .env file se keys load karo

# =============================================
# CONFIG — saari settings ek jagah
# =============================================
class Config:
    WEATHER_KEY = os.getenv("WEATHER_API_KEY")  # weather API key .env se
    NEWS_KEY    = os.getenv("NEWS_API_KEY")      # news API key .env se
    APP_NAME    = os.getenv("APP_NAME",
                            "Smart Dashboard")   # app naam, default value bhi
    MAX_RETRIES = int(os.getenv("MAX_RETRIES",
                                "3"))            # retry count, string to int
    TIMEOUT     = int(os.getenv("TIMEOUT", "5")) # seconds mein timeout
    DEBUG       = os.getenv("DEBUG_MODE",
                            "False") == "True"   # string "True" ko bool banao
    HISTORY_FILE = "dashboard_history.json"      # history file ka naam

# =============================================
# BASE CLIENT — sab clients ka parent
# =============================================
class BaseClient:

    def __init__(self):
        self.config  = Config()            # settings load karo
        self.session = requests.Session()  # persistent connection banao
        self.calls   = 0                   # total calls count
        self.failed  = 0                   # failed calls count
        self.history = []                  # is session ki history

        # har request ke saath yeh headers automatically jayenge
        self.session.headers.update({
            "User-Agent"   : self.config.APP_NAME,  # app identify karwao
            "Content-Type" : "application/json"      # JSON format batao
        })

    def _request(self, method, url, **kwargs):
        kwargs['timeout'] = self.config.TIMEOUT  # timeout add karo

        for attempt in range(1,
                             self.config.MAX_RETRIES + 1):  # retry loop
            try:
                if self.config.DEBUG:  # debug mode mein URL print karo
                    print(f"  🔍 Attempt {attempt}: {url[:45]}...")

                response = self.session.request(
                    method, url, **kwargs  # actual request bhejo
                )
                self.calls += 1              # call count badao
                response.raise_for_status()  # error status pe exception

                return {
                    "success": True,
                    "data"   : response.json()  # dict mein convert karke return
                }

            except requests.exceptions.HTTPError:
                if response.status_code == 429:
                    wait = 2 ** attempt  # exponential backoff: 2,4,8 sec
                    print(f"  ⚠️ Rate limited — {wait}s wait")
                    time.sleep(wait)
                elif response.status_code >= 500:
                    time.sleep(attempt)  # server error — thodi der ruko
                else:
                    self.failed += 1     # 404/401 — retry mat karo
                    return {
                        "success": False,
                        "error"  : f"HTTP {response.status_code}"
                    }

            except requests.exceptions.Timeout:
                print(f"  ⏱️ Timeout — attempt {attempt}")
                time.sleep(attempt)  # timeout pe wait karo

            except requests.exceptions.ConnectionError:
                self.failed += 1  # internet nahi — fail
                return {"success": False, "error": "No internet!"}

        self.failed += 1  # saare retries khatam
        return {"success": False, "error": "Max retries reached"}

    def get(self, url, params=None):
        return self._request("GET", url, params=params)  # GET shortcut

    def post(self, url, payload=None):
        return self._request("POST", url, json=payload)  # POST shortcut

    def log(self, action, query, result):
        # history mein entry add karo
        self.history.append({
            "time"   : datetime.now().strftime("%H:%M:%S"),  # current time
            "action" : action,   # kya kiya — weather/news etc
            "query"  : query,    # user ne kya search kiya
            "status" : "✅" if result else "❌"  # success ya fail
        })

    def stats(self):
        total   = self.calls              # total calls
        success = total - self.failed     # successful calls
        rate    = (success/total*100) \
                  if total else 0         # success percentage
        print(f"\n  📊 Session Stats:")
        print(f"  Total calls  : {total}")
        print(f"  Successful   : {success}")
        print(f"  Failed       : {self.failed}")
        print(f"  Success rate : {rate:.1f}%")  # 1 decimal point

# =============================================
# DASHBOARD CLIENT — BaseClient extend karo
# =============================================
class DashboardClient(BaseClient):
    # BaseClient inherit kiya — uske sab methods available

    def weather(self, city):
        result = self.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q"     : city,               # city name
                "appid" : self.config.WEATHER_KEY,  # API key
                "units" : "metric"            # celsius
            }
        )
        self.log("weather", city,
                 result["success"])  # history mein log karo

        if not result["success"]:
            return result  # error return karo

        d = result["data"]  # response data shortcut
        return {
            "success"   : True,
            "city"      : d['name'],                          # city naam
            "country"   : d['sys']['country'],                # country code
            "temp"      : d['main']['temp'],                  # temperature
            "feels"     : d['main']['feels_like'],            # feels like
            "min"       : d['main']['temp_min'],              # min temp
            "max"       : d['main']['temp_max'],              # max temp
            "humidity"  : d['main']['humidity'],              # humidity %
            "condition" : d['weather'][0]['description'].title(),  # weather description
            "wind"      : d['wind']['speed']                  # wind speed
        }

    def news(self, topic, count=3):
        result = self.get(
            "https://newsapi.org/v2/everything",
            params={
                "q"       : topic,                  # search topic
                "apiKey"  : self.config.NEWS_KEY,   # API key
                "pageSize": count,                  # kitne articles
                "language": "en",                   # english only
                "sortBy"  : "publishedAt"           # latest pehle
            }
        )
        self.log("news", topic,
                 result["success"])  # history mein log karo

        if not result["success"]:
            return []  # error pe empty list

        # list comprehension — sirf zaroori fields
        return [
            {
                "title"  : a['title'],
                "source" : a['source']['name'],
                "date"   : a['publishedAt'][:10],  # sirf date part
                "url"    : a['url']                # article link
            }
            for a in result["data"].get("articles", [])
        ]

    def country(self, name):
        result = self.get(
            f"https://restcountries.com/v3.1/name/{name}"
        )
        self.log("country", name,
                 result["success"])  # history log

        if not result["success"]:
            return result

        c          = result["data"][0]        # list ka pehla result
        currencies = c.get("currencies", {})  # currencies dict
        currency   = list(currencies.keys())[0] \
                     if currencies else "N/A"  # pehli currency
        curr_name  = currencies[currency]["name"] \
                     if currencies else "N/A"  # currency full name
        languages  = list(
            c.get("languages", {}).values()
        )  # languages list

        return {
            "success"    : True,
            "name"       : c['name']['common'],          # country naam
            "capital"    : c.get('capital', ['N/A'])[0], # capital city
            "population" : c.get('population', 0),       # population number
            "region"     : c.get('region', 'N/A'),       # continent
            "currency"   : f"{currency} — {curr_name}",  # currency code + name
            "languages"  : ", ".join(languages),          # languages joined
            "flag"       : c.get('flag', '')              # flag emoji
        }

    def post_test(self, data):
        # httpbin.org pe POST test — jo bhejna wahi wapas aata
        result = self.post(
            "https://httpbin.org/post",
            payload=data
        )
        self.log("post_test", "httpbin",
                 result["success"])  # log karo

        if result["success"]:
            return result["data"]["json"]  # sent data wapas aata hai
        return result

# =============================================
# HISTORY MANAGER — history save/load karo
# =============================================
class HistoryManager:

    def __init__(self):
        self.file = Config.HISTORY_FILE  # file naam config se

    def save(self, session_data):
        # pehle existing history load karo
        all_history = self.load_all()
        all_history.append(session_data)  # naya session add karo

        # wapas save karo
        with open(self.file, "w",
                  encoding="utf-8") as f:
            json.dump(all_history, f,
                      indent=4,
                      ensure_ascii=False)  # unicode support

        print(f"  ✅ History saved → {self.file}")

    def load_all(self):
        if not os.path.exists(self.file):
            return []  # file nahi hai toh empty list

        try:
            with open(self.file, "r",
                      encoding="utf-8") as f:
                return json.load(f)  # JSON load karo
        except json.JSONDecodeError:
            return []  # corrupt file pe empty list

    def show_recent(self, n=5):
        all_history = self.load_all()
        if not all_history:
            print("  No history found.")
            return

        print(f"\n  📚 Last {n} Sessions:")
        print(f"  {'─'*45}")
        # last n sessions dikhao
        for session in all_history[-n:]:
            print(f"  {session.get('started', 'N/A')} — "
                  f"{session.get('total_searches', 0)} searches")

# =============================================
# DISPLAY FUNCTIONS
# =============================================
def display_weather(w):
    # weather data neatly print karo
    print(f"\n  {'='*45}")
    print(f"  🌤️  {w.get('city')}, {w.get('country')}")
    print(f"  {'─'*45}")
    print(f"  Temperature : {w.get('temp')}°C "
          f"(Feels {w.get('feels')}°C)")  # actual + feels like
    print(f"  Range       : {w.get('min')}°C — "
          f"{w.get('max')}°C")  # min max range
    print(f"  Condition   : {w.get('condition')}")
    print(f"  Humidity    : {w.get('humidity')}%")
    print(f"  Wind        : {w.get('wind')} m/s")
    print(f"  {'='*45}")

def display_news(articles, topic):
    print(f"\n  {'='*45}")
    print(f"  📰  {topic.upper()} NEWS")
    print(f"  {'─'*45}")

    if not articles:
        print("  No articles found.")
        return

    for i, a in enumerate(articles):
        # title 55 chars se zyada ho toh cut karo
        title = a['title'][:55] + "..." \
                if len(a['title']) > 55 else a['title']
        print(f"  {i+1}. {title}")
        print(f"     📌 {a['source']} — {a['date']}")
    print(f"  {'='*45}")

def display_country(c):
    print(f"\n  {'='*45}")
    print(f"  🌍  {c.get('name')} {c.get('flag')}")
    print(f"  {'─'*45}")
    print(f"  Capital    : {c.get('capital')}")
    print(f"  Population : {c.get('population', 0):,}")  # comma format
    print(f"  Region     : {c.get('region')}")
    print(f"  Currency   : {c.get('currency')}")
    print(f"  Languages  : {c.get('languages')}")
    print(f"  {'='*45}")

def display_history(session_log):
    # session ki sari searches print karo
    print(f"\n  📋 Session Log:")
    print(f"  {'─'*40}")
    if not session_log:
        print("  No searches yet.")
        return
    for entry in session_log:
        # har entry ek line mein
        print(f"  {entry['time']} | "
              f"{entry['action']:10} | "
              f"{entry['query']:15} | "
              f"{entry['status']}")

# =============================================
# MAIN MENU
# =============================================
def show_menu():
    print(f"\n  {'='*45}")
    print(f"   🚀 {Config.APP_NAME}")
    print(f"  {'='*45}")
    print("  1. 🌤️  Weather lookup")
    print("  2. 📰  News search")
    print("  3. 🌍  Country info")
    print("  4. 🔁  POST request test")
    print("  5. 📋  Session log")
    print("  6. 📚  Past sessions")
    print("  7. 📊  API stats")
    print("  0. 🚪  Exit + save")
    print(f"  {'='*45}")

def main():
    client  = DashboardClient()   # client object banao
    history = HistoryManager()    # history manager banao

    # session data — is run ki saari info
    session = {
        "started"       : datetime.now().strftime(
            "%Y-%m-%d %H:%M"),  # start time
        "total_searches": 0           # searches counter
    }

    print(f"\n  {'='*45}")
    print(f"  🚀 {Config.APP_NAME} — Started!")
    print(f"  Debug: {Config.DEBUG} | "
          f"Retries: {Config.MAX_RETRIES} | "
          f"Timeout: {Config.TIMEOUT}s")
    print(f"  {'='*45}")

    while True:   # jab tak 0 na daalo
        show_menu()
        choice = input("  Choose (0-7): ").strip()

        if choice == "0":
            # session end karo
            session["ended"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M")
            session["total_searches"] = \
                len(client.history)  # kitni searches ki
            session["log"] = client.history  # full log save

            client.stats()           # final stats print
            display_history(client.history)  # session log

            # history file mein save karo
            save = input("\n  Save to history? (y/n): ")
            if save.lower() == "y":
                history.save(session)

            print("\n  Goodbye! Keep coding. 💪")
            break  # loop exit

        elif choice == "1":
            city = input("  Enter city: ").strip()
            if city:  # empty check
                w = client.weather(city)
                if w.get("success"):
                    display_weather(w)
                else:
                    print(f"  ❌ {w.get('error')}")

        elif choice == "2":
            topic = input("  Enter topic: ").strip()
            if topic:
                count = input(
                    "  How many articles? (1-5): "
                ).strip()
                # valid number check
                count = int(count) \
                        if count.isdigit() \
                        and 1 <= int(count) <= 5 else 3
                news  = client.news(topic, count)
                display_news(news, topic)

        elif choice == "3":
            country = input("  Enter country: ").strip()
            if country:
                c = client.country(country)
                if c.get("success"):
                    display_country(c)
                else:
                    print(f"  ❌ {c.get('error')}")

        elif choice == "4":
            print("  Sending POST request...")
            # test data bhejo
            result = client.post_test({
                "name"      : "Samiullah",
                "week"      : 4,
                "skill"     : "API Mastery",
                "timestamp" : datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                )
            })
            print(f"  POST echoed back: {result}")

        elif choice == "5":
            # is session ka log dikhao
            display_history(client.history)

        elif choice == "6":
            # past sessions dikhao history file se
            history.show_recent()

        elif choice == "7":
            client.stats()  # API usage stats

        else:
            print("  ❌ Invalid choice — 0-7 enter karo!")

main()   # program start karo