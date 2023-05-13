#!/bin/sh

if [ ! -d "env" ]; then
    echo "Creating virtual environment: env"
    python3 -m venv env
    source env/bin/activate
    echo "Upgrading pip..."
    python3 -m pip install --upgrade pip
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "Installing pre-commit hooks..."
    pre-commit install
    echo "Done!"
fi

OPEN_WEATHER_API_KEY=""
TWILIO_ACCOUNT_SID=""
TWILIO_AUTH_TOKEN=""
TWILIO_PHONE_NUMBER=""
POSTGRES_HOST=""
POSTGRES_PORT=""
POSTGRES_DATABASE=""
POSTGRES_USER=""
POSTGRES_PASSWORD=""
if [ ! -f ".env" ]; then
    echo "Creating .env file to store environment variables..."
    touch .env
    echo "OPEN_WEATHER_API_KEY = \"$OPEN_WEATHER_API_KEY\"" >> .env
    echo "TWILIO_ACCOUNT_SID = \"$TWILIO_ACCOUNT_SID\"" >> .env
    echo "TWILIO_AUTH_TOKEN = \"$TWILIO_AUTH_TOKEN\"" >> .env
    echo "TWILIO_PHONE_NUMBER = \"$TWILIO_PHONE_NUMBER\"" >> .env
    echo "POSTGRES_HOST = \"$POSTGRES_HOST\"" >> .env
    echo "POSTGRES_PORT = \"$POSTGRES_PORT\"" >> .env
    echo "POSTGRES_DATABASE = \"$POSTGRES_DATABASE\"" >> .env
    echo "POSTGRES_USER = \"$POSTGRES_USER\"" >> .env
    echo "POSTGRES_PASSWORD = \"$POSTGRES_PASSWORD\"" >> .env
    echo "Done!"
fi