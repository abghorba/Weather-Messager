from sms import send_sms, send_mms
from weather import get_current_forecast, get_weekly_forecast

# Send the current forecast to outgoing phone number.
current_forecast, icon = get_current_forecast()
send_mms(current_forecast, icon, "3236056084")

# Send weekly forecast to outgoing phone number.
#weekly_forecast = get_weekly_forecast()
#send_sms(weekly_forecast, "phone_number")