#!/usr/bin/env python3

import sys
import requests
import notify2
from datetime import datetime

city = sys.argv[1] if len(sys.argv) > 1 else "Timisoara"
date = sys.argv[2] if len(sys.argv) > 2 else datetime.now().strftime("%Y-%m-%d")
time = sys.argv[3] if len(sys.argv) > 3 else datetime.now().strftime("%H:00")

WMO = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

# 1. Get coordinates from city name
geo_url = "https://geocoding-api.open-meteo.com/v1/search"
geo_params = {"name": city, "count": 1}
geo_res = requests.get(geo_url, params=geo_params).json()

if "results" in geo_res:
    lat = geo_res["results"][0]["latitude"]
    lon = geo_res["results"][0]["longitude"]

    # 2. Get weather data
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,weathercode,apparent_temperature",
    }

    target_time = datetime.strptime(f"{date}T{time}", "%Y-%m-%dT%H:%M").strftime("%Y-%m-%dT%H:00")

    weather_res = requests.get(weather_url, params=weather_params).json()

    if "hourly" in weather_res:
        for i, time in enumerate(weather_res["hourly"]["time"]):
            if time == target_time:
                 break
        temp = weather_res["hourly"]["temperature_2m"][i]
        feels = weather_res["hourly"]["apparent_temperature"][i]
        weather_code = weather_res["hourly"]["weathercode"][i]

        human_readable_time = datetime.strptime(target_time, "%Y-%m-%dT%H:%M").strftime("%d %B, %H:00")
        time = human_readable_time + ":" if target_time!=datetime.now().strftime("%Y-%m-%dT%H:00") else human_readable_time + " (Now)"
        weather_info = f"{city}\n{time}\n{temp}°C, Feels like: {feels}°C\nWeather: {WMO.get(weather_code, 'Unknown')}   "

        print("Weather:", weather_info)

        # 3. Cross-platform notification
        notify2.init("Weather Notification")
        n = notify2.Notification("Weather Notification", weather_info)
        n.show()
    else:
        print("Weather data not found")
else:
    print("City not found")