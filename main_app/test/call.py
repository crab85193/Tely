import os
import json
from twilio.rest import Client
from dotenv import load_dotenv
# .envファイルの内容を読み込見込む
load_dotenv(".env")

json_open = open('call_data.json', 'r')
voice_data=json.load(json_open)

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
voice_data["voice"]
call = client.calls.create(
                        twiml=f'<Response><Say>{voice_data["voice"]}</Say></Response>',
                        to=voice_data["to_number"],
                        from_=voice_data["from_number"]
                    )
print(call.sid)