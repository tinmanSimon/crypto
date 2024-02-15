from cryptoData import cryptoData
from mongoDBUtils import mongoProject
import flask 
from flask import render_template
import json


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
    dataFrame = cryptoProject.getDataframe()
    jsonResult = json.dumps(dataFrame.to_dict('records'), indent=4)
    return render_template('index.html', data=jsonResult)


cryptoDataHandler = cryptoData(True)
cryptoDataHandler.drawCandles('BTC-USD', 900)
