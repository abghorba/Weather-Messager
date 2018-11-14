<h1> Welcome to my Weather Messager! </h1>

<h2> <u>Requirements to set up:</u> </h2>

You need to sign up at Twilio and get an account_sid and auth_token to use in the app and get a free number.
Note: The SMS and MMS will all begin with a "Sent from your Twilio trial account - " if you
have a trial account. You can pay for the service to get rid of this.

You will also need to get an API key from Dark Sky as well to use the app.


<h3> Setting up your database </h3>
Firstly, you will need to create a PostgreSQL database to connect to. Then execute the following SQL command:

        CREATE TABLE places ( country_code char(2), postal_code varchar(20), place_name varchar(180), admin_name1 varchar(100), admin_code1 varchar(20), admin_name2 varchar(100), admin_code2 varchar(20), admin_name3 varchar(100), admin_code3 varchar(20), latitude NUMERIC, longitude NUMERIC, accuracy varchar(1))

Now we need to populate the table using the US.txt file. We will use the terminal to do this. First, if you don't have this set up (this part is for Mac OS):

        brew install postgresql

To check that it installed correctly run:

        postgres --version

Now we need to connect to the database! Run the following command, filling in the blanks!

        psql --host="" --port=5432 --username="" --password --dbname=""

You will be prompted for your password! If successful you will now be able to run commands on your PostgreSQL database! Now to populate the tables run the following command, and supplying the path to the US.txt file!

        \copy places from {path to US.txt} with DELIMITER E’\t’

You should get returned COPY 41440 if successful. Now the database is set up!


<h3> Setting up your config file </h3>
Create a file called config.py with the following structure and fill in the blanks. You will need the latitude and longitude of the city
you wish to be the default (query the database for it!) and enter them below in default_lat and default_long, respectively.

    class MyNumber:
        MY_NUMBER = ''

    class TwilioAuth:
        ACCOUNT_SID = ''
        AUTH_TOKEN = ''
        TWILIO_NUMBER = ''

    class DarkSkyAuth:
        API_KEY = ''
        CITY_LAT_LONG = default_lat, default_long

    class PostgresAuth:
        DB_HOST= ''
        DB_USER= '' 
        DB_PASSWORD= ''
        DB_NAME= ''


<h3> Setting up Twilio number </h3>
With all this, you can deploy this Flask app to AWS Elastic Beanstalk, or Heroku, etc. Copy the URL you created!
Then you must:
1) Go to your Twilio console
2) Go to phone numbers
3) Click on your phone number
4) Scroll down and under Voice & Fax find "A Call Comes In" and copy and paste your URL with a /call after it and make sure the HTTP request is POST!
5) Do the same as #4 for "Messaging" and have a /sms after your URL!

Your app should be configured!


<h2> What the app does! </h2>
Text your Twilio number CURRENT if you want the current forecast!
Text your Twilio number WEEKLY if you want the weekly forecast!
Text your Twilio number CHANGE <ZIP_CODE> to change the city. Currently, this only supports using zip codes in the US. TODO: adding the feature for typing in a US city!

You can even call your Twilio number for a nice surprise! :)
