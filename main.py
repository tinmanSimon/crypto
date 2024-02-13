from cryptoData import cryptoData
from mongoDBUtils import mongoProject

cryptoDataHandler = cryptoData(True)
data = cryptoDataHandler.getTopVolatileProducts()
cryptoProject = mongoProject()
cryptoProject.setCollection("crypto_analytics", "test_collection")
cryptoProject.deleteData()
cryptoProject.insertData(data)
cryptoProject.printCollection()
