import pytest

from application import application
from database.execute_sql import PostgresDatabaseHandler
from src.utilities import OpenWeatherAPICredentials, PostgresCredentials

application.config["TESTING"] = True


@pytest.fixture(scope="session", autouse=True)
def delete_test_user_from_database():
    """Deletes the test user from the users table at the end of this module."""

    yield
    database_handler = PostgresDatabaseHandler()
    sql = "DELETE FROM users WHERE phone_number = '+1234567890';"
    database_handler.execute_sql(sql, close_connection=True)


@pytest.mark.skipif(OpenWeatherAPICredentials().empty_credentials, reason="Open Weather API Key not provided!")
@pytest.mark.skipif(PostgresCredentials().empty_credentials, reason="PostgreSQL Database credentials not provided!")
class TestApplication:
    @pytest.mark.parametrize(
        "incoming_message,expected_message",
        [
            (
                {"Body": "Hello?", "From": ""},
                "ERROR: No incoming message or number found!",
            ),
            (
                {"Body": "", "From": "+1234567890"},
                "ERROR: No incoming message or number found!",
            ),
            (
                {"Body": "Hello?", "From": "+1234567890"},
                "Hello, you must be new! In order to use this application, please text REGISTER <ZIP CODE>.",
            ),
            (
                {"Body": "REGISTER 1A2B3", "From": "+1234567890"},
                "Invalid format! To register, text REGISTER <ZIP CODE>.",
            ),
            (
                {"Body": "REGISTER 94102", "From": "+1234567890"},
                "Success! You've been registered. You may use the following commands:\n"
                "If you want the current forecast text CURRENT.\n"
                "If you want the weekly forecast text WEEKLY.\n"
                "To change cities, text CHANGE <POSTAL CODE>.\n"
                "To change back your default city, text DEFAULT.",
            ),
            (
                {"Body": "Hello?", "From": "+1234567890"},
                "Sorry, I was not able to understand your request.\n"
                "If you want the current forecast text CURRENT.\n"
                "If you want the weekly forecast text WEEKLY.\n"
                "To change cities, text CHANGE <POSTAL CODE>.\n"
                "To change back your default city, text DEFAULT.",
            ),
            # (
            #     {"Body": "CURRENT", "From": "+1234567890"},
            #     "",
            # ),
            # (
            #     {"Body": "WEEKLY", "From": "+1234567890"},
            #     "",
            # ),
            (
                {"Body": "CHANGE 1A2B3", "From": "+1234567890"},
                "Invalid format! To change cities, text CHANGE <ZIP CODE>.",
            ),
            (
                {"Body": "CHANGE 92612", "From": "+1234567890"},
                "Changed city to: Irvine, CA",
            ),
            (
                {"Body": "DEFAULT", "From": "+1234567890"},
                "City changed back to default city: San Francisco, CA",
            ),
        ],
    )
    def test_incoming_sms(self, incoming_message, expected_message):
        """Tests the /sms app route."""

        response = application.test_client().post("/sms", data=incoming_message)
        assert response.data.decode("utf-8") == expected_message
