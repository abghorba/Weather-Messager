from twilio.rest import Client

from src.utilities import TwilioAuth


class TwilioHandler:
    def __init__(self):
        try:
            self.twilio_auth = TwilioAuth()
            self.client = Client(self.twilio_auth.account_sid, self.twilio_auth.auth_token)
            self.client.incoming_phone_numbers.list()
            print("Authentication to Twilio successful")
            self.successful_auth = True

        except Exception as e:
            print(f"Authentication to Twilio unsuccessful: {str(e)}")
            self.successful_auth = False

    def send_message(self, outgoing_message, outgoing_number, media_url=None):
        """Uses Twilio's API to send an MMS message.

        :param outgoing_message: Message string to send
        :param outgoing_number: Number to send the message to
        :param media_url: URL to the image to send
        :return: MessageInstance object
        """

        if not self.successful_auth:
            print("Cannot send message because authentication was unsuccessful!")
            return

        return self.client.messages.create(
            to=outgoing_number,
            from_=self.twilio_auth.phone_number,
            body=outgoing_message,
            media_url=[media_url],
        )
