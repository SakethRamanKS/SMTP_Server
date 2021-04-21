def extractDetails(request):
    """Extracts the fromId, toId, subject and body from a received mail"""
    from_email = request.form['from']
    to_email = request.form['to']
    subject = request.form['subject']
    body =  request.form['text']
    username = to_email[:to_email.index('@')]
    
    fromMailId = from_email
    if '<' in from_email:
        angledBracketIndex = from_email.index('<')
        angledBracketIndex2 = from_email.index('>')
        fromMailId = from_email[angledBracketIndex+1 : angledBracketIndex2]
    
    print("In extractDetails function")
    print(username, fromMailId, subject, body)
    return username, fromMailId, subject, body
