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
    return render_template('index.html', data=data)

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
    upTrendProducts, downTrendProducts = cryptoDataHandler.findCurHourlyTrends(productIDs)
    cryptoDB.updateCollectionData(upTrendProducts, "crypto_analytics", "up_trends")
    cryptoDB.updateCollectionData(downTrendProducts, "crypto_analytics", "down_trends")
    
# cryptoDataHandler = cryptoData()
# cryptoDataHandler.findCurHourlyTrends(['SPA-USD'])
# cryptoDataHandler.drawCandles({'product_id': 'SPA-USD'})
# update_hourly_trends()
# update_top_volatiles()
