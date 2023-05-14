import pytest

from application import application
from src.utilities import OpenWeatherAPICredentials, PostgresCredentials

application.config["TESTING"] = True


@pytest.mark.skipif(OpenWeatherAPICredentials().empty_credentials, reason="Open Weather API Key not provided!")
@pytest.mark.skipif(PostgresCredentials().empty_credentials, reason="PostgreSQL Database credentials not provided!")
class TestApplication:
    def test_incoming_sms(self):
        pass
