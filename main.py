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

def get_mongo_records():
    print("get_mongo_records started")
    cryptoProject = mongoProject()
    cryptoProject.setCollection("crypto_analytics", "test_collection")
    dataFrame = cryptoProject.getDataframe()
    jsonResult = json.dumps(dataFrame.to_dict('records'), indent=4)
    return jsonResult

def render_results(request: flask.Request) -> flask.Response:
    data = []
    data.append(["mongo records", get_mongo_records()])
    return render_template('index.html', data=data)

cryptoDataHandler = cryptoData()
# cryptoDataHandler.drawCandles({
#     'granularity' : 900,
#     'candleSize' : 600
# })
testIDs = cryptoDataHandler.getProductsIDs()[:10]
cryptoDataHandler.findCurHourlyTrends(testIDs)
