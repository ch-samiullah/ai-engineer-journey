import requests
import json

# first api call
print("\n--5 random quotes---")
for i in range(5):
    response = requests.get("https://api.quotable.io/random")
    if response.status_code == 200:
        data = response.json()
        print(f"Quote {i+1}: {data['content']} - {data['author']}")
    else:
        print(f"Error: {response.status_code}")
        #country api
        print("\n--pakistan info")
response = requests.get("https://restcountries.com/v3.1/name/pakistan")
response =requests.get(url)
if response.status_code == 200:
    data = response.json()
    country_info = data[0]
    print(f"Country: {country_info['name']['common']}")
    print(f"Capital: {country_info['capital'][0]}")
    print(f"Population: {country_info['population']}")
else:    print(f"Error: {response.status_code}")