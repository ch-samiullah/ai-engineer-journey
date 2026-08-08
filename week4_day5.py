# =============================================
# WEEK 4 · DAY 5 — DevTools CLI
# Final Recap Project
# =============================================
import requests      # API calls ke liye
import os            # .env variables read karne ke liye
import time          # rate limiting ke liye sleep()
import json          # JSON file save karne ke liye
from dotenv import load_dotenv   # .env file load karne ke liye
from datetime import datetime    # current time/date ke liye

load_dotenv()   # .env file se saari keys load karo

# =============================================
# CONFIG CLASS — saari settings ek jagah
# =============================================
class Config:
    # os.getenv() .env file se value uthata hai
    WEATHER_KEY  = os.getenv("WEATHER_API_KEY")   # weather API key
    NEWS_KEY     = os.getenv("NEWS_API_KEY")       # news API key
    APP_NAME     = os.getenv("APP_NAME", "DevTools CLI")  # default value bhi hai
    MAX_RETRIES  = int(os.getenv("MAX_RETRIES", "3"))     # string ko int mein convert
    TIMEOUT      = int(os.getenv("TIMEOUT", "5"))         # seconds mein
    DEBUG        = os.getenv("DEBUG_MODE", "False") == "True"  # string "True" ko bool mein convert

# =============================================
# BASE CLIENT — sab API clients ka parent
# =============================================
class BaseClient:

    def __init__(self):
        self.config  = Config()           # settings load karo
        self.session = requests.Session() # persistent HTTP connection banao
        self.calls   = 0                  # total API calls counter
        self.failed  = 0                  # failed calls counter

        # har request ke saath automatically yeh headers jayenge
        self.session.headers.update({
            "User-Agent"   : self.config.APP_NAME,  # app ka naam batao server ko
            "Content-Type" : "application/json"      # hum JSON bhej rahe hain
        })

    def _request(self, method, url, **kwargs):
        # timeout har request mein add karo config se
        kwargs['timeout'] = self.config.TIMEOUT

        # MAX_RETRIES tak try karo
        for attempt in range(1, self.config.MAX_RETRIES + 1):
            try:
                # debug mode ON hai toh request print karo
                if self.config.DEBUG:
                    print(f"  🔍 {method} {url[:50]}...")

                # actual HTTP request bhejo
                response = self.session.request(
                    method, url, **kwargs
                )
                self.calls += 1              # call count badao
                response.raise_for_status()  # 4xx/5xx pe error raise karo

                # success — data wapas karo
                return {"success": True,
                        "data"   : response.json()}

            except requests.exceptions.HTTPError:
                if response.status_code == 429:
                    # rate limited — exponential backoff
                    wait = 2 ** attempt      # 2, 4, 8 seconds
                    print(f"  ⚠️ Rate limited — waiting {wait}s")
                    time.sleep(wait)
                elif response.status_code >= 500:
                    # server error — thodi der wait karo
                    time.sleep(attempt)
                else:
                    # 404, 401 etc — retry mat karo
                    self.failed += 1
                    return {"success": False,
                            "error"  : response.status_code}

            except requests.exceptions.Timeout:
                # request timed out — next attempt try karo
                print(f"  ⏱️ Timeout attempt {attempt}")
                time.sleep(attempt)

            except requests.exceptions.ConnectionError:
                # internet nahi — immediately fail
                self.failed += 1
                return {"success": False,
                        "error"  : "No internet!"}

        # saare retries khatam — fail
        self.failed += 1
        return {"success": False,
                "error"  : "Max retries reached"}

    def get(self, url, params=None):
        # GET request shortcut
        return self._request("GET", url, params=params)

    def post(self, url, payload=None):
        # POST request shortcut
        return self._request("POST", url, json=payload)

    def stats(self):
        total   = self.calls
        success = total - self.failed
        # success rate calculate karo
        rate    = (success/total*100) if total else 0
        print(f"\n  📊 API Stats:")
        print(f"  Total calls  : {total}")
        print(f"  Successful   : {success}")
        print(f"  Failed       : {self.failed}")
        print(f"  Success rate : {rate:.1f}%")

