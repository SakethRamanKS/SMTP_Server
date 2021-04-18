import bcrypt

def verifyHash(hashedPw, checkPw, salt):
    checkPw = checkPw.encode('utf-8')
    hashedCheckPw = bcrypt.hashpw(checkPw, salt)
    if hashedCheckPw == hashedPw:
        return True
    return False