import pymongo
import bcrypt
myclient = pymongo.MongoClient("mongodb+srv://sanjay:1234@cluster0.cew55.mongodb.net/MailDB?retryWrites=true&w=majority")
mydb = myclient["MailDB"]
mycol = mydb["Users"]

password='123'
user= mycol.find_one({"username":'admin'})
hashed = bcrypt.hashpw(password.encode('utf-8'), user['salt'])
if user['password'] == hashed:
    print("yes")