# =============================================
# DEVTOOLS CLIENT — BaseClient ko extend karo
# =============================================
class DevToolsClient(BaseClient):
    # BaseClient inherit kiya — uske sab methods available hain

    def weather(self, city):
        # GET request with weather params
        result = self.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q"     : city,
                "appid" : self.config.WEATHER_KEY,
                "units" : "metric"   # celsius mein chahiye
            }
        )
        if not result["success"]:
            return result            # error wapas karo

        d = result["data"]           # response data shortcut
        # sirf zaroori fields return karo
        return {
            "success"   : True,
            "city"      : d['name'],
            "temp"      : d['main']['temp'],
            "feels"     : d['main']['feels_like'],
            "humidity"  : d['main']['humidity'],
            "condition" : d['weather'][0]['description'].title(),
            "wind"      : d['wind']['speed']
        }

    def news(self, topic, count=3):
        result = self.get(
            "https://newsapi.org/v2/everything",
            params={
                "q"       : topic,
                "apiKey"  : self.config.NEWS_KEY,
                "pageSize": count,
                "sortBy"  : "publishedAt"  # latest pehle
            }
        )
        if not result["success"]:
            return []   # empty list return karo error pe

        # list comprehension — sirf zaroori fields nikalo
        return [
            {
                "title"  : a['title'],
                "source" : a['source']['name'],
                "date"   : a['publishedAt'][:10]  # sirf date, time nahi
            }
            for a in result["data"].get("articles", [])
        ]

    def test_post(self, data):
        # httpbin.org pe POST test karo
        result = self.post(
            "https://httpbin.org/post",
            payload=data
        )
        if result["success"]:
            return result["data"]["json"]  # sent data wapas aata hai
        return result

    def country(self, name):
        result = self.get(
            f"https://restcountries.com/v3.1/name/{name}"
        )
        if not result["success"]:
            return result

        c          = result["data"][0]   # list ka pehla item
        currencies = c.get("currencies", {})
        # dict ka pehla key nikalo — currency code
        currency   = list(currencies.keys())[0] \
                     if currencies else "N/A"
        return {
            "success"    : True,
            "name"       : c['name']['common'],
            "capital"    : c.get('capital', ['N/A'])[0],
            "population" : c.get('population', 0),
            "currency"   : currency,
            "flag"       : c.get('flag', '')
        }

# =============================================
# DISPLAY FUNCTIONS — data ko neatly print karo
# =============================================
def display_weather(w):
    print(f"\n  🌤️  WEATHER — {w.get('city','N/A')}")
    print(f"  {'─'*40}")
    print(f"  Temp      : {w.get('temp')}°C "
          f"(Feels {w.get('feels')}°C)")
    print(f"  Condition : {w.get('condition')}")
    print(f"  Humidity  : {w.get('humidity')}%")
    print(f"  Wind      : {w.get('wind')} m/s")

def display_news(articles, topic):
    print(f"\n  📰  NEWS — {topic.upper()}")
    print(f"  {'─'*40}")
    if not articles:
        print("  No news found.")
        return
    for i, a in enumerate(articles):
        # 55 characters se zyada title cut karo
        title = a['title'][:55] + "..." \
                if len(a['title']) > 55 else a['title']
        print(f"  {i+1}. {title}")
        print(f"     {a['source']} — {a['date']}")

def display_country(c):
    print(f"\n  🌍  COUNTRY — {c.get('name','N/A')}")
    print(f"  {'─'*40}")
    print(f"  Capital    : {c.get('capital')}")
    print(f"  Population : {c.get('population',0):,}")  # comma formatting
    print(f"  Currency   : {c.get('currency')}")
    print(f"  Flag       : {c.get('flag')}")

def save_session(data):
    # unique filename — date aur time se
    filename = f"session_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\n  ✅ Session saved → {filename}")

# =============================================
# MAIN — program ka entry point
# =============================================
def show_menu():
    print(f"\n{'='*45}")
    print(f"   {Config.APP_NAME}")
    print(f"{'='*45}")
    print("  1. Weather lookup")
    print("  2. News search")
    print("  3. Country info")
    print("  4. Test POST request")
    print("  5. API stats")
    print("  0. Exit + save session")
    print(f"{'='*45}")

def main():
    client  = DevToolsClient()   # client object banao
    session = {
        "started"  : datetime.now().strftime("%Y-%m-%d %H:%M"),
        "searches" : []           # is session ki saari searches
    }

    print(f"{'='*45}")
    print(f"  {Config.APP_NAME} — Ready! ✅")
    print(f"  Debug: {Config.DEBUG} | "
          f"Retries: {Config.MAX_RETRIES}")
    print(f"{'='*45}")

    while True:   # jab tak user 0 na dale
        show_menu()
        choice = input("  Choose (0-5): ").strip()

        if choice == "0":
            # session end karo
            session["ended"] = \
                datetime.now().strftime("%Y-%m-%d %H:%M")
            client.stats()    # final stats dikhao
            save = input("\n  Save session? (y/n): ")
            if save.lower() == "y":
                save_session(session)
            print("\n  Goodbye! Keep coding. 💪")
            break   # loop se bahar niklo

        elif choice == "1":
            city = input("  City: ").strip()
            w    = client.weather(city)
            if w.get("success"):
                display_weather(w)
                # session mein add karo
                session["searches"].append(
                    {"type": "weather", "query": city}
                )

        elif choice == "2":
            topic = input("  Topic: ").strip()
            news  = client.news(topic)
            display_news(news, topic)
            session["searches"].append(
                {"type": "news", "query": topic}
            )

        elif choice == "3":
            country = input("  Country: ").strip()
            c       = client.country(country)
            if c.get("success"):
                display_country(c)
                session["searches"].append(
                    {"type": "country", "query": country}
                )

        elif choice == "4":
            print("  Testing POST request...")
            result = client.test_post({
                "name"      : "Samiullah",
                "week"      : 4,
                "skill"     : "API Mastery",
                "timestamp" : datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                )
            })
            print(f"  POST response: {result}")

        elif choice == "5":
            client.stats()   # API usage stats dikhao

        else:
            print("  Invalid choice!")

main()   # program shuru karo