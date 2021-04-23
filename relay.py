# Implements a relay server that receives mails from a client using SMTP
# The mail is then forwarded to the appropriate destination

"""userdefined modules"""
from modules.auth.auth import Authenticator
from modules.mail.sendMx import sendMailMx
from modules.mail.sendgrid import sendMailSendgrid

"""built-in modules"""
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import AuthResult, SMTP

import ssl

# Setting up SSL
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain('/etc/letsencrypt/live/inscriptio.me/fullchain.pem', '/etc/letsencrypt/live/inscriptio.me/privkey.pem')

#subdomain registered in namecheap(domain name inscriptio.me)
username = ''
subdomain = 'mail.inscriptio.me'

def validateFrom(from_email):
    """Validating the username"""
    from_email = from_email.replace(f'@{subdomain}', '')
    print(from_email)
    global username
    if username == from_email:
        return True
    return False

class SmtpRelayHandler:

    async def auth_PLAIN(self, server, argList):
        """Handles authentication by verifying that the user is regsitered"""
        import base64
        print("Auth plain called")
        cred = base64.b64decode(argList[1])
        cred = list(map(chr, cred))

        index2 = cred[1:].index('\x00') + 1                #credentials returned is like 'abc\x00bcd'
        index1 = 0

        global username
        username = ''.join((cred[index1+1:index2]))
        password = ''.join((cred[index2+1:]))

        auth = Authenticator()

        authResult = auth.validateCredentials("PLAIN", (username, password))
        return authResult
    
    async def handle_DATA(self, server, session, envelope):
        """Attempts to forward the email to the intended recipient
            If the email server is accessible, an SMTP connection is established and the mail is delivered
            Otherwise the Sendgrid API is used to relay the mail"""
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

async def startRelayServer():
    """Function that starts the SMTP relay server by creating instances of SMTPRelayHandler and ControlleeTls"""
    relayHandler = SmtpRelayHandler()
    con = ControllerTls(handler = relayHandler, hostname = '', port = 8000)
    con.start()
    print(f"Relay Server running on port {con.port}")


