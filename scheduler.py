import os
from datetime import datetime
from datetime import timedelta


from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv


load_dotenv()


account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)


def schedule_message(to_number, minutes, body):
    try:
        message = client.messages \
            .create(
                messaging_service_sid = os.getenv('TWILIO_MSG_SRVC_SID'),
                to = to_number,
                body = body,
                schedule_type = 'fixed',
                send_at = minutes_from_now(minutes)
            )
        print(message.sid)
    except TwilioRestException as e:
        print(e)
        raise


def minutes_from_now(minutes):
    if (minutes > 15 and minutes < 10080):
        return datetime.utcnow() + timedelta(minutes=minutes)
    else:
        print('Message must be scheduled more than 15 minutes and fewer than 7 days in advance.')


# schedule_message('+1XXXXXXXXXX', 16, 'Ahoy, world! This is another scheduled message in Python.')
