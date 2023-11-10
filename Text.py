import os
from twilio.rest import Client

def send(msg):   
    account_sid = 'RED' 
    auth_token = 'RED'
    client = Client(account_sid, auth_token)
 
    message = client.messages.create(
            body = msg,
            from_='+RED',
            to='+RED'
        )
    
send('hihi')
    
