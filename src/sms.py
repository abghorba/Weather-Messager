from twilio.rest import Client

from src.utilities import MY_NUMBER, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_sms(message):
    """Uses Twilio's API to send an SMS message.

    :param message: Message string to send
    :return: MessageInstance object
    """

    return client.messages.create(to=MY_NUMBER, from_=TWILIO_PHONE_NUMBER, body=message)


def send_mms(message, media_url):
    """Uses Twilio's API to send an MMS message.

    :param message: Message string to send
    :param media_url: URL to the image to send
    :return: MessageInstance object
    """

    return client.messages.create(
        to=MY_NUMBER,
        from_=TWILIO_PHONE_NUMBER,
        body=message,
        media_url=[media_url],
    )
