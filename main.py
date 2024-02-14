from cryptoData import cryptoData
from mongoDBUtils import mongoProject
import flask

# cryptoDataHandler = cryptoData(True)
# data = cryptoDataHandler.getTopVolatileProducts()
# cryptoProject = mongoProject()
# cryptoProject.setCollection("crypto_analytics", "test_collection")
# cryptoProject.deleteData()
# cryptoProject.insertData(data)
# df = cryptoProject.getDataframe()

def get_mongo_records(request: flask.Request) -> flask.Response:
    print("get_mongo_records started")
    cryptoProject = mongoProject()
    cryptoProject.setCollection("crypto_analytics", "test_collection")
    df = cryptoProject.getDataframe()
    return df.to_dict('records')
