# =============================================
# MINI PROJECT — Config Validator
# =============================================
import os
from dotenv import load_dotenv

load_dotenv()

class AppConfig:

    REQUIRED_KEYS = [
        "WEATHER_API_KEY",
        "NEWS_API_KEY"
    ]

    OPTIONAL_KEYS = {
        "APP_NAME"    : "My App",
        "DEBUG_MODE"  : "False",
        "MAX_RETRIES" : "3",
        "TIMEOUT"     : "5"
    }

    def __init__(self):
        self._validate()
        self._load()

    def _validate(self):
        missing = [
            k for k in self.REQUIRED_KEYS
            if not os.getenv(k)
        ]
        if missing:
            raise EnvironmentError(
                f"\n❌ Missing required keys:\n"
                + "\n".join(f"  - {k}" for k in missing)
                + "\n\nAdd them to your .env file!"
            )

    def _load(self):
        # Required
        self.weather_key = os.getenv("WEATHER_API_KEY")
        self.news_key    = os.getenv("NEWS_API_KEY")

        # Optional with defaults
        self.app_name    = os.getenv(
            "APP_NAME",
            self.OPTIONAL_KEYS["APP_NAME"]
        )
        self.debug       = os.getenv(
            "DEBUG_MODE",
            self.OPTIONAL_KEYS["DEBUG_MODE"]
        ) == "True"
        self.max_retries = int(os.getenv(
            "MAX_RETRIES",
            self.OPTIONAL_KEYS["MAX_RETRIES"]
        ))
        self.timeout     = int(os.getenv(
            "TIMEOUT",
            self.OPTIONAL_KEYS["TIMEOUT"]
        ))

    def display(self):
        print(f"\n{'='*40}")
        print(f"  APP CONFIGURATION")
        print(f"{'='*40}")
        print(f"  App Name    : {self.app_name}")
        print(f"  Debug Mode  : {self.debug}")
        print(f"  Max Retries : {self.max_retries}")
        print(f"  Timeout     : {self.timeout}s")
        print(f"  Weather Key : {self.weather_key[:6]}****")
        print(f"  News Key    : {self.news_key[:6]}****")
        print(f"{'='*40}")

# --- TEST ---
try:
    config = AppConfig()
    config.display()
    print("\n✅ App ready to run!")
except EnvironmentError as e:
    print(e)