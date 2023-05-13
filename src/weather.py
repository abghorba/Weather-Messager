from datetime import date, datetime, timedelta

import requests
from pytz import timezone

from database.execute_sql import PostgresDatabaseHandler
from src.utilities import OpenWeatherAuth


class OpenWeatherAPIHandler:
    def __init__(self, default_latitude=33.684566, default_longitude=-117.826508):
        """Defaults to Irvine, CA."""

        self.open_weather_auth = OpenWeatherAuth()
        self.default_latitude = default_latitude
        self.default_longitude = default_longitude
        self.current_latitude = self.default_latitude
        self.current_longitude = self.default_longitude
        self.current_city = self._get_city()

    def _get_city(self):
        """Returns the city and state of the current city"""

        # Execute query to database
        db_handler = PostgresDatabaseHandler()
        sql = "SELECT * FROM places WHERE latitude BETWEEN %s AND %s AND longitude BETWEEN %s AND %s"

        # Execute with a margin of safety so we don't have to be extremely precise with latitude/longitude coordinates
        margin_of_safety = 0.01
        params = (
            self.current_latitude - margin_of_safety,
            self.current_latitude + margin_of_safety,
            self.current_longitude - margin_of_safety,
            self.current_longitude + margin_of_safety,
        )
        db_handler.execute_sql(sql_queries=sql, query_params=params)

        # Get data from the query result
        city_data = db_handler.cursor.fetchone()
        city_name = city_data["place_name"]
        state = city_data["admin_code1"]
        city_state = f"{city_name}, {state}"

        # Close connection to database
        db_handler.close_database_connection()

        return city_state

    def change_city(self, latitude, longitude):
        """Changes the city to get weather data from until reset back to default or a new city"""
        self.current_latitude, self.current_longitude = latitude, longitude
        self.current_city = self._get_city()

    def change_city_to_default(self):
        self.change_city(self.default_latitude, self.default_longitude)

    def get_weather_data(self):
        """Makes a GET request to the Dark Sky API"""

        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={self.current_latitude}&lon={self.current_longitude}&appid={self.open_weather_auth.api_key}"
        )

        response = requests.get(url)
        if response.status_code != 200:
            return None

        data = response.json()
        return data

    def get_current_forecast(self):
        """Parses JSON response to get current forecast"""

        weather_data = self.get_weather_data()

        if not weather_data:
            return "Error getting weather data!", None

        tz = weather_data["timezone"]
        current_weather = weather_data["currently"]
        current_weather_summary = current_weather["summary"].lower()
        current_date = date.strftime(datetime.now(timezone(tz)), "%A, %b. %d, %Y")
        chance_of_rain = str(current_weather["precipProbability"] * 100) + "%"
        humidity = str(round(current_weather["humidity"] * 100)) + "%"
        temperature = str(round(current_weather["temperature"])) + chr(176) + "F"
        icon = weather_data["currently"]["icon"]
        current_forecast = (
            f"It is currently {current_date} in {self.current_city}. "
            f"It is {current_weather_summary} with a temperature of {temperature}, a {chance_of_rain} "
            f"chance of rain, and a humidity of {humidity}."
        )

        return current_forecast, icon

    def get_weekly_forecast(self):
        """Parses JSON response to get weekly forecast"""

        weather_data = self.get_weather_data()

        if not weather_data:
            return "Error getting weather data!", None

        tz = weather_data["timezone"]
        weekly_weather = weather_data["daily"]["data"]
        weekday = datetime.now(timezone(tz))
        daily_forecasts = []
        for daily_weather in weekly_weather:
            day = date.strftime(weekday, "%A")
            daily_summary = daily_weather["summary"].replace(".", "")
            temp_hi = str(round(daily_weather["temperatureHigh"])) + chr(176) + "F"
            temp_lo = str(round(daily_weather["temperatureLow"])) + chr(176) + "F"
            daily_forecasts.append(f"{day}: {daily_summary} with a high of {temp_hi} and a low of {temp_lo}. \n")
            weekday += timedelta(days=1)

        weekly_forecast = f"The weekly forecast for {self.current_city}: \n{''.join(daily_forecasts)}"

        return weekly_forecast, None
