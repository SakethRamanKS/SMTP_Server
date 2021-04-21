from dotenv import load_dotenv
import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from email import message_from_bytes
from email.policy import default

load_dotenv()

def sendMailSendgrid(envelope):
    """Sends an email using the Sendgrid API"""
    try:
        # Creating a Sendgrid Client
        message = message_from_bytes(envelope.content, policy=default)
        api_key = os.environ.get('SENDGRID_API_KEY')
        sgClient = sendgrid.SendGridAPIClient(api_key)

        # Preparing the email for delivery
        from_email = Email(envelope.mail_from)
        subject = message['Subject']
        mail_content = str(message).replace(f"Subject: {subject}", '').strip()
        content = Content("text/plain", mail_content)

        for rcpt in envelope.rcpt_tos:
            to_email = To(rcpt)
            mail = Mail(from_email, to_email, subject, content)
            print(mail)
            mail_json = mail.get()
            # Sending the email
            response = sgClient.client.mail.send.post(request_body=mail_json)
            print(response.status_code)
            print(response.headers)
        
        return True
        
    except Exception as e:
        return False