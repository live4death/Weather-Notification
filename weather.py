#!/usr/bin/env python3

import webview
import json
import requests
from datetime import datetime

WMO = {
    0: {"name": "Clear sky", "emoji": "☀️"},
    1: {"name": "Mainly clear", "emoji": "🌤️"},
    2: {"name": "Partly cloudy", "emoji": "⛅"},
    3: {"name": "Overcast", "emoji": "☁️"},
    45: {"name": "Fog", "emoji": "🌫️"},
    48: {"name": "Depositing rime fog", "emoji": "🌫️"},
    51: {"name": "Light drizzle", "emoji": "🌦️"},
    53: {"name": "Moderate drizzle", "emoji": "🌦️"},
    55: {"name": "Dense drizzle", "emoji": "🌧️"},
    56: {"name": "Light freezing drizzle", "emoji": "🌧️"},
    57: {"name": "Dense freezing drizzle", "emoji": "🌧️"},
    61: {"name": "Slight rain", "emoji": "🌧️"},
    63: {"name": "Moderate rain", "emoji": "🌧️"},
    65: {"name": "Heavy rain", "emoji": "🌧️"},
    66: {"name": "Light freezing rain", "emoji": "🌧️"},
    67: {"name": "Heavy freezing rain", "emoji": "🌧️"},
    71: {"name": "Slight snow", "emoji": "🌨️"},
    73: {"name": "Moderate snow", "emoji": "🌨️"},
    75: {"name": "Heavy snow", "emoji": "❄️"},
    77: {"name": "Snow grains", "emoji": "❄️"},
    80: {"name": "Slight rain showers", "emoji": "🌦️"},
    81: {"name": "Moderate rain showers", "emoji": "🌦️"},
    82: {"name": "Violent rain showers", "emoji": "⛈️"},
    85: {"name": "Slight snow showers", "emoji": "🌨️"},
    86: {"name": "Heavy snow showers", "emoji": "❄️"},
    95: {"name": "Thunderstorm", "emoji": "⛈️"},
    96: {"name": "Thunderstorm with slight hail", "emoji": "⛈️"},
    99: {"name": "Thunderstorm with heavy hail", "emoji": "⛈️"},
}

class Api:
    def get_weather_info(self, city, time, date):
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {"name": city, "count": 1}
        geo_res = requests.get(geo_url, params=geo_params).json()
        
        if "results" in geo_res:
            lat = geo_res["results"][0]["latitude"]
            lon = geo_res["results"][0]["longitude"]

        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,weathercode,apparent_temperature,wind_speed_10m",
        }

        target_date = datetime.strptime(date, "%Y-%m-%d")
        target_date = target_date.replace(year=datetime.now().year)
        if time == "now":
            target_time = datetime.now()
        else:
            target_time = datetime.strptime(time, "%H:00") 
        # target_time = datetime.now().strftime("%Y-%m-%dT%H:00")
        target_datetime = target_date.strftime("%Y-%m-%d") + "T" + target_time.strftime("%H:00")
        weather_res = requests.get(weather_url, params=weather_params).json()

        if "hourly" in weather_res:
            for i, time in enumerate(weather_res["hourly"]["time"]):
                if time == target_datetime:
                    break

        temp = round(weather_res["hourly"]["temperature_2m"][i])
        feels = weather_res["hourly"]["apparent_temperature"][i]
        weather_code = weather_res["hourly"]["weathercode"][i]
        wind_speed = weather_res["hourly"]["wind_speed_10m"][i]
        condition = WMO.get(weather_code, {"name": "Unknown", "emoji": ""})

        maxTemps = {}

        time = target_time.strftime("%H:00");

        if "hourly" in weather_res:
            for timeStr, temperature in zip(weather_res["hourly"]["time"], weather_res["hourly"]["temperature_2m"]):
                dateFor = datetime.fromisoformat(timeStr).date()

                if dateFor not in maxTemps or temperature > maxTemps[dateFor]:
                    maxTemps[dateFor] = temperature

        print(maxTemps)

        return {
            "temperature": temp,
            "feeling": feels,
            "wind": wind_speed,
            "condition": condition,
            "time": time
        }
    
    def get_available_cities(self):
        european_capitals = [
            "Vienna", "Brussels", "Sofia", "Zagreb", "Nicosia", "Prague", "Copenhagen", 
            "Tallinn", "Helsinki", "Paris", "Berlin", "Athens", "Budapest", "Reykjavik", 
            "Dublin", "Rome", "Riga", "Vaduz", "Vilnius", "Luxembourg", "Valletta", 
            "Chisinau", "Monaco", "Podgorica", "Amsterdam", "Skopje", "Oslo", "Warsaw", 
            "Lisbon", "Bucharest", "Moscow", "San Marino", "Belgrade", "Bratislava", 
            "Ljubljana", "Madrid", "Stockholm", "Bern", "Kiev", "London"]

        romanian_cities = [
            "Bucharest", "Cluj-Napoca", "Timișoara", "Iași", "Constanța", "Craiova", 
            "Brașov", "Galați", "Ploiești", "Oradea", "Brăila", "Arad", "Pitești", 
            "Sibiu", "Bacău", "Târgu Mureș", "Baia Mare", "Buzău", "Satu Mare", 
            "Râmnicu Vâlcea", "Drobeta-Turnu Severin", "Suceava", "Piatra Neamț", 
            "Târgu Jiu", "Focșani", "Botoșani", "Rădăuți", "Reșița", "Hunedoara"]

        all_cities = european_capitals + romanian_cities
        all_cities = sorted(list(set(all_cities)))
        
        return all_cities
    
api = Api()

webview.create_window(
    "Weather App",
    "index.html",
    js_api=api,
    width=960,
    height=760,
    resizable=False
)

webview.start(debug=True)