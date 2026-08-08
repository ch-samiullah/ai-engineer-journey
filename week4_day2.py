# =============================================
# MINI PROJECT — Secure Multi API Manager
# =============================================
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class SecureAPIManager:

    def __init__(self):
        self.keys = {
            "weather" : os.getenv("WEATHER_API_KEY"),
            "news"    : os.getenv("NEWS_API_KEY")
        }
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Samiullah-SecureApp/1.0"
        })

    def validate_keys(self):
        missing = [k for k, v in self.keys.items() if not v]
        if missing:
            raise ValueError(f"Missing API keys: {missing}")
        return True

    def make_request(self, method, url, **kwargs):
        try:
            kwargs['timeout'] = kwargs.get('timeout', 5)
            response = self.session.request(
                method, url, **kwargs
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.HTTPError as e:
            return {"success": False,
                    "error": f"HTTP {response.status_code}"}
        except requests.exceptions.ConnectionError:
            return {"success": False,
                    "error": "No internet!"}
        except requests.exceptions.Timeout:
            return {"success": False,
                    "error": "Timed out!"}

    def weather(self, city):
        return self.make_request(
            "GET",
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q"     : city,
                "appid" : self.keys["weather"],
                "units" : "metric"
            }
        )

    def news(self, topic, count=3):
        return self.make_request(
            "GET",
            "https://newsapi.org/v2/everything",
            params={
                "q"       : topic,
                "apiKey"  : self.keys["news"],
                "pageSize": count,
                "sortBy"  : "publishedAt"
            }
        )

# --- TEST ---
try:
    manager = SecureAPIManager()
    manager.validate_keys()

    print("=" * 45)
    print("   SECURE API MANAGER — TEST")
    print("=" * 45)

    # Weather
    w = manager.weather("Islamabad")
    if w["success"]:
        d = w["data"]
        print(f"\nWeather in Islamabad:")
        print(f"  Temp      : {d['main']['temp']}°C")
        print(f"  Condition : "
              f"{d['weather'][0]['description'].title()}")

    # News
    n = manager.news("Pakistan Technology")
    if n["success"]:
        print(f"\nLatest Pakistan Tech News:")
        for i, a in enumerate(n["data"]["articles"]):
            print(f"  {i+1}. {a['title'][:55]}...")

    print("\n✅ All APIs working securely!")

except ValueError as e:
    print(f"❌ Error: {e}")