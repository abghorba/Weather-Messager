from config import MyNumber
from sms import send_sms, send_mms
from weather import get_current_forecast, get_weekly_forecast

## Testing text reponses ##
body = ' ange banana'

# Determine the right reply for this message
if body.lower() == 'current':
    # Send the current forecast to outgoing phone number
    current_forecast, icon = get_current_forecast()
    print(current_forecast)
elif body.lower() == 'weekly':
    # Send weekly forecast to outgoing phone number.
    weekly_forecast = get_weekly_forecast()
    print(weekly_forecast)
elif body.lower()[:6] == 'change':
    # Change location
    print("Feature in progress!")
elif body[0] == ' ':
    # Return error message 1
    print("Make sure you don't have a leading space!",
          "If you want the current forecast text CURRENT.",
          "If you want the weekly forecast text WEEKLY.",
          "To change cities, text CHANGE <POSTAL CODE> or CHANGE <CITY, STATE>.")
else:
    # Return error message 2
    print("If you want the current forecast text CURRENT.",
          "If you want the weekly forecast text WEEKLY.",
          "To change cities, text CHANGE <POSTAL CODE> or CHANGE <CITY, STATE>.")


## Testing SMS ##
error_message1 = "hello world!"
send_sms(error_message1)