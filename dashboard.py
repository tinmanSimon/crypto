from cryptoData import cryptoData
from mongoDBUtils import mongoProject
import flask 
from flask import render_template
import json

def get_mongo_data(database, collectionName):
    print(f"get_mongo_data started. database: {database}, collectionName: {collectionName}")
    cryptoDB = mongoProject()
    cryptoDB.setCollection(database, collectionName)
    volatileDataFrame = cryptoDB.getDataframe()
    jsonResult = json.dumps(volatileDataFrame.to_dict('records'), indent=4)
    return jsonResult

def render_dashboard(request: flask.Request) -> flask.Response:
    data = []
    data.append(["Top 50 volatile products", get_mongo_data("crypto_analytics", "top_50_volatile_products")])
    data.append(["Uptrend products", get_mongo_data("crypto_analytics", "up_trends")])
    data.append(["Downtrend", get_mongo_data("crypto_analytics", "down_trends")])
    data.append(["goldenCrossProducts", get_mongo_data("crypto_analytics", "golden_cross")])
    data.append(["deadCrossProducts", get_mongo_data("crypto_analytics", "dead_cross")])
    return render_template('index.html', data=data)

