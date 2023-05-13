import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
MY_NUMBER = os.getenv("MY_NUMBER")


class PostgresAuth:
    def __init__(self):
        self.host = os.getenv("POSTGRES_HOST")
        self.database = os.getenv("POSTGRES_DATABASE")
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
