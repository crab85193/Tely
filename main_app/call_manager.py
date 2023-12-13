import os
from twilio.rest import Client

class CallManager:
    def __init__(self):
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.__client = Client(account_sid, auth_token)

    def call(self, message, phone_number):
        _twiml = self.create_say_response_xml(message)
        _from  = os.environ.get("FROM_PHONE_NUMBER")
        _to    = f"+81{phone_number[1:]}"

        call = self.__client.calls.create(twiml=_twiml, to=_to, from_=_from)

        return call.sid

    def gather(self, message, phone_number, action):
        _twiml = self.create_gather_response_xml(message, action)
        _from  = os.environ.get("FROM_PHONE_NUMBER")
        _to    = f"+81{phone_number[1:]}"

        call = self.__client.calls.create(
            twiml=_twiml,
            to=_to,
            from_=_from
        )

        return call.sid
    
    def create_say_response_xml(self, message):
        response  = f'<Response>'
        response += f'<Say language="ja-jp">{message}</Say>'
        response += f'</Response>'

        return response
    
    def create_gather_response_xml(self, message, action):
        response  = f'<Response>'
        response += f'<Gather numDigits="1" action="{action}" method="POST">'
        response += f'<Say language="ja-jp">{message}</Say>'
        response += f'</Gather>'
        response += f'</Response>'

        return response
    
    def get_balance(self):
        balance = self.__client.api.balance.fetch()
        return balance.balance
