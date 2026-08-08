# =============================================
# MINI PROJECT — Country Explorer
# =============================================
import requests

def get_country(name):
    try:
        url      = f"https://restcountries.com/v3.1/name/{name}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()[0]
    except requests.exceptions.HTTPError:
        return None
    except requests.exceptions.ConnectionError:
        return {"error": "No internet!"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out!"}

def display_country(country):
    if not country:
        print("Country not found!")
        return
    if "error" in country:
        print(country["error"])
        return

    # safely get currency
    currencies = country.get("currencies", {})
    currency   = list(currencies.keys())[0] if currencies else "N/A"
    curr_name  = currencies[currency]["name"] if currencies else "N/A"

    # safely get languages
    languages  = list(country.get("languages", {}).values())

    print(f"\n{'='*40}")
    print(f"  {country['name']['common'].upper()}")
    print(f"{'='*40}")
    print(f"  Capital    : {country.get('capital', ['N/A'])[0]}")
    print(f"  Population : {country.get('population', 0):,}")
    print(f"  Region     : {country.get('region', 'N/A')}")
    print(f"  Currency   : {currency} — {curr_name}")
    print(f"  Languages  : {', '.join(languages)}")
    print(f"  Flag       : {country.get('flag', '')}")
    print(f"{'='*40}")

def main():
    print("=" * 40)
    print("     COUNTRY EXPLORER")
    print("=" * 40)

    while True:
        name = input("\nEnter country name (or 'quit'): ").strip()
        if name.lower() == "quit":
            print("Goodbye!")
            break
        if not name:
            print("Please enter a country name!")
            continue
        country = get_country(name)
        display_country(country)

main()