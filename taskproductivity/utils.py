from os import getenv
from mailjet_rest import Client

def send_email(sender, sender_name, to, to_name, subject, HTMLPart):
    # Might need to refactor this into a separate util function
    api_key = getenv("MAILJET_KEY")
    api_secret = getenv("MAILJET_SECRET")
    print(f"api_key: {api_key}")
    print(f"api_secret: {api_secret}")
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
            "From": {
                "Email": sender,
                "Name": sender_name
            },
            "To": [
                {
                "Email": to,
                "Name": to_name
                }
            ],
            "Subject": subject,
            "TextPart": "My first Mailjet email",
            "HTMLPart": HTMLPart,
            "CustomID": "AppGettingStartedTest"
            }
        ]
    }

    return mailjet.send.create(data=data)