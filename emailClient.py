from smtplib import SMTP as Client
from getpass import getpass


client = Client('52.89.39.119', 8000)

username = input("Enter your username on inscriptio.me: ")
password = getpass()

client.ehlo()
client.starttls()
client.login(username, password)

rcpt = input("Enter the recipient of the email: ")
subject = input("Enter the subject: ")
message = input("Enter the contents of the message: ")

r = client.sendmail(f'{username}@mail.inscriptio.me', [rcpt], f"""\
Subject: {subject}
{message}
""")

print("Email sent successfully!")