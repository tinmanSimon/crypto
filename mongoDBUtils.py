from pymongo import MongoClient
from pymongo.server_api import ServerApi
from mysecrets import mongo_uid, mongo_pwd

cryptoV1Uri = f"mongodb+srv://{mongo_uid}:{mongo_pwd}@crypto-v1.y3nxe9o.mongodb.net/?retryWrites=true&w=majority"

class mongoProject:
    def __init__(self, uri = cryptoV1Uri):
        self.projectUri = uri
        self.client = None
        self.createClient()

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



mp = mongoProject()
collection = mp.getCollection("crypto_analytics", "sort_by_volatilities")
data = [
    {
        "product_id" : "BTC-USD",
        "volatilities" : 10
    }, {
        "product_id" : "ETC-USD",
        "volatilities" : 100
    }
]
collection.insert_many(data)