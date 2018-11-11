# Powered by Dark Sky https://darksky.net/poweredby/
import requests
import json

from config import DarkSkyAuth
from datetime import date, timedelta

API_KEY = DarkSkyAuth.API_KEY
CITY_LAT_LONG = 33.6846, -117.8265 # Irvine, CA

url = "https://api.darksky.net/forecast/{}/{},{}".format(API_KEY, *CITY_LAT_LONG)
response = requests.get(url)
weather_data = response.json()



def get_current_forecast():
    """Uses Dark Sky API to get the current forecast"""
    current_weather = weather_data["currently"]
    current_weather_summary = current_weather["summary"].lower()
    current_date = date.strftime(date.today(), '%A')
    chance_of_rain = str(current_weather["precipProbability"]*100) + "%"
    humidity = str(round(current_weather["humidity"]*100)) + "%"
    temperature = str(round(current_weather["temperature"])) + chr(176) + "F"
    icon = weather_data["currently"]["icon"]
    current_forecast = "It is currently {}. It is {} with a temperature of {}, a {} chance of rain, and a humidity of {}.".format(current_date, current_weather_summary, temperature, chance_of_rain, humidity)

    return current_forecast, icon



def get_weekly_forecast():
    """Uses Dark Sky API to get the weekly forecast"""
    weekly_weather = weather_data["daily"]["data"]
    weekday = date.today()
    daily_forecast = ""
    for daily_weather in weekly_weather:
        day = date.strftime(weekday, '%A')
        daily_summary = daily_weather["summary"].replace(".","")
        tempHigh = str(round(daily_weather["temperatureHigh"])) + chr(176) + "F"
        tempLow = str(round(daily_weather["temperatureLow"])) + chr(176) + "F"
        daily_forecast += "{}: {} with a high of {} and a low of {}. ".format(day, daily_summary, tempHigh, tempLow) + "\n"
        weekday += timedelta(days=1)

    weekly_forecast = "The weekly forecast: \n" + daily_forecast

    return weekly_forecast