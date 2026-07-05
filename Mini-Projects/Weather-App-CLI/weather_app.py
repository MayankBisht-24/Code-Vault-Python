"""
Weather App (CLI)
------------------
A simple command line tool that fetches live weather data for a city
using the OpenWeatherMap API.

Author: (Mayank Bisht)
"""

import os
import sys
import requests
from dotenv import load_dotenv

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
REQUEST_TIMEOUT = 5  # seconds


def load_api_key():
    """
    Load the OpenWeatherMap API key from the .env file.
    Exits the program if the key is missing.
    """
    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        print("Error: API key not found. Please add OPENWEATHER_API_KEY to your .env file.")
        sys.exit(1)

    return api_key


def get_weather(city, api_key):
    """
    Fetch weather data for the given city from the OpenWeatherMap API.

    Args:
        city (str): Name of the city entered by the user.
        api_key (str): OpenWeatherMap API key.

    Returns:
        dict: Weather data in JSON format if the request is successful.
        None: If the request fails for any reason (error is printed to console).
    """
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # get temperature in Celsius directly
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the internet. Please check your connection.")

    except requests.exceptions.Timeout:
        print("Error: The request timed out. Please try again.")

    except requests.exceptions.HTTPError:
        if response.status_code == 401:
            print("Error: Invalid API key. Please check your .env file.")
        elif response.status_code == 404:
            print(f"Error: City '{city}' not found. Please check the spelling.")
        else:
            print(f"Error: Something went wrong (status code {response.status_code}).")

    except requests.exceptions.RequestException as e:
        print(f"Unexpected error occurred: {e}")

    return None


def display_weather(data):
    """
    Format and print the weather details on the screen.

    Args:
        data (dict): Weather data returned by the API.
    """
    city = data["name"]
    country = data["sys"]["country"]
    temperature = round(data["main"]["temp"])
    feels_like = round(data["main"]["feels_like"])
    condition = data["weather"][0]["main"]
    description = data["weather"][0]["description"].title()
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    pressure = data["main"]["pressure"]
    visibility_km = data.get("visibility", 0) / 1000  # meters to km

    # sunrise and sunset come as unix timestamps, convert using the city's own timezone offset
    from datetime import datetime, timezone, timedelta

    tz_offset = data["timezone"]
    local_tz = timezone(timedelta(seconds=tz_offset))

    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"], tz=local_tz).strftime("%I:%M %p")
    sunset = datetime.fromtimestamp(data["sys"]["sunset"], tz=local_tz).strftime("%I:%M %p")

    print()
    print(f"City          : {city}")
    print(f"Country       : {country}")
    print(f"Temperature   : {temperature}°C")
    print(f"Feels Like    : {feels_like}°C")
    print(f"Condition     : {condition}")
    print(f"Description   : {description}")
    print(f"Humidity      : {humidity}%")
    print(f"Wind Speed    : {wind_speed} m/s")
    print(f"Pressure      : {pressure} hPa")
    print(f"Visibility    : {visibility_km:.0f} km")
    print(f"Sunrise       : {sunrise}")
    print(f"Sunset        : {sunset}")
    print()


def main():
    """
    Program entry point. Handles user input and controls the overall flow.
    """
    print("=" * 30)
    print("        Weather App")
    print("=" * 30)

    api_key = load_api_key()

    city = input("\nEnter City Name: ").strip()

    if not city:
        print("Error: City name cannot be empty.")
        return

    weather_data = get_weather(city, api_key)

    if weather_data:
        display_weather(weather_data)


if __name__ == "__main__":
    main()