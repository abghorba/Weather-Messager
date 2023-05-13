import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class OpenWeatherAuth:
    def __init__(self):
        self.api_key = os.getenv("OPEN_WEATHER_API_KEY")


class TwilioAuth:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.phone_number = os.getenv("TWILIO_PHONE_NUMBER")


class PostgresAuth:
    def __init__(self):
        self.host = os.getenv("POSTGRES_HOST")
        self.port = os.getenv("")
        self.database = os.getenv("POSTGRES_DATABASE")
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
