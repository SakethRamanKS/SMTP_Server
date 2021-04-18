from modules.auth.auth import Authenticator
from modules.mail.sendMx import sendMailMx
from modules.mail.sendgrid import sendMailSendgrid

from aiosmtpd.controller import Controller
from aiosmtpd.smtp import AuthResult, SMTP

import asyncio

import ssl

# Setting up SSL
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain('/etc/letsencrypt/live/inscriptio.me/fullchain.pem', '/etc/letsencrypt/live/inscriptio.me/privkey.pem')

username = ''
subdomain = 'mail.inscriptio.me'

def validateFrom(from_email):
    from_email = from_email.replace(f'@{subdomain}', '')
    print(from_email)
    global username
    if username == from_email:
        return True
    return False

class SmtpRelayHandler:

    async def auth_PLAIN(self, server, argList):
        import base64
        print("Auth plain called")
        cred = base64.b64decode(argList[1])
        cred = list(map(chr, cred))

        index2 = cred[1:].index('\x00') + 1
        index1 = 0

        global username
        username = ''.join((cred[index1+1:index2]))
        password = ''.join((cred[index2+1:]))

        auth = Authenticator()

        authResult = auth.validateCredentials("PLAIN", (username, password))
        return authResult
    
    async def handle_DATA(self, server, session, envelope):

        if not validateFrom(envelope.mail_from):
            return '454 Temporary Authentication Failure'

        if sendMailMx(envelope):
            print("Mail sent successfully through mx method")

        # Normal send through MX servers did not work, sending using the Sendgrid API
        else:
            print("Using sendgrid")
            if sendMailSendgrid(envelope):
                print("Mail sent successfully through Sendgrid")
                return '250 Message accepted for delivery'
            else:
                print("Sendgrid seems to be down")
                return '554 Sendgrid API error'

        

class ControllerTls(Controller):
    def factory(self):
        return SMTP(self.handler, tls_context=context)

async def main():
    relayHandler = SmtpRelayHandler()
    con = ControllerTls(handler = relayHandler, hostname = '', port = 8000)
    con.start()
    print(f"Server running on {con.hostname} on port {con.port}")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Terminating program")
