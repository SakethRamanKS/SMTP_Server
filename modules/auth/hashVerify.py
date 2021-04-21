import bcrypt

def verifyHash(hashedPw, checkPw, salt):
    """Function to verify a bcrypt hash"""
    checkPw = checkPw.encode('utf-8')
    hashedCheckPw = bcrypt.hashpw(checkPw, salt)
    if hashedCheckPw == hashedPw:
        return True
    return False