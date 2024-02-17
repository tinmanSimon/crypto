from cryptoData import cryptoData
from mongoDBUtils import mongoProject
import flask 
from flask import render_template
import json

# update the top volatile products to mongoDB
def update_top_volatiles():
    cryptoDataHandler = cryptoData()
    top50VolatileProducts = cryptoDataHandler.getTopVolatileProducts()
    cryptoDB = mongoProject()
    cryptoDB.updateCollectionData(top50VolatileProducts, "crypto_analytics", "top_50_volatile_products")

def update_hourly_trends():
    print("update_hourly_trends started")
    cryptoDB = mongoProject()
    volatileDataFrame = cryptoDB.getDataframe("crypto_analytics", "top_50_volatile_products")
    productIDs = volatileDataFrame['product_id'].to_list()
    cryptoDataHandler = cryptoData()
    productTrends = cryptoDataHandler.findCurHourlyTrends(productIDs)
    cryptoDB.updateCollectionData(productTrends['upTrendProducts'], "crypto_analytics", "up_trends")
    cryptoDB.updateCollectionData(productTrends['downTrendProducts'], "crypto_analytics", "down_trends")
    cryptoDB.updateCollectionData(productTrends['goldenCrossProducts'], "crypto_analytics", "golden_cross")
    cryptoDB.updateCollectionData(productTrends['deadCrossProducts'], "crypto_analytics", "dead_cross")

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

def update_volatile_flask_wrapper(request: flask.Request) -> flask.Response:
    update_top_volatiles()
    response = "update volatiles Done"
    return flask.Response(response, mimetype="text/plain")

def update_hourly_trends_wrapper(request: flask.Request) -> flask.Response:
    update_hourly_trends()
    response = "update hourly trends Done"
    return flask.Response(response, mimetype="text/plain")

