import hashlib
from Crypto.Cipher import AES
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request
import os
from modules.db.dbConnection import MongoConnect
from modules.mail.parseRecvMail import extractDetails
from modules.auth.encrypt import encryptAES

app = Flask(__name__)


@app.route('/email', methods=['POST'])

def receive_email():
    print("Received mail")
    username, fromMailId, subject, body = extractDetails(request)

    encryptText = fromMailId + '+' + subject + '+' + body
    ciphertext, tag, nonce = encryptAES(username, encryptText)

    client = MongoConnect.getConnection()
    dbName = os.environ.get("DBNAME")
    collectionName = os.environ.get("MAILCOLLNAME")
    InMailCollection = client[dbName][collectionName]

    dataDocDict = {'username': username, 'ciphertext': ciphertext, 'tag': tag, 'nonce': nonce}
    print(dataDocDict)
    InMailCollection.insert_one(dataDocDict)

    # print("testing decryption")
    # key = genKey(username)
    # cipher2 = AES.new(key, AES.MODE_EAX, nonce)
    # data2 = cipher2.decrypt_and_verify(ciphertext, tag)
    # print(data2)

    return ''

@app.route('/', methods=['GET'])

def get_req():
    print("Got get request")
    return 'Hello World from Flask!'

app.run(host= '0.0.0.0')

    