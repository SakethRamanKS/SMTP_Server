# Program to control access to the database
# Uses singleton design pattern

from dotenv import load_dotenv
import os
load_dotenv()
import pymongo

class MongoConnect:
    __instance = None
    @staticmethod
    def getConnection():
        if MongoConnect.__instance == None:
            MongoConnect()
        dbUser = os.environ.get("USERNAME")
        dbPass = os.environ.get("USERPW")
        return pymongo.MongoClient(f"mongodb+srv://{dbUser}:{dbPass}@cluster0.cew55.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    
    def __init__(self):
        if MongoConnect.__instance != None:
            raise Exception("Error: Only one MongoConnect object can be created")
        else:
            MongoConnect.__instance = self

