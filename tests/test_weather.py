import pytest

from src.utilities import OpenWeatherAPICredentials, PostgresCredentials


@pytest.mark.skipif(OpenWeatherAPICredentials().empty_credentials, reason="Open Weather API Key not provided!")
@pytest.mark.skipif(PostgresCredentials().empty_credentials, reason="PostgreSQL Database credentials not provided!")
class TestOpenWeatherAPIHandler:
    def test_get_city(self):
        """Tests OpenWeatherAPIHandler._get_city()."""

        pass

    def test_change_city(self):
        """Tests OpenWeatherAPIHandler.change_city()."""

        pass

    def test_change_city_to_default(self):
        """Tests OpenWeatherAPIHandler.change_city_to_default()."""

        pass

    def test_get_weather_data(self):
        """Tests OpenWeatherAPIHandler.get_weather_data()."""

        pass

    def test_get_current_forecast(self):
        """Tests OpenWeatherAPIHandler.get_current_forecast()."""

        pass

    def test_get_weekly_forecast(self):
        """Tests OpenWeatherAPIHandler.get_weekly_forecast()."""

        pass
