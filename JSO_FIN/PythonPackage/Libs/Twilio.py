# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure

account_sid = "AC7cc150681032e3e8c4cf123ed4dddd36" #"AC6028e8d4d5cd65efe693b7de8885fe72"
auth_token = "3096a51d8f650ac38927d3b1c212c54f" #"2934e22bfa5a2738295452fbb7506871"
client = Client(account_sid, auth_token)

call = client.calls.create(
  twiml='<Response><Say voice="woman">Hey, New offers for you!Please check out your email for more details. Thank you</Say></Response>',
  to="+918157897518",
  from_="+14786062504"
)
"""
call = client.calls.create(
  url="http://demo.twilio.com/docs/voice.xml",
  to="+917909140656",
  from_="+17079407687"
)
"""
#print(call.sid)