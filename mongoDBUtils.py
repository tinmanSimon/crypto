from pymongo import MongoClient
from pymongo.server_api import ServerApi
from mysecrets import mongo_uid, mongo_pwd

cryptoV1Uri = f"mongodb+srv://{mongo_uid}:{mongo_pwd}@crypto-v1.y3nxe9o.mongodb.net/?retryWrites=true&w=majority"

class mongoProject:
    def __init__(self, uri = cryptoV1Uri):
        self.projectUri = uri
        self.client = None
        self.createClient()
        self.collection = None

    # create a mongo client and connect to the projectUri
    def createClient(self):
        if self.client: print("Client is already connected"); return
        client = MongoClient(self.projectUri, server_api=ServerApi('1'))
        try:
            client.admin.command('ping')
            print("Successfully connected to MongoDB!")
            self.client = client
        except Exception as e:
            print(e)
        
    def getCollection(self, database, collection):
        return self.client[database][collection]
    
    def setCollection(self, database, collection):
        self.collection = self.client[database][collection]

    def insertData(self, data):
        if self.collection == None: print("mongoProject: Can't insert data without setting collection first!"); return
        try:
            self.collection.insert_many(data)
            print("Successfully inserted data to MongoDB!")
        except Exception as e:
            print(e)

    def deleteData(self, filter = {}):
        if self.collection == None: print("mongoProject: Can't delete data without setting collection first!"); return
        try:
            self.collection.delete_many(filter)
            print("Successfully deleted data from MongoDB!")
        except Exception as e:
            print(e)