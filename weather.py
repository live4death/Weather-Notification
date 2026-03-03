#!/usr/bin/env python3

import webview
import weatherNotification

class Api:
    def get_weather(self, city, day, time):
        return weatherNotification.get_weather()

webview.create_window(
    "Weather App",
    "index.html",
    width=700,
    height=400,
    resizable=False
)

webview.start()