from os import getenv
from mailjet_rest import Client
from datetime import datetime


def send_email(email_data, template_id):
    # Might need to refactor this into a separate util function
    api_key = getenv("MAILJET_KEY")
    api_secret = getenv("MAILJET_SECRET")
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    variables = None

    # Different data to send to mailjet for different templates
    if template_id == 3221171:
        variables = {
                "password_reset_button": email_data["password_reset_button"],
                "password_reset_link": email_data["password_reset_link"],
            }
    elif template_id == 3930904 or template_id == 3936662:
         variables = {
                "day_num": email_data["day_num"],
            }

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
                "Variables": variables
            }
        ]
    }
    return mailjet.send.create(data=data)

def convert_to_timestamp(entry, renewal, online_start, online_end, departure=None, reported_date=None):
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
    
    if departure is not None:
        if not isinstance(departure, datetime):
            departure = datetime.combine(departure, datetime.min.time())
        departure = datetime.timestamp(departure)
    
    if reported_date is not None:
        if not isinstance(reported_date, datetime):
            reported_date = datetime.combine(reported_date, datetime.min.time())
        reported_date = datetime.timestamp(reported_date)

    if departure == None and reported_date == None:
        return entry, renewal, online_start, online_end
    else:
        return entry, renewal, online_start, online_end, departure, reported_date

