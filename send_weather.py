# Imports
from flask import Flask, render_template, request, redirect
from twilio.twiml.voice_response import VoiceResponse

# Custom imports
from config import MyNumber
from sms import send_sms, send_mms
from weather import get_current_forecast, get_weekly_forecast

# Initialize Flask app
application = Flask(__name__)


@application.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@application.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    if request.method == "POST":
        # Get the message the user sent our Twilio number
        text_message = request.values.get('Body', None)

        # Determine the right reply for this message
        if text_message.lower() == 'current':
            # Send the current forecast to outgoing phone number
            current_forecast, icon = get_current_forecast()
            send_mms(current_forecast, icon, MyNumber.MY_NUMBER)
        elif text_message.lower() == 'weekly':
            # Send weekly forecast to outgoing phone number.
            weekly_forecast = get_weekly_forecast()
            send_sms(weekly_forecast, MyNumber.MY_NUMBER)
        elif text_message.lower()[:6] == 'change':
            # Change location
            send_sms("Feature in progress!", MyNumber.MY_NUMBER)
        elif text_message[0] == ' ':
            # Return error message 1
            error_message1 = ("Make sure you don't have a leading space!",
                              "If you want the current forecast text CURRENT.",
                              "If you want the weekly forecast text WEEKLY.",
                              "To change cities, text CHANGE <POSTAL CODE> or CHANGE <CITY, STATE>.")
            send_sms(error_message1, MyNumber.MY_NUMBER)
        else:
            # Return error message 2
            error_message2 = ("Make sure you don't have a leading space!",
                              "If you want the current forecast text CURRENT.",
                              "If you want the weekly forecast text WEEKLY.",
                              "To change cities, text CHANGE <POSTAL CODE> or CHANGE <CITY, STATE>.")
            send_sms(error_message2, MyNumber.MY_NUMBER)

        return True
    
    elif request.method == "GET":
        return redirect("/")


@application.route("/call", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls and mention the caller's city"""
    if request.method == "POST":
        # Start our TwiML response
        resp = VoiceResponse()

        # Play an audio file for the caller
        resp.play('https://demo.twilio.com/docs/classic.mp3')

        return str(resp)

    elif request.method == "GET":
        return redirect("/")


if __name__ == "__main__":
    application.run()