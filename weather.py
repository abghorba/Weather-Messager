# Powered by Dark Sky https://darksky.net/poweredby/
import requests
import json

from connect import connect_db
from config import DarkSkyAuth
from datetime import date, timedelta

API_KEY = DarkSkyAuth.API_KEY
CITY_LAT_LONG = DarkSkyAuth.CITY_LAT_LONG


def default_city():
    """Changes CITY_LAT_LONG back to default"""
    global CITY_LAT_LONG
    CITY_LAT_LONG = DarkSkyAuth.CITY_LAT_LONG


def change_city(latitude, longitude):
    """Changes the city to get weather data from until reset back to default or a new city"""
    global CITY_LAT_LONG
    CITY_LAT_LONG = latitude, longitude


def get_city():
    """Returns the city and state of the current city"""
    cursor = connect_db()
    cursor.execute("SELECT * FROM places WHERE latitude = %s AND longitude = %s", CITY_LAT_LONG)
    city_data = cursor.fetchone()
    city_name = city_data['place_name']
    state = city_data['admin_code1']
    city_state = f"{city_name}, {state}"

    return city_state


def get_weather_data():
    """Makes a GET request to the Dark Sky API"""
    url = "https://api.darksky.net/forecast/{}/{},{}".format(API_KEY, *CITY_LAT_LONG)
    response = requests.get(url)
    data = response.json()

    return data


def get_current_forecast():
    """Parses JSON response to get current forecast"""
    city_state = get_city()
    weather_data = get_weather_data()
    current_weather = weather_data["currently"]
    current_weather_summary = current_weather["summary"].lower()
    current_date = date.strftime(date.today(), '%A')
    chance_of_rain = str(current_weather["precipProbability"]*100) + "%"
    humidity = str(round(current_weather["humidity"]*100)) + "%"
    temperature = str(round(current_weather["temperature"])) + chr(176) + "F"
    icon = weather_data["currently"]["icon"]
    current_forecast = f"It is currently {current_date} in {city_state}. It is {current_weather_summary} with a temperature of {temperature}, a {chance_of_rain} chance of rain, and a humidity of {humidity}."

    return current_forecast, icon


def get_weekly_forecast():
    """Parses JSON response to get weekly forecast"""
    weather_data = get_weather_data()
    weekly_weather = weather_data["daily"]["data"]
    weekday = date.today()
    daily_forecast = ""
    for daily_weather in weekly_weather:
        day = date.strftime(weekday, '%A')
        daily_summary = daily_weather["summary"].replace(".","")
        tempHigh = str(round(daily_weather["temperatureHigh"])) + chr(176) + "F"
        tempLow = str(round(daily_weather["temperatureLow"])) + chr(176) + "F"
        daily_forecast += f"{day}: {daily_summary} with a high of {tempHigh} and a low of {tempLow}. \n"
        weekday += timedelta(days=1)

    weekly_forecast = f"The weekly forecast for{get_city}: \n" + daily_forecast

    return weekly_forecast
    