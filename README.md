<h1> Welcome to my Weather Messager! </h1>

<h2> <u>Requirements to set up:</u> </h2>

You need to sign up at Twilio and get an account_sid and auth_token to use in the app and get a free number.
Note: The SMS and MMS will all begin with a "Sent from your Twilio trial account - " if you
have a trial account. You can pay for the service to get rid of this.

You will also need to get an API key from Dark Sky as well to use the app.

Create a file called config.py with the following structure and fill in the blanks.

    class MyNumber:
        MY_NUMBER = ''

    class TwilioAuth:
        ACCOUNT_SID = ''
        AUTH_TOKEN = ''
        TWILIO_NUMBER = ''

    class DarkSkyAuth:
        API_KEY = ''

Finally, you will need the latitude and longitude of whatever city you are interested in getting forecasted. And enter those coordinates in weather.py

With all this, you can deploy this Flask app to AWS Elastic Beanstalk, or Heroku, etc. Copy the URL you created!
Then you must:
1) Go to your Twilio console
2) Go to phone numbers
3) Click on your phone number
4) Scroll down and under Voice & Fax find "A Call Comes In" and copy and paste your URL with a /call after it and make sure the HTTP request is POST!
5) Do the same as #4 for "Messaging" and have a /sms after your URL!

Your app should be configured!

<h2> What the app does! </h2>
Text the app "current" if you want the current forecast!
Text the app "weekly" if you want the weekly forecast!
You can even call your Twilio number for a nice surprise! :)
