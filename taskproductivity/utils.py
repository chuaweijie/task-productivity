from os import getenv
from mailjet_rest import Client

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