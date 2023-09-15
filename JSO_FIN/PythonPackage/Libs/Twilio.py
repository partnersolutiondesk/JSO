# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure

account_sid = "AC6028e8d4d5cd65efe693b7de8885fe72"
auth_token = "2934e22bfa5a2738295452fbb7506871"
client = Client(account_sid, auth_token)

call = client.calls.create(
  url="http://demo.twilio.com/docs/voice.xml",
  to="+917909140656",
  from_="+17079407687"
)

print(call.sid)