def send_notif(twilio_sid, twilio_sid_token, from_number, to_number, text):
    from twilio.rest import Client
    client = Client(twilio_sid, twilio_sid_token)

    client.messages.create(body=text,
                           from_= f'whatsapp:{from_number}',
                           to= f'whatsapp:{to_number}')