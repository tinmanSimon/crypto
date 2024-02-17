from cryptoData import cryptoData
from mongoDBUtils import mongoProject
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

