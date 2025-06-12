from twilio.rest import Client
import datetime as dt
from datetime import datetime
from datetime import timedelta
import time


# Twilio credentials
account_sid = 'AC36765affa8322dcc0248b1ae1a40cd49'
auth_token = 'd742c1ffe0f67c773fa91e7e63519724'

client = Client(account_sid, auth_token)


def send_message(recipient_number, message_body):
    try:
        message = client.messages.create(
            from_= 'whatsapp:+14155238886',
            body = message_body,
            to = f'whatsapp:{recipient_number}'

        )

        print(f'message sent succesfully! messege SID{message.sid}')
    except Exception as e:
        print(f'Error sending message: {e}')  


name = input('enter your name:')
recipient_number = input('enter the recipient whatsapp number with cntry code:')
message_body = input(f'enter the message you want to send to {name}:')


date_str = input('enter the date you want to send the message in YYYY-MM-DD format:')
time_str = input('enter the time you want to send the message in HH:MM format:')

sheduled_time = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M')
now = datetime.now()

time_difference = sheduled_time - now
delay_seconds = time_difference.total_seconds()
if delay_seconds < 0:
    print('the scheduled time is in the past. please enter a future date and time.')
else:
    print(f'message will be sent in {delay_seconds} seconds.')
    time.sleep(delay_seconds)
    send_message(recipient_number, message_body)