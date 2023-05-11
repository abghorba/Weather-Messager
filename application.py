# Imports
import psycopg2
import psycopg2.extras

# Custom imports
from config import PostgresAuth
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse

from src.send_message import send_message
from src.weather import change_city, default_city, get_city, get_current_forecast, get_weekly_forecast

# Initialize Flask app
application = Flask(__name__)

ERROR_MESSAGE = (
    "Sorry, I was not able to understand your request.\n"
    "If you want the current forecast text CURRENT.\n"
    "If you want the weekly forecast text WEEKLY.\n"
    "To change cities, text CHANGE <POSTAL CODE>."
)


@application.route("/sms", methods=["POST"])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""

    # Connect to PostgreSQL database
    db = psycopg2.connect(**PostgresAuth.PARAMS)
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Get the message the user sent our Twilio number
    incoming_message = request.values.get("Body", None).strip().lower()
    message = ERROR_MESSAGE
    media_url = None

    if "current" in incoming_message:
        message, media_url = get_current_forecast()

    elif "weekly" in incoming_message:
        message = get_weekly_forecast()

    elif "change" in incoming_message:
        try:
            _, postal_code = incoming_message.split()

            # Query database to find city by postal code
            cursor.execute("SELECT latitude, longitude FROM places WHERE postal_code LIKE %s", (postal_code,))
            city_data = cursor.fetchone()
            latitude = float(city_data[0])
            longitude = float(city_data[1])

            # Change location
            change_city(latitude, longitude)
            message = f"Changed city to: {get_city()}"
        except:
            message = "Invalid format. To change cities, text CHANGE <POSTAL CODE>."

    elif "default" in incoming_message:
        default_city()
        message = f"City changed back to default city: {get_city()}"

    send_message(message, media_url)

    # Close database connection
    cursor.close()
    db.close()

    return message


@application.route("/call", methods=["POST"])
def voice():
    """Respond to incoming phone calls and mention the caller's city"""

    # Start our TwiML response
    resp = VoiceResponse()

    # Play an audio file for the caller
    resp.play("https://demo.twilio.com/docs/classic.mp3")

    return "Call successful"


if __name__ == "__main__":
    application.run()
