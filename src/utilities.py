import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MY_NUMBER = os.getenv("MY_NUMBER")


class OpenWeatherAPICredentials:
    def __init__(self):
        self.api_key = os.getenv("OPEN_WEATHER_API_KEY")

    @property
    def empty_credentials(self):
        """Returns True if credentials are empty; False otherwise."""

        return not bool(self.api_key)


class TwilioCredentials:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.phone_number = os.getenv("TWILIO_PHONE_NUMBER")

    @property
    def empty_credentials(self):
        """Returns True if any credential is empty; False otherwise."""

        return not (bool(self.account_sid) and bool(self.auth_token) and bool(self.phone_number))


class PostgresCredentials:
    def __init__(self):
        self.host = os.getenv("POSTGRES_HOST")
        self.port = os.getenv("POSTGRES_PORT")
        self.database = os.getenv("POSTGRES_DATABASE")
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")

    @property
    def empty_credentials(self):
        """Returns True if any credential is empty; False otherwise."""

        return not (
            bool(self.host) and bool(self.port) and bool(self.database) and bool(self.user) and bool(self.password)
        )
