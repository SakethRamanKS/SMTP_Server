from smtplib import SMTP as Client
client = Client('::1', 8000)

client.login("test", "abc")
r = client.sendmail('test@parse.inscriptio.me', ['sakethramansundaram78@gmail.com'], """\
From: Anne Person <anne@example.com>
To: Bart Person <bart@example.com>
Subject: It works
It works!!!
""")
