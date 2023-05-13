from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse

from database.execute_sql import PostgresDatabaseHandler
from src.send_message import send_message
from src.weather import OpenWeatherAPIHandler

# Initialize Flask app
application = Flask(__name__)
database_handler = PostgresDatabaseHandler()
weather_api = OpenWeatherAPIHandler()

ERROR_MESSAGE = (
    "Sorry, I was not able to understand your request.\n"
    "If you want the current forecast text CURRENT.\n"
    "If you want the weekly forecast text WEEKLY.\n"
    "To change cities, text CHANGE <POSTAL CODE>."
)


@application.route("/sms", methods=["POST"])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""

    incoming_message = request.values.get("Body", None)
    incoming_number = request.values.get("From", None)

    if not (incoming_message and incoming_number):
        return "ERROR: No incoming message or number found!"

    # Clean the incoming data
    incoming_message = incoming_message.lower().strip()
    incoming_number = incoming_number.lower().strip()

    message = ERROR_MESSAGE
    media_url = None

    if "current" in incoming_message:
        message, media_url = weather_api.get_current_forecast()

    elif "weekly" in incoming_message:
        message = weather_api.get_weekly_forecast()

    elif "change" in incoming_message:
        try:
            _, postal_code = incoming_message.split()

            # Query database to find city by postal code
            sql = "SELECT latitude, longitude FROM places WHERE postal_code LIKE %s"
            params = (postal_code,)
            database_handler.execute_sql(sql_queries=sql, query_params=params)

            city_data = database_handler.cursor.fetchone()
            latitude = float(city_data[0])
            longitude = float(city_data[1])

            # Change location
            weather_api.change_city(latitude, longitude)
            message = f"Changed city to: {weather_api.current_city}"

        except:
            message = "Invalid format. To change cities, text CHANGE <POSTAL CODE>."

    elif "default" in incoming_message:
        weather_api.change_city_to_default()
        message = f"City changed back to default city: {weather_api.current_city}"

    send_message(message, media_url)
    database_handler.close_database_connection()

    return message


@application.route("/call", methods=["POST"])
def incoming_call():
    """Respond to incoming phone calls"""

    # Start our TwiML response
    resp = VoiceResponse()

    # Play an audio file for the caller
    resp.play("https://demo.twilio.com/docs/classic.mp3")

    return "Call successful"


if __name__ == "__main__":
    application.run()
