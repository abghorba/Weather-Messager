from twilio.rest import Client

from src.utilities import MY_NUMBER, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER


def send_message(message, media_url=None):
    """Uses Twilio's API to send an MMS message.

    :param message: Message string to send
    :param media_url: URL to the image to send
    :return: MessageInstance object
    """

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    return client.messages.create(
        to=MY_NUMBER,
        from_=TWILIO_PHONE_NUMBER,
        body=message,
        media_url=[media_url],
    )
