import os
from datetime import datetime


from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv


load_dotenv()


account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)

print(datetime.utcnow())


def schedule_message():
    try:
        message = client.messages \
            .create(
                messaging_service_sid = os.getenv('TWILIO_MSG_SRVC_SID'),
                to = 'YOUR_NUMBER',
                body = 'Ahoy, world! This is a scheduled message in Python.',
                schedule_type = 'fixed',
                send_at = datetime(2023, 3, 4, 3, 40, 10)
            )
        print(message.sid)
    except TwilioRestException as e:
        print(e)


schedule_message()