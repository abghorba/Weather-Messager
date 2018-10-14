# Twilio's API can be found https://www.twilio.com/docs/usage/api
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
account_sid = ''
auth_token = ''
my_twilio_number = ''
client = Client(account_sid, auth_token)

def send_sms(text, outgoing):
    """Uses Twilio's API to send an SMS message."""
    message = client.messages \
        .create(
             body = text,
             from_ = my_twilio_number,
             to ='+1' + outgoing.replace("-","").replace("(","").replace(")","")
         )



def send_mms(text, pic_icon, outgoing):
    """Uses Twilio's API to send an MMS message."""
    message = client.messages.create(
                                  body = text,
                                  media_url = "https://darksky.net/images/weather-icons/{}.png".format(pic_icon),
                                  from_ = my_twilio_number,
                                  to ='+1' + outgoing
                              )