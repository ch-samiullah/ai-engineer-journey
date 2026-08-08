# =============================================
# MINI PROJECT — Professional API Wrapper
# =============================================
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

class ProAPIClient:

    def __init__(self, rate_limit_delay=1, max_retries=3):
        self.delay       = rate_limit_delay
        self.max_retries = max_retries
        self.call_count  = 0
        self.session     = requests.Session()
        self.session.headers.update({
            "User-Agent": "Samiullah-Pro/1.0"
        })

    def get(self, url, params=None):
        for attempt in range(1, self.max_retries + 1):
            try:
                # Rate limiting
                if self.call_count > 0:
                    time.sleep(self.delay)

                response = self.session.get(
                    url,
                    params=params,
                    timeout=5
                )
                self.call_count += 1
                response.raise_for_status()
                return {"success": True,
                        "data"   : response.json()}

            except requests.exceptions.HTTPError:
                if response.status_code == 429:
                    wait = self.delay * (2 ** attempt)
                    print(f"Rate limited — waiting {wait}s")
                    time.sleep(wait)
                elif response.status_code >= 500:
                    time.sleep(self.delay * attempt)
                else:
                    return {"success": False,
                            "error"  : response.status_code}

            except requests.exceptions.Timeout:
                time.sleep(self.delay * attempt)

            except requests.exceptions.ConnectionError:
                return {"success": False,
                        "error"  : "No internet!"}

        return {"success": False,
                "error"  : "Max retries reached"}

    def stats(self):
        print(f"Total API calls made: {self.call_count}")


# --- USE IT ---
client      = ProAPIClient(rate_limit_delay=1, max_retries=3)
WEATHER_KEY = os.getenv("WEATHER_API_KEY")

cities = ["Rawalpindi", "Lahore", "Karachi","islamabad","Rawat"]

print("=" * 45)
print("  PRO API CLIENT — Weather Fetcher")
print("=" * 45)

for city in cities:
    result = client.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "q"     : city,
            "appid" : WEATHER_KEY,
            "units" : "metric"
        }
    )
    if result["success"]:
        d = result["data"]
        print(f"{city:15} → "
              f"{d['main']['temp']}°C | "
              f"{d['weather'][0]['description'].title()}")
    else:
        print(f"{city:15} → Error: {result['error']}")

client.stats()