import os 
from dotenv import load_dotenv
from datetime import time

import requests
load_dotenv()
weather_key = os.getenv("WEATHER_KEY")
NEWS_KEY = os.getenv("NEWS_KEY")

#api1-weather
def get_weather(city):
    params = {
        "q": city,
        "appid": weather_key,
        "units": "metric"
    }
    try:
        r = requests.get("http://api.openweathermap.org/data/2.5/weather", params=params, timeout=5)
        r.raise_for_status()
        d = r.json()
        return {
            "city": d.get("name"),
            "temp": d["main"]["temp"],
            "feels": d["main"]["feels_like"],
            "humidity": d["main"]["humidity"],
            "condition": d["weather"][0]["description"].title(),
            "wind": d["wind"]["speed"]
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")
        return []

#api2
def get_new(topic, count=3):
    params ={
        "q": topic,
        "apiKey": NEWS_KEY,
        "pageSize": count
    }
    try:
        r = requests.get("https://newsapi.org/v2/everything", params=params, timeout=5)
        r.raise_for_status()
        d = r.json()
        return [
            {
                "title": article["title"],
                "description": article["description"],
                "url": article["url"]
            }
            for article in d["articles"]
        ]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

#api 3
def get_qouts():
    try:
        r = requests.get("https://api.quotable.io/random", timeout=5)
        r.raise_for_status()
        d = r.json()
        return {
            "content": d["content"],
            "author": d["author"]
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching quote: {e}")
        return []

# display
def display_info(city,topic,weather,name,qoutes):
    print(f"Weather in {city}:")
    print(f"Temperature: {weather['temp']}°C, Feels like: {weather['feels']}°C, Humidity: {weather['humidity']}%, Condition: {weather['condition']}, Wind Speed: {weather['wind']} m/s\n")
    
    print(f"News on {topic}:")
    for article in name:
        print(f"- {article['title']}\n  {article['description']}\n  Read more: {article['url']}\n")
    
    print("Quote of the day:")
    print(f"{qoutes['content']} - {qoutes['author']}")

# save to file
def save_to_file(city, topic, weather, news, quote):
    with open("info.txt", "w") as f:
        f.write(f"Weather in {city}:\n")
        f.write(f"Temperature: {weather['temp']}°C, Feels like: {weather['feels']}°C, Humidity: {weather['humidity']}%, Condition: {weather['condition']}, Wind Speed: {weather['wind']} m/s\n\n")
        f.write(f"News on {topic}:\n")
        for article in news:
            f.write(f"- {article['title']}\n  {article['description']}\n  Read more: {article['url']}\n")
        f.write(f"\nQuote of the day:\n")
        f.write(f"{quote['content']} - {quote['author']}\n")

#main
def main():
    city = input("Enter a city for weather info: ")
    topic = input("Enter a topic for news: ")
    
    weather = get_weather(city)
    news = get_new(topic)
    quote = get_qouts()
    
    display_info(city, topic, weather, news, quote)
    save = input("Do you want to save this information to a file? (yes/no): ")
    if save.lower() == "yes":
        save_to_file(city, topic, weather, news, quote)
        main()

if __name__ == "__main__":
    main()