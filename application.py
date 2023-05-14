from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse

from database.execute_sql import PostgresDatabaseHandler
from src.send_message import TwilioHandler
from src.weather import OpenWeatherAPIHandler

# Initialize Flask app
application = Flask(__name__)
database_handler = PostgresDatabaseHandler()
twilio = TwilioHandler()


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

    # Set to default values for message and media_url
    outgoing_message = (
        "Sorry, I was not able to understand your request.\n"
        "If you want the current forecast text CURRENT.\n"
        "If you want the weekly forecast text WEEKLY.\n"
        "To change cities, text CHANGE <POSTAL CODE>.\n"
        "To change back your default city, text DEFAULT."
    )
    media_url = None

    # Check if the incoming number has been seen before
    sql = "SELECT * FROM users WHERE phone_number = %s;"
    params = (incoming_number,)
    database_handler.execute_sql(sql_queries=sql, query_params=params)
    user_data = database_handler.cursor.fetchone()

    # We've never seen this number before
    if not user_data:
        if "register" in incoming_message:
            try:
                _, postal_code = incoming_message.split()

                # Query places table to find city by postal code
                sql = "SELECT latitude, longitude FROM places WHERE postal_code LIKE %s;"
                params = (postal_code,)
                database_handler.execute_sql(sql_queries=sql, query_params=params)

                city_data = database_handler.cursor.fetchone()
                default_latitude = float(city_data[0])
                default_longitude = float(city_data[1])

                # Update the users table with the new user's default location
                sql = (
                    "INSERT INTO users (phone_number, default_latitude, default_longitude, current_latitude, "
                    "current_longitude) VALUES (%s, %s, %s, %s, %s);"
                )
                params = (incoming_number, default_latitude, default_longitude, default_latitude, default_longitude)
                database_handler.execute_sql(sql_queries=sql, query_params=params)

                outgoing_message = (
                    "Success! You've been registered. You may use the following commands:\n"
                    "If you want the current forecast text CURRENT.\n"
                    "If you want the weekly forecast text WEEKLY.\n"
                    "To change cities, text CHANGE <POSTAL CODE>.\n"
                    "To change back your default city, text DEFAULT."
                )

            except:
                outgoing_message = "Invalid format! To register, text REGISTER <ZIP CODE>."

        else:
            outgoing_message = (
                "Hello, you must be new! In order to use this application, please text REGISTER <ZIP CODE>."
            )

    # We've seen this number before, we can continue on
    else:
        # Set up the OpenWeatherAPIHandler instance with the correct coordinates
        default_latitude = user_data["default_latitude"]
        default_longitude = user_data["default_longitude"]
        current_latitude = user_data["current_latitude"]
        current_longitude = user_data["current_longitude"]
        weather_api = OpenWeatherAPIHandler(default_latitude, default_longitude)

        # Change cities if needed
        if current_latitude != default_latitude or current_longitude != default_longitude:
            weather_api.change_city(current_latitude, current_longitude)

        # Determine appropriate message and media_url for user request
        if "current" in incoming_message:
            outgoing_message, media_url = weather_api.get_current_forecast()

        elif "weekly" in incoming_message:
            outgoing_message = weather_api.get_weekly_forecast()

        elif "change" in incoming_message:
            try:
                _, postal_code = incoming_message.split()

                # Query places table to find city by postal code
                sql = "SELECT latitude, longitude FROM places WHERE postal_code LIKE %s;"
                params = (postal_code,)
                database_handler.execute_sql(sql_queries=sql, query_params=params)

                city_data = database_handler.cursor.fetchone()
                new_latitude = float(city_data[0])
                new_longitude = float(city_data[1])

                # Change location
                weather_api.change_city(new_latitude, new_longitude)
                outgoing_message = f"Changed city to: {weather_api.current_city}"

                # Update the users table with the new current location
                sql = "UPDATE users SET current_latitude = %s, current_longitude = %s WHERE phone_number = %s;"
                params = (new_latitude, new_longitude, incoming_number)
                database_handler.execute_sql(sql_queries=sql, query_params=params)

            except:
                outgoing_message = "Invalid format! To change cities, text CHANGE <ZIP CODE>."

        elif "default" in incoming_message:
            weather_api.change_city_to_default()
            outgoing_message = f"City changed back to default city: {weather_api.current_city}"

    # Send the message back to the user
    twilio.send_message(outgoing_message, outgoing_number=incoming_number, media_url=media_url)

    # Close the database connection
    database_handler.close_database_connection()

    return outgoing_message


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
