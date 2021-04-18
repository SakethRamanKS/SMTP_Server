import hashlib
from Crypto.Cipher import AES

def genKey(username):
    hashed = hashlib.sha256(username.encode('utf-8')).hexdigest()
    key = hashed[-32:]
    key = key.encode('utf-8')
    return key

def encryptAES(username, content):
    key = genKey(username)
    cipher = AES.new(key, AES.MODE_EAX)
    content = content.encode('utf-8')
    ciphertext, tag = cipher.encrypt_and_digest(content)
    nonce = cipher.nonce
    return ciphertext, tag, nonce

