from os import getenv
from mailjet_rest import Client
from datetime import datetime

def send_email(email_data, template_id):
    # Might need to refactor this into a separate util function
    api_key = getenv("MAILJET_KEY")
    api_secret = getenv("MAILJET_SECRET")
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": email_data["sender"],
                    "Name": email_data["sender_name"],
                },
                "To": [
                    {
                        "Email": email_data["to"],
                        "Name": email_data["to_name"],
                    }
                ],
                "TemplateID": template_id,
                "TemplateLanguage": True,
                "Subject": email_data["subject"],
                "Variables": {
                    "password_reset_button": email_data["password_reset_button"],
                    "password_reset_link": email_data["password_reset_link"],
                }
            }
        ]
    }
    return mailjet.send.create(data=data)

def convert_to_timestamp(entry, renewal, online_start, online_end):
    if entry is not None:
        if not isinstance(entry, datetime):
            entry = datetime.combine(entry, datetime.min.time())
        entry = datetime.timestamp(entry)
    
    if renewal is not None:
        if not isinstance(renewal, datetime):
            renewal = datetime.combine(renewal, datetime.min.time())
        renewal = datetime.timestamp(renewal)
    
    if online_start is not None:
        if not isinstance(online_start, datetime):
            online_start = datetime.combine(online_start, datetime.min.time())
        online_start = datetime.timestamp(online_start)
    
    if online_end is not None:
        if not isinstance(online_end, datetime):
            online_end = datetime.combine(online_end, datetime.min.time())
        online_end = datetime.timestamp(online_end)

    return entry, renewal, online_start, online_end