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

def get_top_50_volatiles():
    print("get_top_50_volatiles started")
    cryptoProject = mongoProject()
    cryptoProject.setCollection("crypto_analytics", "top_50_volatile_products")
    volatileDataFrame = cryptoProject.getDataframe()
    jsonResult = json.dumps(volatileDataFrame.to_dict('records'), indent=4)
    return jsonResult, volatileDataFrame

def render_dashboard(request: flask.Request) -> flask.Response:
    data = []
    volatileJson, volatileDataFrame = get_top_50_volatiles()
    productIDs = volatileDataFrame['product_id'].to_list()
    cryptoDataHandler = cryptoData()
    upTrendProducts, downTrendProducts = cryptoDataHandler.findCurHourlyTrends(productIDs)
    upJson = json.dumps(upTrendProducts, indent=4)
    downJson = json.dumps(downTrendProducts, indent=4)

    data.append(["Top 50 volatile products", volatileJson])
    data.append(["Uptrend products", upJson])
    data.append(["Downtrend", downJson])
    return render_template('index.html', data=data)

# update the top volatile products to mongoDB
def update_top_volatiles():
    cryptoDataHandler = cryptoData()
    top50VolatileProducts = cryptoDataHandler.getTopVolatileProducts()
    cryptoProject = mongoProject()
    cryptoProject.setCollection("crypto_analytics", "top_50_volatile_products")
    cryptoProject.deleteData()
    cryptoProject.insertData(top50VolatileProducts)
    
# cryptoDataHandler = cryptoData()
# cryptoDataHandler.findCurHourlyTrends(['SPA-USD'])
# cryptoDataHandler.drawCandles({'product_id': 'SPA-USD'})