from twilio.rest import Client

from src.utilities import TwilioAuth


class TwilioHandler:
    def __init__(self):
        self.twilio_auth = TwilioAuth()
        self.client = Client(self.twilio_auth.account_sid, self.twilio_auth.auth_token)

    def send_message(self, message, outgoing_number, media_url=None):
        """Uses Twilio's API to send an MMS message.

        :param message: Message string to send
        :param outgoing_number: Number to send the message to
        :param media_url: URL to the image to send
        :return: MessageInstance object
        """

        return self.client.messages.create(
            to=outgoing_number,
            from_=self.twilio_auth.phone_number,
            body=message,
            media_url=[media_url],
        )
