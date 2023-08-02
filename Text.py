import os
from twilio.rest import Client

def send(msg):   
    account_sid = 'REDACTED' 
    auth_token = 'REDACTED'
    client = Client(account_sid, auth_token)
 
    message = client.messages.create(
            body = msg,
            from_='+12056192714',
            to='+REDACTED'
        )
    
