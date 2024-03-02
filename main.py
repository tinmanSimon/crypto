from cryptoData import cryptoData
from mongoDBUtils import mongoProject
import flask 
from flask import render_template
import json
import pandas as pd

# update the top volatile products to mongoDB
def update_available_products():
    cryptoDataHandler = cryptoData()
    availableProducts = cryptoDataHandler.getProductsIDs()
    cryptoDB = mongoProject()
    cryptoDB.updateCollectionData(
        "crypto_analytics", 
        "crypto_analysis_results", 
        {
            'analysis_id' : {
                "$eq" : "available-products"
            }
        },
        {
            "$set" : {
                "analysis_data" : availableProducts
            }
        }
    )

# update the top volatile products to mongoDB
def update_top_volatiles():
    cryptoDataHandler = cryptoData()
    top50VolatileProducts = cryptoDataHandler.getTopVolatileProducts()
    cryptoDB = mongoProject()
    cryptoDB.updateCollectionData(
        "crypto_analytics", 
        "crypto_analysis_results", 
        {
            'analysis_id' : {
                "$eq" : "day-volatiles-top-50"
            }
        },
        {
            "$set" : {
                "analysis_data" : top50VolatileProducts
            }
        }
    )

def mongo_pull_available_products():
    cryptoDB = mongoProject()
    cryptoDB.setCollection("crypto_analytics", "crypto_analysis_results")
    volatileDataFrame = pd.DataFrame(cryptoDB.findOneItem(filter={
        'analysis_id' : {
            "$eq" : "available-products"
        }
    })['analysis_data'])
    return volatileDataFrame


def update_hourly_analysis():
    print("update_hourly_trends started")
    cryptoDB = mongoProject()
    cryptoDataHandler = cryptoData()
    availableProducts = mongo_pull_available_products()
    productIDs = availableProducts['product_id'].to_list()
    analysisResultDict = cryptoDataHandler.findCurHourlyAnalysis(productIDs)
    cryptoDB.updateCollectionData(
        "crypto_analytics", 
        "crypto_analysis_results", 
        {
            'analysis_id' : {
                "$eq" : "hourly-analysis"
            }
        },
        {
            "$set" : {
                "analysis_data" : analysisResultDict
            }
        }
    )

def render_dashboard(request: flask.Request) -> flask.Response:
    data = []
    cryptoDB = mongoProject()
    cryptoDB.setCollection("crypto_analytics", "crypto_analysis_results")
    hourlyData = cryptoDB.findOneItem(filter={
        'analysis_id' : {
            "$eq" : "hourly-analysis"
        }
    })['analysis_data']
    data = [[analysis_name, json.dumps(analysis_data, indent=4)] for analysis_name, analysis_data in hourlyData.items()]
    return render_template('index.html', data=data)

def update_volatile_flask_wrapper(request: flask.Request) -> flask.Response:
    update_top_volatiles()
    response = "update volatiles Done"
    return flask.Response(response, mimetype="text/plain")

def update_hourly_analysis_wrapper(request: flask.Request) -> flask.Response:
    update_hourly_analysis()
    response = "update hourly trends Done"
    return flask.Response(response, mimetype="text/plain")
