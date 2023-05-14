import pytest

from src.send_message import TwilioMessageHandler
from src.utilities import MY_NUMBER, TwilioCredentials

TEST_IMG_URL = (
    "https://legendary-digital-network-assets.s3.amazonaws.com/wp-content/uploads/2020/07/13032616/maxresdefault.jpg"
)


@pytest.mark.skipif(TwilioCredentials().empty_credentials, reason="Twilio credentials not provided!")
class TestTwilioMessageHandler:
    twilio = TwilioMessageHandler()

    @pytest.mark.skipif(
        condition=not twilio.successful_auth,
        reason="Cannot test TwilioMessageHandler because authentication to Twilio was not successful.",
    )
    @pytest.mark.parametrize(
        "receiving_number,text_message,image_url",
        [
            (MY_NUMBER, "Hi! This is is a test SMS.", None),
            (MY_NUMBER, "Hi! This is is a test MMS.", TEST_IMG_URL),
        ],
    )
    def test_send_message(self, receiving_number, text_message, image_url):
        """Tests TwilioMessageHandler.send_message()."""

        message_sid = self.twilio.send_message(receiving_number, text_message, image_url)
        assert len(message_sid) == 34

        if image_url:
            assert message_sid.startswith("MM")

        else:
            assert message_sid.startswith("SM")
