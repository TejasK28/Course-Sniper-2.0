import os
from twilio.rest import Client

def send(msg):   
    account_sid = 'AC2c60b74c483f1166e6a24a7ad388368e' 
    auth_token = '3edf3ebf68382e44f8edfec9e91b9d43'
    client = Client(account_sid, auth_token)
 
    message = client.messages.create(
            body = msg,
            from_='+18449594235',
            to='+18482563099'
        )
    
send('hihi')
    
