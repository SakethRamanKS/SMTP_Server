from dotenv import load_dotenv
load_dotenv()
from aiosmtpd.smtp import AuthResult, LoginPassword
import os
import modules.auth.hashVerify as hashVerify
from modules.db.dbConnection import MongoConnect
# Defining the authenticator class

supportedMechanisms = ("LOGIN", "PLAIN")

class Authenticator:
    def __init__(self):
        self.client = MongoConnect.getConnection()
        db = self.client.MailDB

    def validateCredentials(self, mechanism, authData):
        # Reading in name of database and collection from envinroment variables
        print("Auth called")
        authFail = AuthResult(success = False, handled = False)

        if mechanism not in supportedMechanisms:
            return authFail
        
        dbName = os.environ.get("DBNAME")
        collectionName = os.environ.get("USERCOLLNAME")

        UserCollection = self.client[dbName][collectionName]
        
        username = authData[0]
        password = authData[1]
        # Querying the database
        user = UserCollection.find_one({"username":username})
        if not user:
            # No user found
            print("No user")
            return authFail

        if hashVerify.verifyHash(user['password'], password, user['salt']):
           print("Successful login")
           return AuthResult(success = True)
        else:
           print("Incorrect Password")
           return authFail
    
    # def test(self, username, password):
    #     dbName = os.environ.get("DBNAME")
    #     collectionName = os.environ.get("USERCOLLNAME")

    #     UserCollection = self.client[dbName][collectionName]
    #     authFail = AuthResult(success = False, handled = False)
    #     user = UserCollection.find_one({"username":username})
    #     if not user:
    #         # No user found
    #         print("No user")
    #         return authFail

    #     hashed=bcrypt.hashpw(password.encode('utf-8'),user['salt'])
    #     if user['password'] == hashed:
    #        print("Successful login")
    #        return AuthResult(success = True)
    #     else:
    #        print("Incorrect Password")
    #        return authFail

if __name__ == "__main__":
    auth = Authenticator()
    print(auth.test("admin1", "abcd"))
