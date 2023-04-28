# Twilio's API can be found https://www.twilio.com/docs/usage/api
# Custom import
from config import MyNumber, TwilioAuth
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
account_sid = TwilioAuth.ACCOUNT_SID
auth_token = TwilioAuth.AUTH_TOKEN
my_twilio_number = TwilioAuth.TWILIO_NUMBER
outgoing_number = MyNumber.MY_NUMBER.replace("-", "").replace("(", "").replace(")", "")

client = Client(account_sid, auth_token)


def send_sms(text):
    """Uses Twilio's API to send an SMS message."""
    message = client.messages.create(body=text, from_=my_twilio_number, to="+1{}".format(outgoing_number))


def send_mms(text, pic_icon):
    """Uses Twilio's API to send an MMS message."""
    message = client.messages.create(
        body=text,
        media_url="https://darksky.net/images/weather-icons/{}.png".format(pic_icon),
        from_=my_twilio_number,
        to="+1{}".format(outgoing_number),
    )
