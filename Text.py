import os
from twilio.rest import Client

def send(msg):   
    account_sid = 'AC163f8f196b6a64211e0d77d03301fd5a' 
    auth_token = 'ceb3f404973bc4a9b3488fb0ae34fb86'
    client = Client(account_sid, auth_token)
 
    message = client.messages.create(
            body = msg,
            from_='+12056192714',
            to='+18482563099'
        )
    
