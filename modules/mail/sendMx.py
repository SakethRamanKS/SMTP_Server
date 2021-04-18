from smtplib import SMTP as SMTPClient
import dns.resolver

timeoutDuration = 2

def getMxRecord(domainName):
    mxRecords = dns.resolver.resolve(domainName, "MX")
    if not mxRecords:
        return None
    mxRecords = sorted(mxRecords, key = lambda record: record.preference)
    firstRecord = mxRecords[0].exchange
    return str(firstRecord)

def sendMailMx(envelope):
    recptMx = {}
    for rcpt in envelope.rcpt_tos:
        atPos = rcpt.index('@')
        domainName = rcpt[atPos+1:]
        mx = getMxRecord(domainName)
        if mx is None:
            continue
        if mx not in recptMx:
            recptMx[mx] = []
        recptMx[mx].append(rcpt)

    for mx, rcpts in recptMx.items():
        try:
            client = SMTPClient(mx, 25, timeout = timeoutDuration)
        except OSError:
            return False
        client.starttls()
        client.sendmail(from_addr = envelope.mail_from, to_addrs = rcpts, msg = envelope.original_content)
    return True